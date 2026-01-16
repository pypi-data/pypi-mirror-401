"""配置管理器 - 配置加载、验证、保存和热更新

功能：
- 配置加载（使用TextProcessor处理换行符）
- 配置验证（必填字段、格式检查）
- 配置保存（使用TextProcessor处理换行符）
- 观察者模式（配置变更通知）
- 统一的robot_wxid获取
- 变更日志记录
- 敏感配置从环境变量读取（auth、dingtalk）
"""
import asyncio
import logging
import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Callable, Awaitable, Tuple

from ..utils.text_processor import TextProcessor

logger = logging.getLogger(__name__)


# 默认忽略的 wxid（系统服务号，避免机器人与它们对话形成循环）
DEFAULT_IGNORE_WXIDS = [
    'qqsafe',           # QQ安全中心
    'weixin',           # 微信团队
    'filehelper',       # 文件传输助手
    'floatbottle',      # 漂流瓶
    'medianote',        # 语音记事本
    'newsapp',          # 腾讯新闻
]

# 忽略的 wxid 前缀（公众号、服务号等）
DEFAULT_IGNORE_PREFIXES = [
    'gh_',              # 公众号/服务号/游戏号
    'wxh_',             # 微信小程序
]

# 从环境变量读取的配置键（这些配置不会被保存到config.yaml）
ENV_CONFIG_KEYS = ['auth', 'dingtalk']


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "config.yaml"):
        self._config: Dict[str, Any] = {}
        self._config_path = Path(config_path)
        self._observers: List[Callable[[Dict, Dict], Awaitable[None]]] = []
        self._lock = asyncio.Lock()
        self._text_processor = TextProcessor()
        self._env_config: Dict[str, Any] = {}  # 从环境变量读取的配置

    @property
    def robot_wxid(self) -> str:
        """统一获取机器人wxid"""
        return self._config.get('qianxun', {}).get('robot_wxid', '')

    @property
    def config(self) -> Dict[str, Any]:
        """获取当前配置（只读）"""
        return self._config.copy()

    def _load_env_config(self) -> Dict[str, Any]:
        """从环境变量加载敏感配置

        环境变量命名规则：
        - AUTH_ENABLED: 是否启用认证 (true/false)
        - AUTH_JWT_SECRET: JWT密钥
        - AUTH_JWT_EXPIRE_HOURS: JWT过期时间（小时）
        - DINGTALK_APP_KEY: 钉钉应用AppKey
        - DINGTALK_APP_SECRET: 钉钉应用AppSecret
        - DINGTALK_CORP_ID: 钉钉企业CorpId
        - DINGTALK_AGENT_ID: 钉钉应用AgentId

        Returns:
            从环境变量读取的配置字典
        """
        env_config: Dict[str, Any] = {}

        # Auth配置
        auth_enabled = os.environ.get('AUTH_ENABLED', '').lower()
        if auth_enabled or os.environ.get('AUTH_JWT_SECRET'):
            env_config['auth'] = {
                'enabled': auth_enabled == 'true',
                'jwt_secret': os.environ.get('AUTH_JWT_SECRET', 'default-secret-change-me'),
                'jwt_expire_hours': int(os.environ.get('AUTH_JWT_EXPIRE_HOURS', '24')),
            }

        # 钉钉配置
        dingtalk_app_key = os.environ.get('DINGTALK_APP_KEY', '')
        if dingtalk_app_key:
            env_config['dingtalk'] = {
                'app_key': dingtalk_app_key,
                'app_secret': os.environ.get('DINGTALK_APP_SECRET', ''),
                'corp_id': os.environ.get('DINGTALK_CORP_ID', ''),
                'agent_id': os.environ.get('DINGTALK_AGENT_ID', ''),
            }

        return env_config

    def load(self) -> Dict[str, Any]:
        """加载配置文件

        Returns:
            加载的配置字典
        """
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}

            # 转换配置中的换行符
            config = self._convert_to_newlines(config)

            # 从环境变量加载敏感配置
            self._env_config = self._load_env_config()

            # 环境变量配置优先级高于文件配置
            for key in ENV_CONFIG_KEYS:
                if key in self._env_config:
                    config[key] = self._env_config[key]
                    logger.info(f"配置 '{key}' 从环境变量加载")

            self._config = config
            logger.info(f"配置已加载: {self._config_path}")
            return config

        except FileNotFoundError:
            logger.warning(f"配置文件不存在: {self._config_path}")
            # 即使文件不存在，也尝试从环境变量加载
            self._env_config = self._load_env_config()
            self._config = self._env_config.copy()
            return self._config
        except yaml.YAMLError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise ValueError(f"配置文件格式错误: {e}")
    
    def _recursive_transform(self, obj: Any, transform_fn: Callable[[str], str],
                             condition: Callable[[str], bool] = lambda _: True) -> Any:
        """递归转换配置中的字符串值

        Args:
            obj: 要转换的对象
            transform_fn: 字符串转换函数
            condition: 条件函数，只有满足条件的字符串才会被转换
        """
        if isinstance(obj, dict):
            return {k: self._recursive_transform(v, transform_fn, condition) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._recursive_transform(item, transform_fn, condition) for item in obj]
        elif isinstance(obj, str) and condition(obj):
            return transform_fn(obj)
        return obj

    def _convert_to_newlines(self, obj: Any) -> Any:
        """递归转换配置中的\\n字符串为真正的换行符"""
        return self._recursive_transform(obj, TextProcessor.config_to_text, lambda s: '\\n' in s)

    def _convert_newlines_for_save(self, obj: Any) -> Any:
        """递归转换换行符为配置文件格式"""
        return self._recursive_transform(obj, TextProcessor.text_to_config)
    
    def validate(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """验证配置格式
        
        Args:
            config: 要验证的配置
            
        Returns:
            (是否有效, 错误信息)
        """
        errors = []
        
        # 检查必填字段
        qianxun = config.get('qianxun', {})
        if not qianxun.get('api_url'):
            errors.append("缺少千寻API地址 (qianxun.api_url)")
        
        # 检查LangBot配置
        langbot = config.get('langbot', {})
        if langbot:
            if langbot.get('ws_host') and not isinstance(langbot.get('ws_port'), int):
                errors.append("LangBot端口必须是整数 (langbot.ws_port)")
        
        # 检查限流配置
        rate_limit = config.get('rate_limit', {})
        if rate_limit:
            min_interval = rate_limit.get('min_interval', 1)
            max_interval = rate_limit.get('max_interval', 3)
            if min_interval < 0 or max_interval < 0:
                errors.append("限流间隔不能为负数")
            if min_interval > max_interval:
                errors.append("最小间隔不能大于最大间隔")
        
        # 检查欢迎配置
        welcome = config.get('welcome', [])
        if isinstance(welcome, list):
            for i, task in enumerate(welcome):
                if task.get('enabled'):
                    # 支持单条 message 或多条 messages
                    has_message = bool(task.get('message') and task.get('message').strip())
                    # 过滤空字符串后检查 messages 数组
                    messages_list = task.get('messages', []) or []
                    valid_messages = [m for m in messages_list if m and m.strip()]
                    has_messages = len(valid_messages) > 0
                    if not has_message and not has_messages:
                        errors.append(f"欢迎配置 #{i+1} 启用但没有设置欢迎词")
        
        # 检查昵称检测配置
        nickname_check = config.get('nickname_check', [])
        if isinstance(nickname_check, list):
            for i, task in enumerate(nickname_check):
                if task.get('enabled'):
                    if not task.get('target_groups'):
                        errors.append(f"昵称检测 #{i+1} 启用但没有设置目标群")
                    if not task.get('regex'):
                        errors.append(f"昵称检测 #{i+1} 启用但没有设置检测规则 (regex)")
        
        # 检查定时提醒配置
        reminders = config.get('scheduled_reminders', [])
        if isinstance(reminders, list):
            for i, task in enumerate(reminders):
                if task.get('enabled'):
                    if not task.get('cron'):
                        errors.append(f"定时提醒 #{i+1} 启用但没有设置cron表达式")
                    if not task.get('content'):
                        errors.append(f"定时提醒 #{i+1} 启用但没有设置提醒内容 (content)")
        
        # 检查排班配置
        duty_schedules = config.get('duty_schedules', [])
        if isinstance(duty_schedules, list):
            for i, schedule in enumerate(duty_schedules):
                if schedule.get('enabled'):
                    if not schedule.get('target_group'):
                        errors.append(f"排班任务 #{i+1} 启用但没有设置目标群")
                    if not schedule.get('schedule_type'):
                        errors.append(f"排班任务 #{i+1} 启用但没有设置排班类型")
                    # 检查自动轮换配置
                    auto = schedule.get('auto_rotation', {})
                    manual = schedule.get('manual_assignments', [])
                    if auto.get('enabled'):
                        if not auto.get('members'):
                            errors.append(f"排班任务 #{i+1} 启用自动轮换但没有设置参与人员")
                    elif not manual:
                        errors.append(f"排班任务 #{i+1} 没有设置自动轮换也没有手动排班")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    async def save(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """保存配置并通知观察者

        注意：auth 和 dingtalk 配置从环境变量读取，不会被保存到文件

        Args:
            config: 新配置

        Returns:
            (是否成功, 错误信息或成功消息)
        """
        async with self._lock:
            # 验证配置
            valid, error = self.validate(config)
            if not valid:
                return False, error

            old_config = self._config.copy()

            try:
                # 自动合并默认忽略列表
                if 'filter' not in config:
                    config['filter'] = {}
                user_ignore = config['filter'].get('ignore_wxids', []) or []
                merged_ignore = list(set(user_ignore + DEFAULT_IGNORE_WXIDS))
                config['filter']['ignore_wxids'] = merged_ignore

                # 准备保存到文件的配置（排除环境变量配置）
                config_to_save = {k: v for k, v in config.items() if k not in ENV_CONFIG_KEYS}

                # 转换换行符为配置文件格式
                converted = self._convert_newlines_for_save(config_to_save)

                # 保存到文件
                with open(self._config_path, "w", encoding="utf-8") as f:
                    yaml.dump(converted, f, allow_unicode=True,
                             default_flow_style=False, sort_keys=False)

                # 更新内存中的配置（保留环境变量配置）
                for key in ENV_CONFIG_KEYS:
                    if key in self._env_config:
                        config[key] = self._env_config[key]

                self._config = config

                # 记录变更日志
                self._log_changes(old_config, config)

                # 通知观察者
                await self._notify_observers(old_config, config)

                logger.info("配置已保存并生效")
                return True, "配置已保存并生效"

            except Exception as e:
                logger.error(f"保存配置失败: {e}")
                return False, f"保存配置失败: {e}"
    
    def _log_changes(self, old_config: Dict, new_config: Dict, prefix: str = ""):
        """记录配置变更日志"""
        all_keys = set(old_config.keys()) | set(new_config.keys())
        
        for key in all_keys:
            full_key = f"{prefix}.{key}" if prefix else key
            old_val = old_config.get(key)
            new_val = new_config.get(key)
            
            if old_val != new_val:
                if isinstance(old_val, dict) and isinstance(new_val, dict):
                    self._log_changes(old_val, new_val, full_key)
                else:
                    # 对于敏感字段，不记录具体值
                    sensitive_keys = ['access_token', 'password', 'secret']
                    if any(s in key.lower() for s in sensitive_keys):
                        logger.info(f"配置变更: {full_key} = [已隐藏]")
                    else:
                        logger.info(f"配置变更: {full_key}: {old_val} -> {new_val}")
    
    def register_observer(self, callback: Callable[[Dict, Dict], Awaitable[None]]):
        """注册配置变更观察者
        
        Args:
            callback: 回调函数，接收 (old_config, new_config)
        """
        self._observers.append(callback)
        logger.debug(f"注册配置观察者，当前共 {len(self._observers)} 个")
    
    def unregister_observer(self, callback: Callable[[Dict, Dict], Awaitable[None]]):
        """取消注册配置变更观察者"""
        if callback in self._observers:
            self._observers.remove(callback)
    
    async def _notify_observers(self, old_config: Dict, new_config: Dict):
        """通知所有观察者配置已变更"""
        for observer in self._observers:
            try:
                await observer(old_config, new_config)
            except Exception as e:
                logger.error(f"通知配置观察者失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项
        
        支持点号分隔的嵌套键，如 'qianxun.api_url'
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_langbot_config(self) -> Dict[str, Any]:
        """获取LangBot连接配置"""
        return self._config.get('langbot', {})
    
    def get_qianxun_config(self) -> Dict[str, Any]:
        """获取千寻配置"""
        return self._config.get('qianxun', {})
    
    def get_filter_config(self) -> Dict[str, Any]:
        """获取过滤配置"""
        return self._config.get('filter', {})
    
    def get_rate_limit_config(self) -> Dict[str, Any]:
        """获取限流配置"""
        return self._config.get('rate_limit', {})
    
    def get_welcome_tasks(self) -> List[Dict[str, Any]]:
        """获取入群欢迎任务列表"""
        welcome = self._config.get('welcome', [])
        if isinstance(welcome, list):
            return welcome
        return [welcome] if welcome else []
    
    def get_nickname_check_tasks(self) -> List[Dict[str, Any]]:
        """获取昵称检测任务列表"""
        return self._config.get('nickname_check', []) or []
    
    def get_scheduled_reminders(self) -> List[Dict[str, Any]]:
        """获取定时提醒任务列表"""
        return self._config.get('scheduled_reminders', []) or []
    
    def get_duty_schedules(self) -> List[Dict[str, Any]]:
        """获取排班任务列表"""
        return self._config.get('duty_schedules', []) or []
