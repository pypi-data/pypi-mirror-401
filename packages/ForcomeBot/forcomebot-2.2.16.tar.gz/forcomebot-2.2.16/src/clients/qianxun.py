"""千寻框架API封装 - 带重试机制"""
import asyncio
import httpx
import logging
import base64
import json
import re
from typing import Optional, Dict, Any

from ..utils.text_processor import TextProcessor

logger = logging.getLogger(__name__)


class QianXunClient:
    """千寻框架HTTP API客户端（带重试）"""

    # API成功状态码
    SUCCESS_CODES = (0, 200)

    def __init__(self, api_url: str, max_retries: int = 3, retry_delay: float = 1.0):
        """初始化千寻客户端

        Args:
            api_url: 千寻API地址，如 http://192.168.17.181:7777/qianxun/httpapi
            max_retries: 最大重试次数，默认3次
            retry_delay: 初始重试延迟（秒），默认1秒，每次递增
        """
        self.api_url = api_url.rstrip('/')
        self.base_url = '/'.join(api_url.split('/')[:3])
        self.client = httpx.AsyncClient(timeout=30.0)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.text_processor = TextProcessor()

    def update_api_url(self, new_url: str):
        """更新API地址（配置热更新）"""
        self.api_url = new_url.rstrip('/')
        self.base_url = '/'.join(new_url.split('/')[:3])
        logger.info(f"千寻API地址已更新: {self.api_url}")

    def _parse_response(self, resp: httpx.Response) -> Dict[str, Any]:
        """统一解析API响应JSON

        使用 strict=False 容忍非法控制字符（群名/昵称可能包含特殊字符）
        """
        return json.loads(resp.text, strict=False)

    def _is_success(self, result: Dict[str, Any]) -> bool:
        """检查API响应是否成功"""
        return result.get("code") in self.SUCCESS_CODES

    def _get_result_data(self, result: Dict[str, Any]) -> Any:
        """从响应中提取数据"""
        return result.get("result") or result.get("data")

    # 需要重试的HTTP状态码
    RETRY_STATUS_CODES = (502, 503, 504, 429)

    async def _request_with_retry(self, method: str, url: str, **kwargs) -> httpx.Response:
        """带重试的HTTP请求（支持502等错误重试）

        重试策略：
        - 网络异常：重试
        - 502/503/504/429状态码：重试
        - 使用递增延迟（1秒、2秒、3秒）
        """
        last_error: Exception = Exception("请求失败")
        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'GET':
                    resp = await self.client.get(url, **kwargs)
                else:
                    resp = await self.client.post(url, **kwargs)

                # 检查是否需要重试的状态码
                if resp.status_code in self.RETRY_STATUS_CODES:
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (attempt + 1)
                        logger.warning(
                            f"收到HTTP {resp.status_code} (尝试 {attempt + 1}/{self.max_retries})，"
                            f"{delay}秒后重试"
                        )
                        await asyncio.sleep(delay)
                        continue
                    else:
                        logger.error(
                            f"收到HTTP {resp.status_code}，已达最大重试次数 ({self.max_retries})"
                        )

                return resp

            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (attempt + 1)
                    logger.warning(f"请求异常 (尝试 {attempt + 1}/{self.max_retries})，{delay}秒后重试: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"请求异常，已达最大重试次数 ({self.max_retries}): {e}")
        raise last_error

    async def _send_message(
        self,
        robot_wxid: str,
        to_wxid: str,
        msg_type: str,
        data: Dict[str, Any],
        operation_name: str
    ) -> bool:
        """通用消息发送方法

        Args:
            robot_wxid: 机器人wxid
            to_wxid: 接收者wxid
            msg_type: 消息类型（如 sendText, sendImage）
            data: 消息数据
            operation_name: 操作名称（用于日志）

        Returns:
            是否发送成功
        """
        try:
            payload = {"type": msg_type, "data": {"wxid": to_wxid, **data}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)

            if self._is_success(result):
                logger.info(f"{operation_name}成功: {to_wxid}")
                return True
            else:
                logger.error(f"{operation_name}失败: {result}")
                return False
        except Exception as e:
            logger.error(f"{operation_name}异常: {e}", exc_info=True)
            return False
    
    def _extract_base64_data(self, data_url: str) -> str:
        """从 Data URL 中提取 base64 数据并添加千寻框架需要的前缀"""
        if not data_url.startswith('data:'):
            return data_url
        if ';base64,' in data_url:
            return f"base64,{data_url.split(';base64,')[1]}"
        if ',' in data_url:
            return f"base64,{data_url.split(',')[1]}"
        return data_url

    def _sanitize_filename(self, file_name: str) -> str:
        """清理文件名中的特殊字符"""
        if not file_name:
            return file_name
        original_name = file_name
        # 替换 Windows 非法字符和空格
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ']:
            file_name = file_name.replace(char, '_')
        # 只保留字母、数字、中文、下划线、点、横线
        file_name = re.sub(r'[^\w\u4e00-\u9fff.\-]', '_', file_name)
        if original_name != file_name:
            logger.info(f"文件名已处理: {repr(original_name)} -> {repr(file_name)}")
        return file_name

    async def send_text(self, robot_wxid: str, to_wxid: str, msg: str) -> bool:
        """发送文本消息"""
        msg = self.text_processor.encode_for_qianxun(msg)
        return await self._send_message(robot_wxid, to_wxid, "sendText", {"msg": msg}, "发送消息")

    async def send_image(self, robot_wxid: str, to_wxid: str, image_path: str, file_name: str = "") -> bool:
        """发送图片消息"""
        image_path = self._extract_base64_data(image_path)
        return await self._send_message(
            robot_wxid, to_wxid, "sendImage",
            {"path": image_path, "fileName": file_name},
            "发送图片"
        )

    async def send_file(self, robot_wxid: str, to_wxid: str, file_path: str, file_name: str = "") -> bool:
        """发送文件"""
        file_path = self._extract_base64_data(file_path)
        file_name = self._sanitize_filename(file_name)
        logger.info(f"发送文件: to={to_wxid}, fileName={repr(file_name)}")
        return await self._send_message(
            robot_wxid, to_wxid, "sendFile",
            {"path": file_path, "fileName": file_name},
            "发送文件"
        )

    async def send_share_url(
        self, robot_wxid: str, to_wxid: str, title: str, content: str,
        jump_url: str, thumb_path: str = "", app: str = ""
    ) -> bool:
        """发送分享链接"""
        return await self._send_message(
            robot_wxid, to_wxid, "sendShareUrl",
            {"title": title, "content": content, "jumpUrl": jump_url, "path": thumb_path, "app": app},
            "发送分享链接"
        )

    async def send_applet(
        self, robot_wxid: str, to_wxid: str, title: str, content: str,
        jump_path: str, gh: str, thumb_path: str = ""
    ) -> bool:
        """发送小程序"""
        return await self._send_message(
            robot_wxid, to_wxid, "sendApplet",
            {"title": title, "content": content, "jumpPath": jump_path, "gh": gh, "path": thumb_path},
            "发送小程序"
        )

    async def get_contact_info(self, robot_wxid: str, wxid: str) -> Optional[dict]:
        """获取联系人信息"""
        try:
            payload = {"type": "getContactInfo", "data": {"wxid": wxid}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            return self._get_result_data(result) if self._is_success(result) else None
        except Exception as e:
            logger.error(f"获取联系人信息异常: {e}", exc_info=True)
            return None

    async def get_self_info(self, robot_wxid: str) -> Optional[dict]:
        """获取机器人自身信息"""
        try:
            payload = {"type": "getSelfInfo", "data": {"type": "2"}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            logger.info(f"获取机器人信息响应: {result}")

            if self._is_success(result):
                data = self._get_result_data(result)
                if data:
                    for key in ("nick", "nickname"):
                        if data.get(key):
                            data[key] = self.text_processor.decode_emoji(data[key])
                return data
            return None
        except Exception as e:
            logger.error(f"获取机器人信息异常: {e}", exc_info=True)
            return None

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()

    async def get_contact_list(self, robot_wxid: str) -> list:
        """获取联系人列表（包括好友和群）"""
        try:
            payload = {"type": "getContactList", "data": {}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            logger.debug(f"获取联系人列表响应: {result}")

            if self._is_success(result):
                contacts = self._get_result_data(result) or []
                logger.info(f"获取联系人列表: 共 {len(contacts)} 个")
                return contacts
            logger.error(f"获取联系人列表失败: {result}")
            return []
        except Exception as e:
            logger.error(f"获取联系人列表异常: {e}", exc_info=True)
            return []

    async def get_chatroom_list(self, robot_wxid: str, refresh: bool = True) -> list:
        """获取群聊列表"""
        try:
            payload = {"type": "getGroupList", "data": {"type": "2" if refresh else "1"}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            logger.info(f"请求群聊列表: {url}")
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            logger.debug(f"获取群聊列表响应: {result}")

            if self._is_success(result):
                chatrooms = result.get("result", [])
                formatted = [{
                    "wxid": c.get("wxid", ""),
                    "nickname": self.text_processor.decode_emoji(c.get("nick", "") or c.get("wxid", "")),
                    "memberCount": c.get("groupMemberNum", 0)
                } for c in chatrooms]
                logger.info(f"获取群聊列表: 共 {len(formatted)} 个群")
                return formatted
            logger.error(f"获取群聊列表失败: {result}")
            return []
        except Exception as e:
            logger.error(f"获取群聊列表异常: {e}", exc_info=True)
            return []

    async def get_friend_list(self, robot_wxid: str, refresh: bool = True) -> list:
        """获取好友列表"""
        try:
            payload = {"type": "getFriendList", "data": {"type": "2" if refresh else "1"}}
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            logger.debug(f"获取好友列表响应: {result}")

            if self._is_success(result):
                friends = result.get("result", [])
                formatted = [{
                    "wxid": f.get("wxid", ""),
                    "nickname": self.text_processor.decode_emoji(
                        f.get("remark", "") or f.get("nick", "") or f.get("wxid", "")
                    )
                } for f in friends]
                logger.info(f"获取好友列表: 共 {len(formatted)} 个好友")
                return formatted
            logger.error(f"获取好友列表失败: {result}")
            return []
        except Exception as e:
            logger.error(f"获取好友列表异常: {e}", exc_info=True)
            return []

    async def get_group_member_list(
        self, robot_wxid: str, group_wxid: str, get_nick: bool = True, refresh: bool = False
    ) -> list:
        """获取群成员列表"""
        try:
            payload = {
                "type": "getMemberList",
                "data": {
                    "wxid": group_wxid,
                    "type": "2" if refresh else "1",
                    "getNick": "2" if get_nick else "1"
                }
            }
            url = f"{self.api_url}?wxid={robot_wxid}"
            resp = await self._request_with_retry('POST', url, json=payload)
            result = self._parse_response(resp)
            logger.debug(f"获取群成员列表响应: {result}")

            if self._is_success(result):
                members = self._get_result_data(result) or []
                for m in members:
                    for key in ("groupNick", "nickname"):
                        if m.get(key):
                            m[key] = self.text_processor.decode_emoji(m[key])
                logger.info(f"获取群成员列表: {group_wxid}, 共 {len(members)} 人")
                return members
            logger.error(f"获取群成员列表失败: {result}")
            return []
        except Exception as e:
            logger.error(f"获取群成员列表异常: {e}", exc_info=True)
            return []

    async def download_image(self, image_path: str) -> Optional[str]:
        """下载图片并返回 base64 编码"""
        try:
            url = f"{self.base_url}/qianxun/httpapi/file"
            params = {"path": image_path}
            logger.info(f"下载图片: {image_path}")
            resp = await self._request_with_retry('GET', url, params=params)

            if resp.status_code == 200:
                image_data = resp.content
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                logger.info(f"图片下载成功，大小: {len(image_data)} bytes")
                return image_base64
            logger.error(f"下载图片失败: HTTP {resp.status_code}")
            return None
        except Exception as e:
            logger.error(f"下载图片异常: {e}", exc_info=True)
            return None

    def parse_image_path(self, msg: str) -> Optional[str]:
        """从消息中解析图片路径"""
        match = re.search(r'\[pic=([^,\]]+)', msg)
        return match.group(1) if match else None

    def get_image_url(self, image_path: str) -> str:
        """生成千寻图片下载URL"""
        from urllib.parse import urlencode
        return f"{self.base_url}/qianxun/httpapi/file?{urlencode({'path': image_path})}"

    def parse_voice_info(self, xml_content: str) -> Optional[dict]:
        """从XML消息中解析语音信息"""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_content)
            voicemsg = root.find('voicemsg')
            if voicemsg is not None:
                return {'voicelength': int(voicemsg.get('voicelength', 0))}
            return None
        except Exception as e:
            logger.error(f"解析语音XML失败: {e}", exc_info=True)
            return None
