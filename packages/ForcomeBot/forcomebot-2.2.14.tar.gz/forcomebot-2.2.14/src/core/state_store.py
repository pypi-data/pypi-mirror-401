"""状态存储器 - 管理内存状态和持久化"""
import asyncio
import json
import logging
import time
from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class StateStore:
    """状态存储器"""

    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)

        # 数据存储
        self._processed_msg_ids: OrderedDict[str, float] = OrderedDict()
        self._image_cache: OrderedDict[tuple, Dict[str, Any]] = OrderedDict()
        self._group_id_mapping: OrderedDict[str, str] = OrderedDict()
        self._message_user_mapping: OrderedDict[str, str] = OrderedDict()

        # 清理任务
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False

        # 配置限制
        self.max_msg_ids = 10000
        self.max_image_cache = 1000
        self.max_group_mapping = 10000
        self.max_message_mapping = 10000
        self.msg_id_ttl = 60
        self.image_cache_ttl = 120

        # 持久化
        self._state_file = self._data_dir / "state.json"
        self._persist_lock = asyncio.Lock()
        self._dirty = False

    def _enforce_limit(self, collection: OrderedDict, max_size: int):
        """通用的集合大小限制执行"""
        while len(collection) > max_size:
            collection.popitem(last=False)

    def _set_mapping(self, collection: OrderedDict, key: str, value: Any, max_size: int):
        """通用的映射设置方法"""
        collection[key] = value
        self._dirty = True
        collection.move_to_end(key)
        self._enforce_limit(collection, max_size)

    async def start(self):
        """启动状态存储器"""
        logger.info("启动状态存储器...")
        await self._load_persisted()
        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("状态存储器已启动")

    async def stop(self):
        """停止状态存储器"""
        logger.info("停止状态存储器...")
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        await self._persist()
        logger.info("状态存储器已停止")

    def is_duplicate_message(self, msg_id: str) -> bool:
        """检查消息是否重复"""
        if msg_id in self._processed_msg_ids:
            return True
        self._processed_msg_ids[msg_id] = time.time()
        self._dirty = True
        self._enforce_limit(self._processed_msg_ids, self.max_msg_ids)
        return False

    def cache_image(self, group_id: str, user_id: str, image_url: str):
        """缓存图片"""
        cache_key = (group_id, user_id)
        self._image_cache[cache_key] = {"image_url": image_url, "timestamp": time.time()}
        self._dirty = True
        self._image_cache.move_to_end(cache_key)
        self._enforce_limit(self._image_cache, self.max_image_cache)
        logger.debug(f"缓存图片: [{group_id}][{user_id}] -> {image_url}")

    def get_cached_image(self, group_id: str, user_id: str) -> Optional[str]:
        """获取缓存的图片"""
        cache_key = (group_id, user_id)
        cached = self._image_cache.get(cache_key)

        if cached:
            age = time.time() - cached["timestamp"]
            if age < self.image_cache_ttl:
                del self._image_cache[cache_key]
                self._dirty = True
                logger.info(f"命中图片缓存: [{group_id}][{user_id}], 年龄: {age:.1f}秒")
                return cached["image_url"]
            else:
                logger.debug(f"图片缓存已过期: {age:.1f}秒 > {self.image_cache_ttl}秒")
                del self._image_cache[cache_key]
                self._dirty = True
        return None

    def set_group_mapping(self, numeric_id: str, original_id: str):
        """设置群ID映射"""
        self._set_mapping(self._group_id_mapping, numeric_id, original_id, self.max_group_mapping)

    def get_original_group_id(self, numeric_id: str) -> str:
        """获取原始群ID"""
        return self._group_id_mapping.get(numeric_id, numeric_id)

    def set_message_user(self, message_id: str, user_id: str):
        """设置消息-用户映射"""
        self._set_mapping(self._message_user_mapping, message_id, user_id, self.max_message_mapping)

    def get_user_by_message(self, message_id: str) -> Optional[str]:
        """根据消息ID获取用户ID"""
        return self._message_user_mapping.get(message_id)

    async def _cleanup_loop(self):
        """定期清理过期数据（每60秒）"""
        while self._running:
            try:
                await asyncio.sleep(60)
                if not self._running:
                    break
                self._cleanup_expired()
                if self._dirty:
                    await self._persist()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"清理任务异常: {e}", exc_info=True)

    def _cleanup_expired(self):
        """清理过期数据"""
        now = time.time()

        # 清理过期的消息ID
        expired_msg_ids = [k for k, v in self._processed_msg_ids.items() if now - v > self.msg_id_ttl]
        for k in expired_msg_ids:
            del self._processed_msg_ids[k]

        # 清理过期的图片缓存
        expired_images = [k for k, v in self._image_cache.items() if now - v["timestamp"] > self.image_cache_ttl]
        for k in expired_images:
            del self._image_cache[k]

        if expired_msg_ids or expired_images:
            self._dirty = True
            logger.debug(f"清理过期数据: 消息ID={len(expired_msg_ids)}, 图片缓存={len(expired_images)}")

    async def _persist(self):
        """异步持久化数据"""
        async with self._persist_lock:
            try:
                data = {
                    "processed_msg_ids": dict(self._processed_msg_ids),
                    "group_id_mapping": dict(self._group_id_mapping),
                    "message_user_mapping": dict(self._message_user_mapping),
                }

                def write_file():
                    with open(self._state_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                await asyncio.get_event_loop().run_in_executor(None, write_file)
                self._dirty = False
                logger.debug(f"状态已持久化到 {self._state_file}")
            except Exception as e:
                logger.error(f"持久化状态失败: {e}", exc_info=True)

    async def _load_persisted(self):
        """加载持久化数据"""
        if not self._state_file.exists():
            logger.info("没有找到持久化文件，使用空状态启动")
            return

        try:
            def read_file():
                with open(self._state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)

            data = await asyncio.get_event_loop().run_in_executor(None, read_file)
            now = time.time()

            # 恢复消息ID记录（过滤过期的）
            if "processed_msg_ids" in data:
                self._processed_msg_ids = OrderedDict(
                    (k, v) for k, v in data["processed_msg_ids"].items()
                    if now - v <= self.msg_id_ttl
                )

            # 恢复群ID映射
            if "group_id_mapping" in data:
                self._group_id_mapping = OrderedDict(data["group_id_mapping"])

            # 恢复消息-用户映射
            if "message_user_mapping" in data:
                self._message_user_mapping = OrderedDict(data["message_user_mapping"])

            logger.info(f"已从 {self._state_file} 恢复状态: "
                       f"消息ID={len(self._processed_msg_ids)}, "
                       f"群映射={len(self._group_id_mapping)}, "
                       f"消息映射={len(self._message_user_mapping)}")

        except json.JSONDecodeError as e:
            logger.warning(f"持久化文件格式错误，使用空状态启动: {e}")
        except Exception as e:
            logger.error(f"加载持久化数据失败: {e}", exc_info=True)

    def get_stats(self) -> Dict[str, int]:
        """获取状态统计信息"""
        return {
            "processed_msg_ids": len(self._processed_msg_ids),
            "image_cache": len(self._image_cache),
            "group_id_mapping": len(self._group_id_mapping),
            "message_user_mapping": len(self._message_user_mapping),
        }

    def clear_image_cache(self):
        """清空图片缓存"""
        self._image_cache.clear()
        self._dirty = True
        logger.info("图片缓存已清空")

    def clear_all(self):
        """清空所有缓存"""
        self._processed_msg_ids.clear()
        self._image_cache.clear()
        self._group_id_mapping.clear()
        self._message_user_mapping.clear()
        self._dirty = True
        logger.info("所有缓存已清空")
