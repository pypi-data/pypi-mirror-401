"""钉钉API客户端"""
import logging
import time
from typing import Optional, Dict, Any

import httpx

logger = logging.getLogger(__name__)


class DingTalkClient:
    """钉钉开放平台API客户端"""

    # API基础地址
    BASE_URL = "https://oapi.dingtalk.com"
    NEW_API_URL = "https://api.dingtalk.com"

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        corp_id: str = "",
        agent_id: str = ""
    ):
        """
        初始化钉钉客户端

        Args:
            app_key: 应用AppKey
            app_secret: 应用AppSecret
            corp_id: 企业CorpId（工作台免登需要）
            agent_id: 应用AgentId（工作台免登需要）
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.corp_id = corp_id
        self.agent_id = agent_id

        # Access Token缓存
        self._access_token: Optional[str] = None
        self._token_expire_time: float = 0

        # HTTP客户端
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """关闭HTTP客户端"""
        await self._client.aclose()

    async def get_access_token(self) -> str:
        """
        获取企业内部应用的Access Token

        Returns:
            Access Token字符串
        """
        # 检查缓存
        if self._access_token and time.time() < self._token_expire_time - 60:
            return self._access_token

        # 请求新Token
        url = f"{self.BASE_URL}/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        try:
            response = await self._client.get(url, params=params)
            data = response.json()

            if data.get("errcode") == 0:
                self._access_token = data["access_token"]
                # Token有效期7200秒
                self._token_expire_time = time.time() + data.get("expires_in", 7200)
                logger.info("获取钉钉Access Token成功")
                return self._access_token
            else:
                logger.error(f"获取钉钉Access Token失败: {data}")
                raise Exception(f"获取Access Token失败: {data.get('errmsg')}")
        except Exception as e:
            logger.error(f"请求钉钉API异常: {e}")
            raise

    async def get_user_info_by_code(self, auth_code: str) -> Dict[str, Any]:
        """
        通过授权码获取用户信息（新版OAuth2扫码登录）

        Args:
            auth_code: 授权码

        Returns:
            用户信息字典
        """
        try:
            # 1. 通过授权码获取用户access_token（新版OAuth2 API）
            url = f"{self.NEW_API_URL}/v1.0/oauth2/userAccessToken"
            body = {
                "clientId": self.app_key,
                "clientSecret": self.app_secret,
                "code": auth_code,
                "grantType": "authorization_code"
            }

            response = await self._client.post(url, json=body)
            data = response.json()

            if "accessToken" not in data:
                logger.error(f"获取用户Token失败: {data}")
                raise Exception(f"获取用户Token失败: {data.get('message', data)}")

            user_access_token = data["accessToken"]
            logger.info("获取用户access_token成功")

            # 2. 使用用户access_token获取用户信息
            user_info_url = f"{self.NEW_API_URL}/v1.0/contact/users/me"
            headers = {"x-acs-dingtalk-access-token": user_access_token}

            user_response = await self._client.get(user_info_url, headers=headers)
            user_data = user_response.json()

            if "unionId" not in user_data:
                logger.error(f"获取用户信息失败: {user_data}")
                raise Exception(f"获取用户信息失败: {user_data.get('message', user_data)}")

            unionid = user_data.get("unionId")
            logger.info(f"获取用户信息成功: unionId={unionid}")

            # 3. 通过unionId获取企业内用户userid
            userid = await self.get_userid_by_unionid(unionid)

            if userid:
                # 获取企业内用户详细信息
                user_detail = await self.get_user_detail(userid)
                return {
                    "userid": userid,
                    "unionid": unionid,
                    "name": user_detail.get("name", user_data.get("nick", "")),
                    "avatar": user_detail.get("avatar", user_data.get("avatarUrl", "")),
                    "mobile": user_detail.get("mobile", user_data.get("mobile", "")),
                    "email": user_detail.get("email", user_data.get("email", "")),
                    "department": self._format_department(user_detail.get("dept_id_list", [])),
                    "title": user_detail.get("title", ""),
                }
            else:
                # 非企业内用户，使用OAuth返回的基本信息
                return {
                    "userid": user_data.get("openId", unionid),
                    "unionid": unionid,
                    "name": user_data.get("nick", ""),
                    "avatar": user_data.get("avatarUrl", ""),
                    "mobile": user_data.get("mobile", ""),
                    "email": user_data.get("email", ""),
                    "department": "",
                    "title": "",
                }

        except Exception as e:
            logger.error(f"通过授权码获取用户信息异常: {e}")
            raise

    async def get_user_info_by_code_internal(self, auth_code: str) -> Dict[str, Any]:
        """
        通过免登授权码获取用户信息（企业内部应用/H5免登）

        Args:
            auth_code: 免登授权码（通过钉钉JSAPI获取）

        Returns:
            用户信息字典
        """
        access_token = await self.get_access_token()

        # 通过免登授权码获取用户userid
        url = f"{self.BASE_URL}/topapi/v2/user/getuserinfo"
        params = {"access_token": access_token}
        body = {"code": auth_code}

        try:
            response = await self._client.post(url, params=params, json=body)
            data = response.json()

            if data.get("errcode") != 0:
                logger.error(f"获取用户信息失败: {data}")
                raise Exception(f"获取用户信息失败: {data.get('errmsg')}")

            result = data.get("result", {})
            userid = result.get("userid")
            unionid = result.get("unionid")

            if not userid:
                raise Exception("未获取到用户userid")

            # 获取用户详细信息
            user_detail = await self.get_user_detail(userid)

            return {
                "userid": userid,
                "unionid": unionid,
                "name": user_detail.get("name", ""),
                "avatar": user_detail.get("avatar", ""),
                "mobile": user_detail.get("mobile", ""),
                "email": user_detail.get("email", ""),
                "department": self._format_department(user_detail.get("dept_id_list", [])),
                "title": user_detail.get("title", ""),
            }

        except Exception as e:
            logger.error(f"通过免登授权码获取用户信息异常: {e}")
            raise

    async def get_user_detail(self, userid: str) -> Dict[str, Any]:
        """
        获取用户详细信息

        Args:
            userid: 用户ID

        Returns:
            用户详细信息
        """
        access_token = await self.get_access_token()

        url = f"{self.BASE_URL}/topapi/v2/user/get"
        params = {"access_token": access_token}
        body = {"userid": userid}

        try:
            response = await self._client.post(url, params=params, json=body)
            data = response.json()

            if data.get("errcode") != 0:
                logger.error(f"获取用户详情失败: {data}")
                raise Exception(f"获取用户详情失败: {data.get('errmsg')}")

            return data.get("result", {})

        except Exception as e:
            logger.error(f"获取用户详情异常: {e}")
            raise

    async def get_userid_by_unionid(self, unionid: str) -> Optional[str]:
        """
        通过UnionId获取UserId

        Args:
            unionid: 用户UnionId

        Returns:
            用户UserId
        """
        access_token = await self.get_access_token()

        url = f"{self.BASE_URL}/topapi/user/getbyunionid"
        params = {"access_token": access_token}
        body = {"unionid": unionid}

        try:
            response = await self._client.post(url, params=params, json=body)
            data = response.json()

            if data.get("errcode") != 0:
                logger.warning(f"通过UnionId获取UserId失败: {data}")
                return None

            return data.get("result", {}).get("userid")

        except Exception as e:
            logger.error(f"通过UnionId获取UserId异常: {e}")
            return None

    async def get_jsapi_ticket(self) -> str:
        """
        获取JSAPI Ticket（H5页面调用钉钉JS API需要）

        Returns:
            JSAPI Ticket
        """
        access_token = await self.get_access_token()

        url = f"{self.BASE_URL}/get_jsapi_ticket"
        params = {"access_token": access_token}

        try:
            response = await self._client.get(url, params=params)
            data = response.json()

            if data.get("errcode") != 0:
                logger.error(f"获取JSAPI Ticket失败: {data}")
                raise Exception(f"获取JSAPI Ticket失败: {data.get('errmsg')}")

            return data.get("ticket", "")

        except Exception as e:
            logger.error(f"获取JSAPI Ticket异常: {e}")
            raise

    def _format_department(self, dept_ids: list) -> str:
        """格式化部门信息"""
        if not dept_ids:
            return ""
        # 简单返回部门ID列表，实际可以查询部门名称
        return ",".join(str(d) for d in dept_ids)

    def generate_qrcode_url(self, redirect_uri: str, state: str = "") -> str:
        """
        生成钉钉扫码登录URL（新版OAuth2）

        Args:
            redirect_uri: 回调地址
            state: 状态参数

        Returns:
            扫码登录URL
        """
        import urllib.parse

        params = {
            "client_id": self.app_key,
            "response_type": "code",
            "scope": "openid",
            "redirect_uri": redirect_uri,
            "state": state or "dingtalk_login",
            "prompt": "consent"
        }

        query = urllib.parse.urlencode(params)
        return f"https://login.dingtalk.com/oauth2/auth?{query}"

    def generate_h5_auth_url(self, redirect_uri: str, state: str = "") -> str:
        """
        生成H5页面授权URL（用于钉钉内H5应用）

        Args:
            redirect_uri: 回调地址
            state: 状态参数

        Returns:
            H5授权URL
        """
        import urllib.parse

        params = {
            "appid": self.app_key,
            "response_type": "code",
            "scope": "snsapi_auth",
            "redirect_uri": redirect_uri,
            "state": state or "dingtalk_h5"
        }

        query = urllib.parse.urlencode(params)
        return f"https://login.dingtalk.com/oauth2/auth?{query}"


# 全局客户端实例
_dingtalk_client: Optional[DingTalkClient] = None


def init_dingtalk_client(
    app_key: str,
    app_secret: str,
    corp_id: str = "",
    agent_id: str = ""
) -> DingTalkClient:
    """初始化全局钉钉客户端"""
    global _dingtalk_client
    _dingtalk_client = DingTalkClient(app_key, app_secret, corp_id, agent_id)
    return _dingtalk_client


def get_dingtalk_client() -> Optional[DingTalkClient]:
    """获取全局钉钉客户端"""
    return _dingtalk_client
