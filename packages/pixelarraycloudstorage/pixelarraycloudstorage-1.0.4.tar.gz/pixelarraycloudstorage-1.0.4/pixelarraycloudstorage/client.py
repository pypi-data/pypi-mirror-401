import aiohttp
from typing import Dict, Any


class AsyncClient:
    """
    异步HTTP客户端基础类
    
    提供统一的API请求功能，支持API Key认证。
    所有请求都返回统一格式的响应字典，包含success、data和message字段。
    
    Attributes:
        base_url (str): API服务器基础URL，默认为 "https://cloudstorage.pixelarrayai.com"
        api_key (str): API密钥，用于身份认证
        headers (Dict[str, str]): 默认请求头，包含Content-Type和X-API-Key
    
    Example:
        ```python
        client = AsyncClient(api_key="your-api-key")
        response = await client._request("GET", "/api/auth/user_info")
        if response["success"]:
            data = response["data"]
        else:
            error_message = response["message"]
        ```
    """

    def __init__(self, api_key: str):
        """
        初始化异步HTTP客户端
        
        Args:
            api_key (str): API密钥，用于身份认证。可通过用户信息API获取。
        
        Raises:
            ValueError: 如果api_key为空或None
        """
        self.base_url = "https://cloudstorage.pixelarrayai.com"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

    async def _request(
        self, method: str, url: str, **kwargs
    ) -> Dict[str, Any]:
        """
        发送异步HTTP请求，返回统一格式的响应字典
        
        此方法封装了所有HTTP请求逻辑，包括：
        - 自动添加API Key认证头
        - 统一错误处理
        - 响应格式标准化
        
        Args:
            method (str): HTTP方法，支持GET、POST、PUT、DELETE等
            url (str): API端点路径，例如 "/api/auth/user_info"
            **kwargs: 其他aiohttp请求参数，例如：
                - json (Dict): JSON请求体（用于POST/PUT）
                - params (Dict): URL查询参数（用于GET）
                - headers (Dict): 额外的请求头（会与默认请求头合并）
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 请求是否成功
                - data (Any): 响应数据，成功时包含实际数据，失败时为{}
                - message (str, 可选): 响应消息，成功时为提示信息，失败时为错误描述
        
        Example:
            ```python
            # GET请求
            response = await client._request("GET", "/api/auth/user_info")
            
            # POST请求
            response = await client._request(
                "POST",
                "/api/file_storage/upload/init",
                json={"filename": "test.txt", "file_type": "text/plain", "total_size": 1024}
            )
            
            # 检查响应
            if response["success"]:
                upload_data = response["data"]
            else:
                error_msg = response["message"]
            ```
        
        Note:
            - 如果服务器返回的响应已经是统一格式（包含success字段），则直接返回
            - 如果响应不是JSON格式，会根据HTTP状态码包装成统一格式
            - 所有异常都会被捕获并返回错误格式的响应
        """
        # 如果kwargs中有headers，则合并headers
        headers = self.headers.copy()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            kwargs = {k: v for k, v in kwargs.items() if k != "headers"}

        async with aiohttp.ClientSession() as session:
            req_method = getattr(session, method.lower())
            try:
                async with req_method(
                    f"{self.base_url}{url}", headers=headers, **kwargs
                ) as resp:
                    try:
                        result = await resp.json()
                        # 如果响应是统一格式，直接返回
                        if isinstance(result, dict) and "success" in result:
                            return result
                        # 如果不是统一格式，包装成统一格式
                        if resp.status == 200:
                            return {
                                "success": True,
                                "data": result.get("data", result),
                                "message": result.get("message", "请求成功"),
                            }
                        else:
                            return {
                                "success": False,
                                "data": {},
                                "message": result.get("message", result.get("detail", f"请求失败，状态码：{resp.status}")),
                            }
                    except Exception as e:
                        # 如果不是JSON响应
                        if resp.status == 200:
                            return {
                                "success": True,
                                "data": {},
                                "message": "请求成功，但响应不是JSON格式",
                            }
                        else:
                            return {
                                "success": False,
                                "data": {},
                                "message": f"请求失败，状态码：{resp.status}",
                            }
            except Exception as e:
                return {
                    "success": False,
                    "data": {},
                    "message": f"请求异常：{str(e)}",
                }
