from pixelarraycloudstorage.client import AsyncClient
from typing import Dict, Any, Optional, List, AsyncGenerator
import os
import aiohttp
import mimetypes
import math
import time


class FileStorageManagerAsync(AsyncClient):
    """
    异步文件存储管理器
    
    提供完整的文件存储功能，包括：
    - 文件上传（支持分片上传）
    - 文件下载
    - 文件列表查询
    - 文件删除
    - 流量统计查询
    
    所有方法都是异步的，使用async/await语法。
    所有方法返回统一格式的字典，包含success、data和message字段。
    
    Attributes:
        base_url (str): API服务器基础URL（继承自AsyncClient）
        api_key (str): API密钥（继承自AsyncClient）
        headers (Dict[str, str]): 默认请求头（继承自AsyncClient）
    
    Example:
        ```python
        import asyncio
        
        async def main():
            # 创建文件存储管理器实例
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 上传文件
            result = await manager.upload(
                file_path="/path/to/local/file.txt",
                remote_path="folder1/file.txt"
            )
            if result["success"]:
                print(f"上传成功: {result['data']}")
            else:
                print(f"上传失败: {result['message']}")
            
            # 获取文件列表
            files_result = await manager.list_files(remote_path="folder1", page=1, page_size=50)
            if files_result["success"]:
                files = files_result["data"].get("data", [])
                print(f"找到 {len(files)} 个文件")
        
        asyncio.run(main())
        ```
    """

    def __init__(self, api_key: str):
        """
        初始化异步文件存储管理器
        
        Args:
            api_key (str): API密钥，用于身份认证。可通过用户信息API获取。
        
        Raises:
            ValueError: 如果api_key为空或None
        """
        super().__init__(api_key)

    async def get_namespace(self) -> Optional[str]:
        """
        获取当前用户的命名空间
        
        通过调用用户信息API获取当前账号绑定的命名空间。
        命名空间用于文件存储的路径标识和权限控制。
        
        Returns:
            Optional[str]: 用户的命名空间字符串，如果未绑定则返回None
        
        Raises:
            RuntimeError: 如果获取用户信息失败或账号未绑定命名空间
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            try:
                namespace = await manager.get_namespace()
                print(f"当前命名空间: {namespace}")
            except RuntimeError as e:
                print(f"获取命名空间失败: {e}")
            ```
        
        Note:
            - 命名空间是文件存储系统中的唯一标识符
            - 每个用户只能绑定一个命名空间
            - 命名空间不能为空，必须由3-64位字母、数字、下划线或中划线组成
        """
        user_info_response = await self._request("GET", "/api/auth/user_info")
        if not user_info_response.get("success"):
            raise RuntimeError(user_info_response.get("message", "获取用户信息失败，无法确定命名空间"))
        user_info = user_info_response.get("data", {})
        namespace = user_info.get("namespace")
        if not namespace:
            raise RuntimeError("当前账号未绑定命名空间")
        return namespace

    async def upload(
        self,
        file_path: str,
        remote_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        上传文件到云端存储
        
        此方法封装了完整的上传流程，包括：
        1. 初始化上传（获取上传ID和分片URL）
        2. 分片上传（将文件分成2MB的分片，并行上传到OSS）
        3. 完成上传（通知服务器合并分片并创建文件记录）
        
        如果remote_path未提供，则使用file_path作为远端路径。
        如果remote_path包含目录路径（如"folder1/folder2/file.txt"），会自动创建所需的目录结构。
        
        Args:
            file_path (str): 本地文件路径，必须是存在的文件
            remote_path (Optional[str]): 云端保存路径，可选。如果未提供，则使用file_path的值。
                路径可以使用斜杠分隔目录，例如："folder1/folder2/file.txt"
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 上传是否成功
                - data (Dict[str, Any]): 上传结果数据，成功时包含：
                    - file_record (Dict): 文件记录信息，包含文件ID、名称、大小等
                    - oss_url (str): OSS访问URL（可选）
                    - oss_path (str): OSS存储路径（可选）
                - message (str): 响应消息，成功时为提示信息，失败时为错误描述
        
        Raises:
            FileNotFoundError: 如果本地文件不存在
            RuntimeError: 如果获取命名空间失败
            aiohttp.ClientError: 如果网络请求失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 上传文件到根目录
            result = await manager.upload(
                file_path="/local/path/document.pdf",
                remote_path="documents/document.pdf"
            )
            
            if result["success"]:
                file_record = result["data"].get("file_record", {})
                print(f"上传成功，文件ID: {file_record.get('id')}")
            else:
                print(f"上传失败: {result['message']}")
            ```
        
        Note:
            - 文件会被分成2MB的分片进行上传，支持大文件
            - 上传过程中会自动创建所需的目录结构
            - 如果同名文件已存在，上传会失败
        """
        final_result: Dict[str, Any] = {}
        error_message = "上传失败"
        async for progress in self.upload_stream(
            file_path=file_path, remote_path=remote_path
        ):
            event = progress.get("event")
            if event == "error":
                return {
                    "success": False,
                    "data": {},
                    "message": progress.get("message", "上传失败"),
                }
            if event == "complete" and progress.get("success"):
                final_result = progress.get("result", {})
                return {
                    "success": True,
                    "data": final_result,
                    "message": progress.get("message", "上传成功"),
                }
        return {
            "success": False,
            "data": {},
            "message": error_message,
        }

    async def upload_stream(
        self,
        file_path: str,
        remote_path: Optional[str] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        上传文件（流式，返回异步生成器，包含实时进度信息）
        
        此方法是upload方法的流式版本，通过异步生成器实时返回上传进度。
        适用于需要显示上传进度条的场景。
        
        Args:
            file_path (str): 本地文件路径，必须是存在的文件
            remote_path (Optional[str]): 云端保存路径，可选。如果未提供，则使用file_path的值
        
        Yields:
            Dict[str, Any]: 进度信息字典，包含以下字段：
                - event (str): 事件类型，可能的值：
                    - "init": 初始化完成
                    - "chunk": 单个分片上传完成
                    - "complete": 所有分片上传完成
                    - "error": 上传失败
                - percentage (float): 上传进度百分比（0-100）
                - total_chunks (int): 总分片数
                - remaining_chunks (int): 剩余分片数
                - total_bytes (int): 文件总大小（字节）
                - processed_bytes (int): 已处理字节数
                - chunk_index (int): 当前分片索引（仅chunk事件）
                - chunk_size (int): 当前分片大小（仅chunk事件）
                - speed (float): 当前上传速度（字节/秒）
                - message (str): 进度消息
                - success (bool): 是否成功
                - result (Dict): 完成时的结果数据（仅complete事件）
        
        Raises:
            FileNotFoundError: 如果本地文件不存在
            RuntimeError: 如果获取命名空间失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            async for progress in manager.upload_stream(
                file_path="/local/path/bigfile.zip",
                remote_path="backups/bigfile.zip"
            ):
                event = progress.get("event")
                percentage = progress.get("percentage", 0)
                
                if event == "init":
                    print("初始化完成，开始上传...")
                elif event == "chunk":
                    speed_mbps = progress.get("speed", 0) / (1024 * 1024)
                    print(f"进度: {percentage:.1f}% | 速度: {speed_mbps:.2f} MB/s")
                elif event == "complete":
                    print("上传完成！")
                    file_record = progress.get("result", {})
                    print(f"文件ID: {file_record.get('file_record', {}).get('id')}")
                elif event == "error":
                    print(f"上传失败: {progress.get('message')}")
                    break
            ```
        
        Note:
            - 分片大小为2MB，大文件会被自动分割
            - 每个分片上传后都会返回进度信息
            - 如果上传失败，会返回error事件并停止生成
        """
        chunk_size = 2 * 1024 * 1024  # 2MB
        upload_start = time.perf_counter()
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        total_size = len(file_bytes)

        file_name = remote_path.split("/")[-1]
        mime_type = mimetypes.guess_type(file_path)[0]
        init_data = {
            "filename": file_name,
            "file_type": mime_type,
            "total_size": total_size,
            "file_path": remote_path,
        }
        namespace = await self.get_namespace()
        if namespace:
            init_data["namespace"] = namespace

        init_result = await self._request(
            "POST", "/api/file_storage/upload/init", json=init_data
        )
        if not init_result.get("success"):
            yield {
                "event": "error",
                "percentage": 0,
                "total_chunks": 0,
                "remaining_chunks": 0,
                "total_bytes": total_size,
                "processed_bytes": 0,
                "speed": 0,
                "message": init_result.get("message", "初始化上传失败"),
                "success": False,
            }
            return

        upload_data = init_result.get("data", {})
        upload_id = upload_data.get("upload_id")
        chunk_urls = upload_data.get("chunk_urls", [])
        total_chunks = len(chunk_urls)

        if not upload_id or not chunk_urls:
            yield {
                "event": "error",
                "percentage": 0,
                "total_chunks": 0,
                "remaining_chunks": 0,
                "total_bytes": total_size,
                "processed_bytes": 0,
                "speed": 0,
                "message": "缺少上传ID或分片信息",
                "success": False,
            }
            return

        yield {
            "event": "init",
            "percentage": 0,
            "total_chunks": total_chunks,
            "remaining_chunks": total_chunks,
            "total_bytes": total_size,
            "processed_bytes": 0,
            "speed": 0,
            "message": "初始化完成，开始上传分片",
            "success": True,
        }

        parts: List[Dict[str, Any]] = []
        uploaded_bytes = 0

        async with aiohttp.ClientSession() as session:
            for idx, chunk_info in enumerate(chunk_urls):
                part_number = chunk_info.get("part_number")
                url = chunk_info.get("url")
                start = idx * chunk_size
                end = min(start + chunk_size, total_size)
                chunk_data = file_bytes[start:end]

                if not url or not part_number:
                    percentage = (
                        0
                        if total_size == 0
                        else min((uploaded_bytes / total_size) * 100, 100)
                    )
                    yield {
                        "event": "error",
                        "percentage": percentage,
                        "total_chunks": total_chunks,
                        "remaining_chunks": total_chunks - idx,
                        "total_bytes": total_size,
                        "processed_bytes": uploaded_bytes,
                        "speed": 0,
                        "message": "分片信息缺失",
                        "success": False,
                    }
                    return

                chunk_start = time.perf_counter()
                try:
                    async with session.put(url, data=chunk_data) as resp:
                        if resp.status != 200:
                            raise RuntimeError(f"分片上传失败，状态码：{resp.status}")
                        etag = resp.headers.get("ETag", "").strip('"')
                        parts.append(
                            {
                                "part_number": part_number,
                                "etag": etag,
                            }
                        )
                except Exception as exc:
                    percentage = (
                        0
                        if total_size == 0
                        else min((uploaded_bytes / total_size) * 100, 100)
                    )
                    yield {
                        "event": "error",
                        "percentage": percentage,
                        "total_chunks": total_chunks,
                        "remaining_chunks": max(total_chunks - idx, 0),
                        "total_bytes": total_size,
                        "processed_bytes": uploaded_bytes,
                        "speed": 0,
                        "message": f"分片上传异常：{exc}",
                        "success": False,
                    }
                    return

                uploaded_bytes += len(chunk_data)
                duration = max(time.perf_counter() - chunk_start, 1e-6)
                speed = len(chunk_data) / duration
                percentage = (
                    100
                    if total_size == 0
                    else min((uploaded_bytes / total_size) * 100, 100)
                )

                yield {
                    "event": "chunk",
                    "percentage": percentage,
                    "total_chunks": total_chunks,
                    "remaining_chunks": max(total_chunks - (idx + 1), 0),
                    "total_bytes": total_size,
                    "processed_bytes": uploaded_bytes,
                    "chunk_index": idx,
                    "chunk_size": len(chunk_data),
                    "speed": speed,
                    "message": f"分片{idx + 1}/{total_chunks}上传完成",
                    "success": True,
                }

        complete_data = {
            "upload_id": upload_id,
            "parts": parts,
        }
        complete_result = await self._request(
            "POST", "/api/file_storage/upload/complete", json=complete_data
        )
        if not complete_result.get("success"):
            yield {
                "event": "error",
                "percentage": 100,
                "total_chunks": total_chunks,
                "remaining_chunks": 0,
                "total_bytes": total_size,
                "processed_bytes": total_size,
                "speed": 0,
                "message": complete_result.get("message", "完成上传失败"),
                "success": False,
            }
            return

        total_duration = max(time.perf_counter() - upload_start, 1e-6)
        yield {
            "event": "complete",
            "percentage": 100,
            "total_chunks": total_chunks,
            "remaining_chunks": 0,
            "total_bytes": total_size,
            "processed_bytes": total_size,
            "speed": total_size / total_duration if total_duration else 0,
            "message": complete_result.get("message", "上传完成"),
            "success": True,
            "result": complete_result.get("data", {}),
        }

    async def list_files(
        self,
        remote_path: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """
        获取文件列表
        
        查询指定路径下的文件和文件夹列表，支持分页查询。
        可以查询根目录、指定文件夹或指定文件的信息。
        
        Args:
            remote_path (Optional[str]): 目标路径，可选。可能的值：
                - None: 查询根目录
                - "folder1": 查询folder1文件夹下的内容
                - "folder1/folder2": 查询folder1/folder2文件夹下的内容
                - "file.txt": 查询file.txt文件的信息（如果存在）
            page (int): 页码，从1开始，默认为1
            page_size (int): 每页返回的文件数量，默认为50，最大建议不超过100
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 查询是否成功
                - data (Dict[str, Any]): 查询结果数据，包含：
                    - data (List[Dict]): 文件列表，每个文件/文件夹包含：
                        - id (int): 文件/文件夹ID
                        - file_name (str): 文件名或文件夹名
                        - file_size (int): 文件大小（字节），文件夹为None
                        - file_type (str): 文件MIME类型，文件夹为None
                        - is_folder (bool): 是否为文件夹
                        - is_public (bool): 是否为公共文件
                        - parent_id (int): 父文件夹ID，根目录为None
                        - created_at (str): 创建时间
                        - updated_at (str): 更新时间
                    - total (int): 总文件数量
                    - page (int): 当前页码
                    - page_size (int): 每页数量
                    - namespace (str): 命名空间
                - message (str): 响应消息
        
        Raises:
            RuntimeError: 如果获取命名空间失败
            aiohttp.ClientError: 如果网络请求失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 查询根目录
            result = await manager.list_files()
            if result["success"]:
                files = result["data"].get("data", [])
                total = result["data"].get("total", 0)
                print(f"根目录下有 {total} 个文件/文件夹")
                for item in files:
                    if item.get("is_folder"):
                        print(f"[文件夹] {item['file_name']}")
                    else:
                        size_mb = item.get("file_size", 0) / (1024 * 1024)
                        print(f"[文件] {item['file_name']} ({size_mb:.2f} MB)")
            
            # 查询指定文件夹
            folder_result = await manager.list_files(remote_path="documents", page=1, page_size=20)
            if folder_result["success"]:
                files = folder_result["data"].get("data", [])
                print(f"documents文件夹下有 {len(files)} 个项目")
            ```
        
        Note:
            - 如果remote_path指向一个文件，返回该文件的信息
            - 如果remote_path指向一个文件夹，返回该文件夹下的内容列表
            - 如果remote_path不存在，返回404错误
            - 分页从1开始，不是0
        """
        data = {
            "page": page,
            "page_size": page_size,
        }
        if remote_path is not None:
            data["remote_path"] = remote_path
        namespace = await self.get_namespace()
        if namespace:
            data["namespace"] = namespace

        return await self._request(
            "POST", "/api/file_storage/files/list", json=data
        )

    async def delete_file(
        self,
        remote_path: str,
    ) -> Dict[str, Any]:
        """
        删除文件或文件夹
        
        根据云端路径删除指定的文件或文件夹。
        如果删除的是文件夹，会递归删除文件夹内的所有子文件和子文件夹。
        删除操作不可逆，请谨慎操作。
        
        Args:
            remote_path (str): 目标文件/文件夹的云端路径，例如：
                - "file.txt": 删除根目录下的file.txt文件
                - "folder1/file.txt": 删除folder1文件夹下的file.txt文件
                - "folder1": 删除folder1文件夹及其所有内容
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 删除是否成功
                - data (Dict[str, Any]): 删除结果数据（通常为空字典）
                - message (str): 响应消息，成功时为提示信息，失败时为错误描述
        
        Raises:
            RuntimeError: 如果获取命名空间失败
            aiohttp.ClientError: 如果网络请求失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 删除单个文件
            result = await manager.delete_file(remote_path="documents/old_file.pdf")
            if result["success"]:
                print("文件删除成功")
            else:
                print(f"删除失败: {result['message']}")
            
            # 删除整个文件夹（包括所有子文件）
            folder_result = await manager.delete_file(remote_path="temp_folder")
            if folder_result["success"]:
                print("文件夹及其所有内容已删除")
            ```
        
        Note:
            - 删除文件夹会递归删除其所有内容，操作不可逆
            - 删除操作会同时删除OSS中的实际文件
            - 如果文件/文件夹不存在，会返回404错误
            - 根目录不能删除
        """
        payload: Dict[str, Any] = {"remote_path": remote_path}
        namespace = await self.get_namespace()
        if namespace:
            payload["namespace"] = namespace
        return await self._request(
            "POST",
            "/api/file_storage/files/delete_by_path",
            json=payload,
        )

    async def download(
        self,
        remote_path: str,
        save_path: str,
    ) -> Dict[str, Any]:
        """
        从云端下载文件到本地
        
        此方法封装了完整的下载流程，包括：
        1. 生成下载签名URL
        2. 下载文件数据
        3. 保存到本地路径
        
        如果save_path的目录不存在，会自动创建。
        
        Args:
            remote_path (str): 文件在云端的路径，例如："documents/file.pdf"
            save_path (str): 本地保存路径，例如："/local/path/downloaded_file.pdf"
                如果目录不存在，会自动创建
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 下载是否成功
                - data (Dict[str, Any]): 下载结果数据，成功时包含：
                    - total_size (int): 下载的文件大小（字节）
                    - success (bool): 是否成功
                - message (str): 响应消息，成功时为提示信息，失败时为错误描述
        
        Raises:
            RuntimeError: 如果获取命名空间失败或路径解析失败
            aiohttp.ClientError: 如果网络请求失败
            OSError: 如果本地文件系统操作失败（如权限不足、磁盘空间不足）
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 下载文件
            result = await manager.download(
                remote_path="documents/report.pdf",
                save_path="/local/downloads/report.pdf"
            )
            
            if result["success"]:
                size_mb = result["data"].get("total_size", 0) / (1024 * 1024)
                print(f"下载成功，文件大小: {size_mb:.2f} MB")
            else:
                print(f"下载失败: {result['message']}")
            ```
        
        Note:
            - 只支持下载文件，不支持下载文件夹
            - 如果本地文件已存在，会被覆盖
            - 下载大文件时会自动使用分块下载
            - 签名URL有过期时间（默认1小时），如果下载时间过长可能失败
        """
        final_result: Dict[str, Any] = {}
        error_message = "下载失败"
        async for progress in self.download_stream(remote_path, save_path):
            event = progress.get("event")
            if event == "error":
                return {
                    "success": False,
                    "data": {},
                    "message": progress.get("message", "下载失败"),
                }
            if event == "complete" and progress.get("success"):
                final_result = progress.get("result", {})
                return {
                    "success": True,
                    "data": final_result,
                    "message": progress.get("message", "下载成功"),
                }
        return {
            "success": False,
            "data": {},
            "message": error_message,
        }

    async def download_stream(
        self,
        remote_path: str,
        save_path: str,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        下载文件（流式，返回异步生成器，包含实时进度信息）
        
        此方法是download方法的流式版本，通过异步生成器实时返回下载进度。
        适用于需要显示下载进度条或需要处理大文件的场景。
        
        Args:
            remote_path (str): 文件在云端的路径，例如："documents/file.pdf"
            save_path (str): 本地保存路径，例如："/local/path/downloaded_file.pdf"
                如果目录不存在，会自动创建
        
        Yields:
            Dict[str, Any]: 进度信息字典，包含以下字段：
                - event (str): 事件类型，可能的值：
                    - "init": 初始化完成，开始下载
                    - "chunk": 单个分片下载完成
                    - "complete": 文件下载完成
                    - "error": 下载失败
                - percentage (float): 下载进度百分比（0-100）
                - total_chunks (int): 总分片数（估算值）
                - remaining_chunks (int): 剩余分片数
                - total_bytes (int): 文件总大小（字节），如果未知则为0
                - processed_bytes (int): 已下载字节数
                - chunk_index (int): 当前分片索引（仅chunk事件）
                - chunk_size (int): 当前分片大小（仅chunk事件）
                - speed (float): 当前下载速度（字节/秒）
                - message (str): 进度消息
                - success (bool): 是否成功
                - result (Dict): 完成时的结果数据（仅complete事件）
        
        Raises:
            RuntimeError: 如果获取命名空间失败或路径解析失败
            aiohttp.ClientError: 如果网络请求失败
            OSError: 如果本地文件系统操作失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            async for progress in manager.download_stream(
                remote_path="videos/big_video.mp4",
                save_path="/local/downloads/video.mp4"
            ):
                event = progress.get("event")
                percentage = progress.get("percentage", 0)
                
                if event == "init":
                    total_mb = progress.get("total_bytes", 0) / (1024 * 1024)
                    print(f"开始下载，文件大小: {total_mb:.2f} MB")
                elif event == "chunk":
                    speed_mbps = progress.get("speed", 0) / (1024 * 1024)
                    print(f"进度: {percentage:.1f}% | 速度: {speed_mbps:.2f} MB/s")
                elif event == "complete":
                    print("下载完成！")
                    total_size = progress.get("result", {}).get("total_size", 0)
                    print(f"文件大小: {total_size / (1024*1024):.2f} MB")
                elif event == "error":
                    print(f"下载失败: {progress.get('message')}")
                    break
            ```
        
        Note:
            - 下载时会自动分块处理，每块约2MB
            - 如果文件大小未知，total_bytes可能为0
            - 签名URL有过期时间，长时间下载可能失败
        """
        chunk_size = 2 * 1024 * 1024
        signed_url_response = await self._request(
            "POST",
            "/api/file_storage/files/download_by_path",
            json={"file_path": remote_path},
        )
        if not signed_url_response.get("success"):
            yield {
                "event": "error",
                "percentage": 0,
                "total_chunks": 0,
                "remaining_chunks": 0,
                "total_bytes": 0,
                "processed_bytes": 0,
                "speed": 0,
                "message": signed_url_response.get("message", "生成签名URL失败"),
                "success": False,
            }
            return

        signed_url_data = signed_url_response.get("data", {})
        signed_url = signed_url_data.get("signed_url")
        file_record = signed_url_data.get("file_record", {}) or {}
        total_size = file_record.get("file_size", 0) or 0

        if not signed_url:
            yield {
                "event": "error",
                "percentage": 0,
                "total_chunks": 0,
                "remaining_chunks": 0,
                "total_bytes": total_size,
                "processed_bytes": 0,
                "speed": 0,
                "message": "签名URL为空",
                "success": False,
            }
            return

        total_chunks = math.ceil(total_size / chunk_size) if total_size else 0

        yield {
            "event": "init",
            "percentage": 0,
            "total_chunks": total_chunks,
            "remaining_chunks": total_chunks,
            "total_bytes": total_size,
            "processed_bytes": 0,
            "speed": 0,
            "message": "开始下载文件",
            "success": True,
        }

        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

        downloaded_bytes = 0
        chunk_index = 0
        download_start = time.perf_counter()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(signed_url) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"文件下载失败，状态码：{resp.status}")

                    header_size = resp.headers.get("Content-Length")
                    if total_size == 0 and header_size:
                        try:
                            total_size = int(header_size)
                            total_chunks = (
                                math.ceil(total_size / chunk_size) if total_size else 0
                            )
                        except ValueError:
                            total_size = 0

                    with open(save_path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(chunk_size):
                            chunk_start = time.perf_counter()
                            chunk_index += 1
                            downloaded_bytes += len(chunk)
                            f.write(chunk)

                            chunk_duration = max(
                                time.perf_counter() - chunk_start, 1e-6
                            )
                            instant_speed = len(chunk) / chunk_duration
                            percentage = (
                                0
                                if total_size == 0
                                else min((downloaded_bytes / total_size) * 100, 100)
                            )
                            remaining = (
                                max(total_chunks - chunk_index, 0)
                                if total_chunks
                                else 0
                            )

                            yield {
                                "event": "chunk",
                                "percentage": percentage,
                                "total_chunks": total_chunks,
                                "remaining_chunks": remaining,
                                "total_bytes": total_size,
                                "processed_bytes": downloaded_bytes,
                                "chunk_index": chunk_index - 1,
                                "chunk_size": len(chunk),
                                "speed": instant_speed,
                                "message": f"分片{chunk_index}/{total_chunks or '?'}下载完成",
                                "success": True,
                            }
            except Exception as exc:
                yield {
                    "event": "error",
                    "percentage": 0,
                    "total_chunks": total_chunks,
                    "remaining_chunks": total_chunks,
                    "total_bytes": total_size,
                    "processed_bytes": downloaded_bytes,
                    "speed": 0,
                    "message": f"下载过程中发生错误：{exc}",
                    "success": False,
                }
                return

        total_duration = max(time.perf_counter() - download_start, 1e-6)
        result = {
            "total_size": total_size,
            "success": True,
        }
        yield {
            "event": "complete",
            "percentage": 100,
            "total_chunks": total_chunks,
            "remaining_chunks": 0,
            "total_bytes": total_size,
            "processed_bytes": total_size if total_size else downloaded_bytes,
            "speed": (total_size or downloaded_bytes) / max(total_duration, 1e-6),
            "message": "下载完成",
            "success": True,
            "result": result,
        }

    async def get_traffic_details(
        self,
        remote_path: Optional[str] = None,
        days: int = 30,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        获取流量统计详情
        
        查询指定路径下的文件流量使用情况，支持按时间范围和路径过滤。
        可以查询单个文件、文件夹或路径前缀的流量统计。
        
        Args:
            remote_path (Optional[str]): 远端路径过滤，可选。可能的值：
                - None: 查询所有文件的流量
                - "folder1": 查询folder1文件夹下所有文件的流量（前缀匹配）
                - "folder1/file.txt": 查询特定文件的流量（精确匹配）
            days (int): 查询最近天数，默认30天。仅在未提供start_date和end_date时生效。
                范围：1-90天
            start_date (Optional[str]): 开始日期，格式："YYYY-MM-DD"，例如："2024-01-01"
                必须与end_date同时提供，不能单独使用
            end_date (Optional[str]): 结束日期，格式："YYYY-MM-DD"，例如："2024-01-31"
                必须与start_date同时提供，不能单独使用
                日期范围最长90天
            page (int): 页码，从1开始，默认为1
            page_size (int): 每页返回的记录数量，默认为20
        
        Returns:
            Dict[str, Any]: 统一格式的响应字典，包含以下字段：
                - success (bool): 查询是否成功
                - data (Dict[str, Any]): 流量统计数据，包含：
                    - totals (Dict): 总计流量，包含：
                        - upload_bytes (int): 总上传流量（字节）
                        - download_bytes (int): 总下载流量（字节）
                    - items (List[Dict]): 流量详情列表，每个项目包含：
                        - file_record_id (int): 文件记录ID（可选）
                        - file_name (str): 文件名（可选）
                        - oss_path (str): OSS路径（可选）
                        - remote_path (str): 云端路径（可选）
                        - upload_bytes (int): 上传流量（字节）
                        - download_bytes (int): 下载流量（字节）
                        - total_bytes (int): 总流量（字节）
                        - first_seen (str): 首次访问时间（可选）
                        - last_seen (str): 最后访问时间（可选）
                    - meta (Dict): 分页信息，包含：
                        - page (int): 当前页码
                        - page_size (int): 每页数量
                        - total (int): 总记录数
                    - range_days (int): 查询的天数范围
                    - start_date (str): 查询开始日期
                    - end_date (str): 查询结束日期
                    - namespace (str): 命名空间
                    - filters (Dict): 过滤条件，包含：
                        - remote_path (str): 过滤的路径（可选）
                        - match_mode (str): 匹配模式："exact"（精确）或"prefix"（前缀）
                - message (str): 响应消息
        
        Raises:
            RuntimeError: 如果获取命名空间失败或参数验证失败
            aiohttp.ClientError: 如果网络请求失败
        
        Example:
            ```python
            manager = FileStorageManagerAsync(api_key="your-api-key")
            
            # 查询最近30天的所有流量
            result = await manager.get_traffic_details()
            if result["success"]:
                data = result["data"]
                totals = data.get("totals", {})
                upload_gb = totals.get("upload_bytes", 0) / (1024 ** 3)
                download_gb = totals.get("download_bytes", 0) / (1024 ** 3)
                print(f"上传流量: {upload_gb:.2f} GB")
                print(f"下载流量: {download_gb:.2f} GB")
            
            # 查询指定文件夹的流量（最近7天）
            folder_result = await manager.get_traffic_details(
                remote_path="videos",
                days=7
            )
            if folder_result["success"]:
                items = folder_result["data"].get("items", [])
                for item in items:
                    file_name = item.get("file_name", "未知")
                    total_mb = item.get("total_bytes", 0) / (1024 * 1024)
                    print(f"{file_name}: {total_mb:.2f} MB")
            
            # 查询指定日期范围的流量
            date_result = await manager.get_traffic_details(
                start_date="2024-01-01",
                end_date="2024-01-31",
                page=1,
                page_size=50
            )
            ```
        
        Note:
            - 如果提供start_date和end_date，days参数会被忽略
            - start_date和end_date必须同时提供，不能单独使用
            - 日期范围不能超过90天
            - 如果remote_path以"/"结尾，会进行前缀匹配
            - 流量统计仅记录已完成的下载和上传操作
        """
        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "days": days,
        }
        if remote_path is not None:
            params["remote_path"] = remote_path
        if start_date and end_date:
            params["start_date"] = start_date
            params["end_date"] = end_date
        elif start_date or end_date:
            return {
                "success": False,
                "data": {},
                "message": "start_date 与 end_date 需同时提供",
            }

        return await self._request(
            "GET",
            "/api/file_storage/traffic/details",
            params=params,
        )
