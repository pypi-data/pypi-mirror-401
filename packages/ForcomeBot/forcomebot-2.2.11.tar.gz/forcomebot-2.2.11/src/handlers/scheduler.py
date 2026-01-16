"""定时任务调度器 - 重构版本

使用新模块：
- ConfigManager 获取配置
- TextProcessor 处理消息文本
- StateStore 持久化任务执行记录
- MessageQueue 统一消息发送

新增功能：
- 任务执行记录（持久化到StateStore）
- 任务执行失败日志
- 支持手动触发任务执行
- 通过消息队列发送，避免并发过高
- 排班提醒功能
- 节假日跳过功能
"""
import logging
import re
import asyncio
import random
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from datetime import datetime, date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..utils.text_processor import TextProcessor

# 尝试导入中国节假日库
try:
    import chinese_calendar
    HAS_CHINESE_CALENDAR = True
except ImportError:
    HAS_CHINESE_CALENDAR = False

if TYPE_CHECKING:
    from ..clients.qianxun import QianXunClient
    from ..core.config_manager import ConfigManager
    from ..core.state_store import StateStore
    from ..core.log_collector import LogCollector
    from ..core.message_queue import MessageQueue

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器 - 重构版本"""
    
    def __init__(
        self,
        qianxun_client: "QianXunClient",
        config_manager: "ConfigManager",
        state_store: "StateStore",
        log_collector: "LogCollector",
        message_queue: Optional["MessageQueue"] = None
    ):
        """初始化定时任务调度器
        
        Args:
            qianxun_client: 千寻客户端
            config_manager: 配置管理器
            state_store: 状态存储器
            log_collector: 日志收集器
            message_queue: 消息队列（可选，如果提供则通过队列发送）
        """
        self.qianxun = qianxun_client
        self.config_manager = config_manager
        self.state_store = state_store
        self.log_collector = log_collector
        self.message_queue = message_queue
        self.text_processor = TextProcessor()
        
        self.scheduler = AsyncIOScheduler()
        self.robot_wxid: Optional[str] = None
        
        # 任务执行历史（内存中保留最近100条）
        self._task_history: List[Dict[str, Any]] = []
        self._max_history = 100
    
    def set_message_queue(self, message_queue: "MessageQueue"):
        """设置消息队列"""
        self.message_queue = message_queue
        logger.info("定时任务调度器已设置消息队列")
    
    @property
    def _config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config_manager.config
    
    @property
    def _rate_limit(self) -> Dict[str, Any]:
        """获取限流配置"""
        return self.config_manager.get_rate_limit_config()
    
    async def _random_delay(self):
        """随机延迟，模拟人工操作（仅在不使用消息队列时调用）
        
        使用配置中的 batch_min_interval 和 batch_max_interval
        """
        min_interval = self._rate_limit.get('batch_min_interval', 2)
        max_interval = self._rate_limit.get('batch_max_interval', 5)
        delay = random.uniform(min_interval, max_interval)
        await asyncio.sleep(delay)
    
    async def _send_text(self, target: str, message: str, task_name: str = ""):
        """发送文本消息（通过消息队列或直接发送）
        
        Args:
            target: 目标wxid
            message: 消息内容
            task_name: 任务名称（用于日志）
        """
        if self.message_queue:
            # 通过消息队列发送
            from ..core.message_queue import MessagePriority
            await self.message_queue.enqueue_text(
                self.qianxun,
                self.robot_wxid,
                target,
                message,
                priority=MessagePriority.NORMAL  # 定时任务使用普通优先级
            )
            logger.info(f"[{task_name}] 消息已加入队列 -> {target}")
        else:
            # 直接发送（带延迟）
            await self._random_delay()
            await self.qianxun.send_text(self.robot_wxid, target, message)
            logger.info(f"[{task_name}] 消息已发送 -> {target}")
    
    def set_robot_wxid(self, wxid: str):
        """设置机器人wxid"""
        self.robot_wxid = wxid
        logger.info(f"调度器设置机器人wxid: {wxid}")
    
    def start(self):
        """启动调度器"""
        # 从配置获取机器人wxid
        robot_wxid = self.config_manager.robot_wxid
        if robot_wxid:
            self.robot_wxid = robot_wxid
            logger.info(f"从配置加载机器人wxid: {robot_wxid}")
        
        self._setup_nickname_check_tasks()
        self._setup_scheduled_reminders()
        self._setup_duty_schedules()
        
        if self.scheduler.get_jobs():
            self.scheduler.start()
            logger.info(f"定时任务调度器已启动，共 {len(self.scheduler.get_jobs())} 个任务")
            for job in self.scheduler.get_jobs():
                try:
                    next_run = job.next_run_time if hasattr(job, 'next_run_time') else None
                    logger.info(f"  - {job.id}: 下次执行 {next_run}")
                except Exception:
                    logger.info(f"  - {job.id}")
        else:
            logger.info("没有启用的定时任务")
    
    def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        logger.info("定时任务调度器已停止")

    def _parse_cron(self, cron_expr: str) -> dict:
        """解析Cron表达式"""
        parts = cron_expr.split()
        
        if len(parts) == 6:
            return {
                'second': parts[0],
                'minute': parts[1],
                'hour': parts[2],
                'day': parts[3],
                'month': parts[4],
                'day_of_week': parts[5].replace('?', '*')
            }
        elif len(parts) == 5:
            return {
                'minute': parts[0],
                'hour': parts[1],
                'day': parts[2],
                'month': parts[3],
                'day_of_week': parts[4].replace('?', '*')
            }
        else:
            raise ValueError(f"无效的Cron表达式: {cron_expr}")
    
    def _setup_nickname_check_tasks(self):
        """设置昵称检测任务"""
        nickname_checks = self.config_manager.get_nickname_check_tasks()
        
        for task in nickname_checks:
            if not task.get('enabled', False):
                continue
            
            task_id = task.get('task_id', 'unnamed')
            cron_expr = task.get('cron', '')
            
            if not cron_expr:
                continue
            
            try:
                cron_params = self._parse_cron(cron_expr)
                trigger = CronTrigger(**cron_params)
                
                self.scheduler.add_job(
                    self._run_nickname_check,
                    trigger,
                    args=[task],
                    id=f"nickname_check_{task_id}",
                    replace_existing=True
                )
                logger.info(f"已添加昵称检测任务: {task_id}, cron={cron_expr}")
            except Exception as e:
                logger.error(f"添加昵称检测任务失败 {task_id}: {e}")
    
    def _setup_scheduled_reminders(self):
        """设置定时提醒任务"""
        reminders = self.config_manager.get_scheduled_reminders()
        
        for idx, task in enumerate(reminders):
            if not task.get('enabled', False):
                continue
            
            task_name = task.get('task_name', f'reminder_{idx}')
            cron_expr = task.get('cron', '')
            
            if not cron_expr:
                continue
            
            try:
                cron_params = self._parse_cron(cron_expr)
                trigger = CronTrigger(**cron_params)
                
                self.scheduler.add_job(
                    self._run_scheduled_reminder,
                    trigger,
                    args=[task],
                    id=f"reminder_{task_name}_{idx}",
                    replace_existing=True
                )
                logger.info(f"已添加定时提醒任务: {task_name}, cron={cron_expr}")
            except Exception as e:
                logger.error(f"添加定时提醒任务失败 {task_name}: {e}")
    
    def _setup_duty_schedules(self):
        """设置排班提醒任务
        
        提醒触发规则：
        - 按日轮换：每天触发，检查当天或提前N天的值班人员
        - 按周轮换：每天触发，检查当天或提前N天是否有值班（由 _run_duty_reminder 判断）
        - 按月轮换：每天触发，检查当天或提前N天是否有值班（由 _run_duty_reminder 判断）
        
        注意：所有类型都设置为每天触发，由 _run_duty_reminder 判断是否需要发送提醒
        这样可以正确支持"提前提醒"功能
        """
        schedules = self.config_manager.get_duty_schedules()
        
        for idx, schedule in enumerate(schedules):
            if not schedule.get('enabled', False):
                continue
            
            schedule_id = schedule.get('schedule_id', f'duty_{idx}')
            reminder = schedule.get('reminder', {})
            
            if not reminder.get('enabled', False):
                continue
            
            remind_time = reminder.get('time', '09:00')
            
            try:
                hour, minute = remind_time.split(':')
                
                # 所有类型都每天触发，由 _run_duty_reminder 判断是否需要发送
                cron_params = {'hour': int(hour), 'minute': int(minute)}
                
                trigger = CronTrigger(**cron_params)
                
                self.scheduler.add_job(
                    self._run_duty_reminder,
                    trigger,
                    args=[schedule],
                    id=f"duty_{schedule_id}_{idx}",
                    replace_existing=True
                )
                schedule_type = schedule.get('schedule_type', 'daily')
                logger.info(f"已添加排班提醒任务: {schedule_id}, time={remind_time}, type={schedule_type}")
            except Exception as e:
                logger.error(f"添加排班提醒任务失败 {schedule_id}: {e}")
    
    def _record_task_execution(
        self, 
        task_id: str, 
        task_type: str, 
        status: str, 
        details: Optional[str] = None
    ):
        """记录任务执行历史
        
        Args:
            task_id: 任务ID
            task_type: 任务类型（nickname_check, scheduled_reminder）
            status: 执行状态（success, failed）
            details: 详细信息
        """
        record = {
            "task_id": task_id,
            "task_type": task_type,
            "executed_at": datetime.now().isoformat(),
            "status": status,
            "details": details
        }
        
        self._task_history.append(record)
        
        # 限制历史记录数量
        if len(self._task_history) > self._max_history:
            self._task_history = self._task_history[-self._max_history:]
        
        logger.info(f"任务执行记录: {task_id} - {status}")
    
    def get_task_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取任务执行历史
        
        Args:
            limit: 返回条数限制
            
        Returns:
            任务执行历史列表（最新的在前）
        """
        return list(reversed(self._task_history))[:limit]
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """获取所有定时任务信息
        
        Returns:
            任务列表
        """
        tasks = []
        
        # 昵称检测任务
        for task in self.config_manager.get_nickname_check_tasks():
            task_id = task.get('task_id', 'unnamed')
            job = self.scheduler.get_job(f"nickname_check_{task_id}")
            tasks.append({
                "id": f"nickname_check_{task_id}",
                "name": task_id,
                "type": "nickname_check",
                "cron": task.get('cron', ''),
                "enabled": task.get('enabled', False),
                "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None
            })
        
        # 定时提醒任务
        for idx, task in enumerate(self.config_manager.get_scheduled_reminders()):
            task_name = task.get('task_name', f'reminder_{idx}')
            job = self.scheduler.get_job(f"reminder_{task_name}_{idx}")
            tasks.append({
                "id": f"reminder_{task_name}_{idx}",
                "name": task_name,
                "type": "scheduled_reminder",
                "cron": task.get('cron', ''),
                "enabled": task.get('enabled', False),
                "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None
            })
        
        # 排班提醒任务
        for idx, schedule in enumerate(self.config_manager.get_duty_schedules()):
            schedule_id = schedule.get('schedule_id', f'duty_{idx}')
            job = self.scheduler.get_job(f"duty_{schedule_id}_{idx}")
            reminder = schedule.get('reminder', {})
            tasks.append({
                "id": f"duty_{schedule_id}_{idx}",
                "name": schedule_id,
                "type": "duty_schedule",
                "schedule_type": schedule.get('schedule_type', 'daily'),
                "remind_time": reminder.get('time', ''),
                "enabled": schedule.get('enabled', False),
                "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None
            })
        
        return tasks

    async def run_task_manually(self, task_id: str) -> Dict[str, Any]:
        """手动触发任务执行
        
        Args:
            task_id: 任务ID（如 nickname_check_xxx 或 reminder_xxx_0 或 duty_xxx_0）
            
        Returns:
            执行结果
        """
        logger.info(f"手动触发任务: {task_id}")
        
        try:
            if task_id.startswith("nickname_check_"):
                # 查找对应的昵称检测任务
                check_id = task_id.replace("nickname_check_", "")
                for task in self.config_manager.get_nickname_check_tasks():
                    if task.get('task_id') == check_id:
                        await self._run_nickname_check(task)
                        return {"status": "success", "message": f"任务 {task_id} 执行完成"}
                return {"status": "error", "message": f"未找到任务: {task_id}"}
            
            elif task_id.startswith("reminder_"):
                # 查找对应的定时提醒任务
                for idx, task in enumerate(self.config_manager.get_scheduled_reminders()):
                    task_name = task.get('task_name', f'reminder_{idx}')
                    if task_id == f"reminder_{task_name}_{idx}":
                        await self._run_scheduled_reminder(task)
                        return {"status": "success", "message": f"任务 {task_id} 执行完成"}
                return {"status": "error", "message": f"未找到任务: {task_id}"}
            
            elif task_id.startswith("duty_"):
                # 查找对应的排班提醒任务
                for idx, schedule in enumerate(self.config_manager.get_duty_schedules()):
                    schedule_id = schedule.get('schedule_id', f'duty_{idx}')
                    if task_id == f"duty_{schedule_id}_{idx}":
                        await self._run_duty_reminder(schedule)
                        return {"status": "success", "message": f"任务 {task_id} 执行完成"}
                return {"status": "error", "message": f"未找到任务: {task_id}"}
            
            else:
                return {"status": "error", "message": f"未知任务类型: {task_id}"}
                
        except Exception as e:
            logger.error(f"手动执行任务失败 {task_id}: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
    
    async def _run_nickname_check(self, task: dict):
        """执行昵称检测任务"""
        if not self.robot_wxid:
            logger.warning("机器人wxid未设置，跳过昵称检测")
            return
        
        task_id = task.get('task_id', 'unnamed')
        target_groups = task.get('target_groups', [])
        exclude_users = task.get('exclude_users', [])
        regex_pattern = task.get('regex', '')
        message_tpl = task.get('message_tpl', '⚠️ @{user} 您的昵称不规范，请及时修改。')
        
        if not target_groups or not regex_pattern:
            return
        
        logger.info(f"开始执行昵称检测任务: {task_id}")
        
        try:
            pattern = re.compile(regex_pattern)
        except re.error as e:
            logger.error(f"正则表达式无效 {task_id}: {e}")
            self._record_task_execution(task_id, "nickname_check", "failed", f"正则表达式无效: {e}")
            return
        
        try:
            for group_id in target_groups:
                await self._check_group_nicknames(
                    group_id, pattern, exclude_users, message_tpl, task_id
                )
            
            self._record_task_execution(task_id, "nickname_check", "success")
            
        except Exception as e:
            logger.error(f"昵称检测任务执行失败 {task_id}: {e}", exc_info=True)
            self._record_task_execution(task_id, "nickname_check", "failed", str(e))
    
    async def _check_group_nicknames(
        self, 
        group_id: str, 
        pattern: re.Pattern, 
        exclude_users: List[str],
        message_tpl: str,
        task_id: str
    ):
        """检测单个群的昵称"""
        logger.info(f"检测群 {group_id} 的昵称")
        
        members = await self.qianxun.get_group_member_list(
            self.robot_wxid, group_id, get_nick=True, refresh=True
        )
        
        if not members:
            logger.warning(f"获取群 {group_id} 成员列表失败或为空")
            return
        
        non_compliant = []
        for member in members:
            wxid = member.get('wxid', '')
            nick = member.get('groupNick', '')
            
            if wxid in exclude_users:
                continue
            
            if nick and not pattern.match(nick):
                non_compliant.append({'wxid': wxid, 'nick': nick})
        
        if not non_compliant:
            logger.info(f"群 {group_id} 所有成员昵称均合规")
            return
        
        logger.info(f"群 {group_id} 有 {len(non_compliant)} 人昵称不合规")
        
        at_codes = [f"[@,wxid={m['wxid']},nick=,isAuto=true]" for m in non_compliant]
        at_str = " ".join(at_codes)
        message = message_tpl.replace('{user}', at_str)
        
        # 使用 TextProcessor 把 \n 字符串转换为真正的换行符
        message = self.text_processor.config_to_text(message)
        
        logger.debug(f"发送消息内容: {repr(message)}")
        
        # 通过统一方法发送
        await self._send_text(group_id, message, f"昵称检测_{task_id}")
        nicks = ", ".join([m['nick'] for m in non_compliant])
        logger.info(f"已发送昵称提醒: {nicks}")
    
    async def _run_scheduled_reminder(self, task: dict):
        """执行定时提醒任务"""
        if not self.robot_wxid:
            logger.warning("机器人wxid未设置，跳过定时提醒")
            return
        
        task_name = task.get('task_name', 'unnamed')
        target_groups = task.get('target_groups', [])
        mention_users = task.get('mention_users', [])
        content = task.get('content', '')
        
        if not target_groups or not content:
            return
        
        logger.info(f"开始执行定时提醒任务: {task_name}")
        
        try:
            at_prefix = ""
            if mention_users:
                if "all" in mention_users:
                    at_prefix = "[@,wxid=all,nick=,isAuto=true] "
                else:
                    at_codes = [f"[@,wxid={uid},nick=,isAuto=true]" for uid in mention_users]
                    at_prefix = " ".join(at_codes) + " "
            
            message = at_prefix + content
            
            # 使用 TextProcessor 把 \n 转换为真正的换行符
            message = self.text_processor.config_to_text(message)
            
            for group_id in target_groups:
                await self._send_text(group_id, message, f"定时提醒_{task_name}")
            
            self._record_task_execution(task_name, "scheduled_reminder", "success")
            
        except Exception as e:
            logger.error(f"定时提醒任务执行失败 {task_name}: {e}", exc_info=True)
            self._record_task_execution(task_name, "scheduled_reminder", "failed", str(e))
    
    def reload_tasks(self):
        """重新加载任务（配置变更后调用）"""
        logger.info("重新加载定时任务...")
        
        # 移除所有现有任务
        for job in self.scheduler.get_jobs():
            job.remove()
        
        # 重新设置任务
        self._setup_nickname_check_tasks()
        self._setup_scheduled_reminders()
        self._setup_duty_schedules()
        
        logger.info(f"定时任务已重新加载，共 {len(self.scheduler.get_jobs())} 个任务")
    
    def _is_holiday(self, target_date: date) -> bool:
        """判断是否为法定节假日
        
        Args:
            target_date: 目标日期
            
        Returns:
            是否为节假日
        """
        if not HAS_CHINESE_CALENDAR:
            return False
        
        try:
            return chinese_calendar.is_holiday(target_date)
        except Exception as e:
            logger.warning(f"判断节假日失败: {e}")
            return False
    
    def _is_workday(self, target_date: date) -> bool:
        """判断是否为工作日（包括调休补班）
        
        Args:
            target_date: 目标日期
            
        Returns:
            是否为工作日
        """
        if not HAS_CHINESE_CALENDAR:
            # 没有库时，简单判断周末
            return target_date.weekday() < 5
        
        try:
            return chinese_calendar.is_workday(target_date)
        except Exception as e:
            logger.warning(f"判断工作日失败: {e}")
            return target_date.weekday() < 5
    
    def _should_skip_date(
        self, 
        schedule: Dict[str, Any], 
        target_date: date
    ) -> bool:
        """判断是否应该跳过该日期
        
        Args:
            schedule: 排班配置
            target_date: 目标日期
            
        Returns:
            是否跳过
        """
        target_date_str = target_date.isoformat()
        
        # 1. 检查手动增加的日期（优先级最高，不跳过）
        included_dates = schedule.get('included_dates', [])
        if target_date_str in included_dates:
            return False
        
        # 2. 检查手动排除的日期
        excluded_dates = schedule.get('excluded_dates', [])
        if target_date_str in excluded_dates:
            return True
        
        # 3. 检查是否跳过节假日
        skip_holidays = schedule.get('skip_holidays', False)
        if skip_holidays and self._is_holiday(target_date):
            return True
        
        return False
    
    def _get_duty_users_for_date(
        self, 
        schedule: Dict[str, Any], 
        target_date: date
    ) -> List[Dict[str, str]]:
        """获取指定日期的值班人员
        
        Args:
            schedule: 排班配置
            target_date: 目标日期
            
        Returns:
            值班人员列表 [{"wxid": "xxx", "name": "张三"}, ...]
        """
        # 检查是否应该跳过该日期
        if self._should_skip_date(schedule, target_date):
            return []
        
        # 1. 优先检查手动指定
        manual_assignments = schedule.get('manual_assignments', [])
        target_date_str = target_date.isoformat()
        
        for assignment in manual_assignments:
            if assignment.get('date') == target_date_str:
                return assignment.get('users', [])
        
        # 2. 使用自动轮换计算
        auto = schedule.get('auto_rotation', {})
        if not auto.get('enabled', False):
            return []
        
        members = auto.get('members', [])
        if not members:
            return []
        
        group_size = auto.get('group_size', 1)
        start_date_str = auto.get('start_date', '')
        
        if not start_date_str:
            return []
        
        try:
            start_date = date.fromisoformat(start_date_str)
        except ValueError:
            logger.error(f"无效的开始日期: {start_date_str}")
            return []
        
        # 如果目标日期在开始日期之前，返回空
        if target_date < start_date:
            return []
        
        schedule_type = schedule.get('schedule_type', 'daily')
        total_groups = len(members) // group_size
        if total_groups == 0:
            total_groups = 1
        
        # 计算有效的轮换周期数（跳过节假日和排除日期）
        skip_holidays = schedule.get('skip_holidays', False)
        excluded_dates = set(schedule.get('excluded_dates', []))
        included_dates = set(schedule.get('included_dates', []))
        
        if schedule_type == 'daily':
            # 按日轮换：计算从开始日期到目标日期之间的有效天数
            periods_passed = 0
            current = start_date
            while current < target_date:
                current_str = current.isoformat()
                # 判断该日期是否有效
                if current_str in included_dates:
                    # 手动增加的日期，算有效
                    periods_passed += 1
                elif current_str in excluded_dates:
                    # 手动排除的日期，跳过
                    pass
                elif skip_holidays and self._is_holiday(current):
                    # 节假日，跳过
                    pass
                else:
                    # 正常日期，算有效
                    periods_passed += 1
                current += timedelta(days=1)
        elif schedule_type == 'weekly':
            periods_passed = (target_date - start_date).days // 7
        elif schedule_type == 'monthly':
            periods_passed = (target_date.year - start_date.year) * 12 + (target_date.month - start_date.month)
        else:
            periods_passed = (target_date - start_date).days
        
        group_index = periods_passed % total_groups
        start_idx = group_index * group_size
        end_idx = min(start_idx + group_size, len(members))
        
        return members[start_idx:end_idx]
    
    async def _run_duty_reminder(self, schedule: Dict[str, Any]):
        """执行排班提醒任务
        
        提醒逻辑：
        1. 根据 timing_type 计算目标值班日期
           - same_day: 今天
           - advance: 今天 + advance_days
        2. 获取目标日期的值班人员
        3. 如果有值班人员，发送提醒
        4. 如果启用重复提醒，按间隔重复发送
        """
        if not self.robot_wxid:
            logger.warning("机器人wxid未设置，跳过排班提醒")
            return
        
        schedule_id = schedule.get('schedule_id', 'unnamed')
        target_group = schedule.get('target_group', '')
        reminder = schedule.get('reminder', {})
        
        if not target_group:
            logger.warning(f"排班任务 {schedule_id} 没有设置目标群")
            return
        
        logger.info(f"开始执行排班提醒任务: {schedule_id}")
        
        try:
            # 根据提醒时机计算目标日期
            timing_type = reminder.get('timing_type', 'same_day')
            advance_days = reminder.get('advance_days', 1)
            
            today = date.today()
            if timing_type == 'advance':
                # 提前提醒：获取N天后的值班人员
                target_date = today + timedelta(days=advance_days)
            else:
                # 当天提醒：获取今天的值班人员
                target_date = today
            
            # 检查结束日期
            auto = schedule.get('auto_rotation', {})
            end_date_str = auto.get('end_date', '')
            if end_date_str:
                try:
                    end_date = date.fromisoformat(end_date_str)
                    if target_date > end_date:
                        logger.info(f"排班任务 {schedule_id} 目标日期 {target_date} 已超过结束日期 {end_date}")
                        return
                except ValueError:
                    pass
            
            duty_users = self._get_duty_users_for_date(schedule, target_date)
            
            if not duty_users:
                logger.info(f"排班任务 {schedule_id} 目标日期 {target_date} 没有值班人员（可能是节假日或未排班）")
                return
            
            # 构建@用户列表
            at_codes = [f"[@,wxid={u['wxid']},nick=,isAuto=true]" for u in duty_users]
            at_str = " ".join(at_codes)
            user_names = "、".join([u.get('name', u['wxid']) for u in duty_users])
            
            # 格式化日期
            target_date_str = target_date.strftime('%m月%d日')
            
            # 构建消息
            message_tpl = reminder.get('message', '📢 值班提醒\n\n{users} 今天是你们的值班日！')
            message = message_tpl.replace('{users}', at_str).replace('{names}', user_names).replace('{date}', target_date_str)
            
            # 使用 TextProcessor 处理换行符
            message = self.text_processor.config_to_text(message)
            
            # 发送提醒
            repeat_enabled = reminder.get('repeat_enabled', False)
            repeat_count = reminder.get('repeat_count', 1) if repeat_enabled else 1
            repeat_interval = reminder.get('repeat_interval', 30)  # 分钟
            
            for i in range(repeat_count):
                if i > 0:
                    # 等待间隔时间
                    await asyncio.sleep(repeat_interval * 60)
                
                await self._send_text(target_group, message, f"排班提醒_{schedule_id}")
                logger.info(f"[排班提醒_{schedule_id}] 第{i+1}次提醒已发送，值班日期: {target_date}，值班人员: {user_names}")
            
            self._record_task_execution(schedule_id, "duty_schedule", "success", f"值班日期: {target_date}, 值班人员: {user_names}")
            
        except Exception as e:
            logger.error(f"排班提醒任务执行失败 {schedule_id}: {e}", exc_info=True)
            self._record_task_execution(schedule_id, "duty_schedule", "failed", str(e))
