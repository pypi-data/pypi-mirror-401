import os
import uuid
from typing import Union

from loguru import logger

from .workflow_io import parse_workflow_io

try:
    import execution
    from server import PromptServer
except ImportError:
    logger.error(
        "Failed to import ComfyUI server modules, ensure PYTHONPATH is set correctly. (export PYTHONPATH=$PYTHONPATH:/path/to/ComfyUI)"
    )
    exit(1)
import aiohttp
from aiohttp import web

from .env import BIZYDRAFT_SERVER
from .resp import ErrResponse, JsonResponse, OKResponse

_API_PREFIX = "bizyair"
_SERVER_MODE_HC_FLAG = True

BIZYAIR_MAGIC_STRING = os.getenv("BIZYAIR_MAGIC_STRING", "QtDtsxAc8JI1bTb7")
# 整个HTTP请求的总时间限制
HTTP_CLIENT_TOTAL_TIMEOUT = int(os.getenv("HTTP_CLIENT_TOTAL_TIMEOUT", 300))
# 建立TCP连接的时间限制
HTTP_CLIENT_CONNECT_TIMEOUT = int(os.getenv("HTTP_CLIENT_CONNECT_TIMEOUT", 50))
# HTTP客户端连接池设置
HTTP_CLIENT_LIMIT = int(os.getenv("HTTP_CLIENT_LIMIT", 100))
# 每个主机最大连接数
HTTP_CLIENT_LIMIT_PER_HOST = int(os.getenv("HTTP_CLIENT_LIMIT_PER_HOST", 50))
# DNS缓存时间(秒)
HTTP_CLIENT_DNS_TTL = int(os.getenv("HTTP_CLIENT_DNS_TTL", 300))
# 连接保持超时(秒)
HTTP_CLIENT_KEEPALIVE_TIMEOUT = int(os.getenv("HTTP_CLIENT_KEEPALIVE_TIMEOUT", 30))

if BIZYAIR_MAGIC_STRING == "QtDtsxAc8JI1bTb7":
    logger.warning(
        "BIZYAIR_MAGIC_STRING is not set, using default value. This is insecure and should be changed in production!"
    )


class BizyDraftServer:
    def __init__(self):
        BizyDraftServer.instance = self
        self.prompt_server = PromptServer.instance
        self.session = None  # 复用客户端会话
        self.setup_routes()

    def _get_auth_header(self, request):
        """从请求中提取 Authorization 头"""
        auth_header = request.headers.get("Authorization", "")
        return auth_header

    def _get_session(self):
        """获取或创建客户端会话"""
        if self.session is None or self.session.closed:
            # 配置连接超时和连接池限制
            timeout = aiohttp.ClientTimeout(
                total=HTTP_CLIENT_TOTAL_TIMEOUT, connect=HTTP_CLIENT_CONNECT_TIMEOUT
            )
            connector = aiohttp.TCPConnector(
                limit=HTTP_CLIENT_LIMIT,
                limit_per_host=HTTP_CLIENT_LIMIT_PER_HOST,
                ttl_dns_cache=HTTP_CLIENT_DNS_TTL,
                use_dns_cache=True,
                keepalive_timeout=HTTP_CLIENT_KEEPALIVE_TIMEOUT,
            )
            self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self.session

    def setup_routes(self):
        @self.prompt_server.routes.get(f"/{_API_PREFIX}/are_you_alive")
        async def are_you_alive(request) -> Union[OKResponse, ErrResponse]:
            if _SERVER_MODE_HC_FLAG:
                return OKResponse()
            return ErrResponse(500)

        @self.prompt_server.routes.post(
            f"/{_API_PREFIX}/are_you_alive_{BIZYAIR_MAGIC_STRING}"
        )
        async def toggle_are_you_alive(request) -> OKResponse:
            global _SERVER_MODE_HC_FLAG
            _SERVER_MODE_HC_FLAG = not _SERVER_MODE_HC_FLAG
            return OKResponse()

        @self.prompt_server.routes.post(f"/{_API_PREFIX}/workflow_io")
        async def workflow_io(request) -> Union[JsonResponse, ErrResponse]:
            try:
                data = await request.json()
            except Exception as e:
                logger.error(f"解析 request.json() 失败: {e}")
                return ErrResponse(400)
            try:
                response = parse_workflow_io(data)
                return JsonResponse(200, response)
            except Exception as e:
                logger.error(f"parse_workflow_io 处理失败: {e}")
                return ErrResponse(500)

        @self.prompt_server.routes.post(f"/{_API_PREFIX}/workflow_valid")
        async def workflow_valid(request):
            logger.info("got workflow_valid request")
            json_data = await request.json()
            json_data = self.prompt_server.trigger_on_prompt(json_data)

            if "prompt" in json_data:
                prompt = json_data["prompt"]
                prompt_id = str(json_data.get("prompt_id", uuid.uuid4()))

                partial_execution_targets = None
                if "partial_execution_targets" in json_data:
                    partial_execution_targets = json_data["partial_execution_targets"]

                valid = await execution.validate_prompt(
                    prompt_id, prompt, partial_execution_targets
                )
                extra_data = {}
                if "extra_data" in json_data:
                    extra_data = json_data["extra_data"]

                if "client_id" in json_data:
                    extra_data["client_id"] = json_data["client_id"]
                if valid[0]:
                    sensitive = {}
                    for sensitive_val in execution.SENSITIVE_EXTRA_DATA_KEYS:
                        if sensitive_val in extra_data:
                            sensitive[sensitive_val] = extra_data.pop(sensitive_val)
                    response = {
                        "prompt_id": prompt_id,
                        "node_errors": valid[3],
                    }
                    return web.json_response(response)
                else:
                    logger.warning("invalid prompt: {}".format(valid[1]))
                    return web.json_response(
                        {"error": valid[1], "node_errors": valid[3]}, status=400
                    )
            else:
                error = {
                    "type": "no_prompt",
                    "message": "No prompt provided",
                    "details": "No prompt provided",
                    "extra_info": {},
                }
                return web.json_response(
                    {"error": error, "node_errors": {}}, status=400
                )

        @self.prompt_server.routes.get(f"/{_API_PREFIX}/commit_input_resource")
        async def get_input_resource(request) -> Union[JsonResponse, ErrResponse]:
            """
            获取输入资源列表
            查询参数:
                - url: 资源URL
                - ext: 文件扩展名
                - current: 当前页码
                - page_size: 每页大小
            """
            try:
                # 获取查询参数
                url_arg = request.query.get("url", "")
                ext = request.query.get("ext", "")
                current = request.query.get("current", "1")
                page_size = request.query.get("page_size", "10")

                # 获取认证头
                auth_header = self._get_auth_header(request)
                print("get_input_resource auth_header:", auth_header)
                # 构建后端API URL
                backend_url = f"{BIZYDRAFT_SERVER}/input_resource"
                params = {
                    "url": url_arg,
                    "ext": ext,
                    "current": current,
                    "page_size": page_size,
                }

                # 请求后端API
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": auth_header,
                }

                session = self._get_session()
                async with session.get(
                    backend_url, params=params, headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return JsonResponse(200, {"code": 20000, "data": data})
                    else:
                        error_text = await resp.text()
                        logger.error(f"获取输入资源失败: {resp.status} - {error_text}")
                        return ErrResponse(
                            resp.status, f"获取输入资源失败: {error_text}"
                        )

            except Exception as e:
                logger.error(f"get_input_resource 处理失败: {e}")
                return ErrResponse(500)

        @self.prompt_server.routes.post(f"/{_API_PREFIX}/commit_input_resource")
        async def commit_input_resource(request) -> Union[JsonResponse, ErrResponse]:
            """
            提交输入资源
            请求体: JSON 格式的资源数据
            """
            try:
                # 解析请求体
                data = await request.json()
            except Exception as e:
                logger.error(f"解析 request.json() 失败: {e}")
                return ErrResponse(400)

            try:
                # 获取认证头
                auth_header = self._get_auth_header(request)

                # 构建后端API URL
                backend_url = f"{BIZYDRAFT_SERVER}/input_resource/commit"

                # 请求后端API
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": auth_header,
                }

                session = self._get_session()
                async with session.post(
                    backend_url, json=data, headers=headers
                ) as resp:
                    if resp.status == 200:
                        response_data = await resp.json()
                        return JsonResponse(
                            200, {"success": True, "data": response_data}
                        )
                    else:
                        error_text = await resp.text()
                        logger.error(f"提交输入资源失败: {resp.status} - {error_text}")
                        return ErrResponse(
                            resp.status, f"提交输入资源失败: {error_text}"
                        )

            except Exception as e:
                logger.error(f"commit_input_resource 处理失败: {e}")
                return ErrResponse(500)

        @self.prompt_server.routes.get(f"/{_API_PREFIX}/upload_token")
        async def get_upload_token(request) -> Union[JsonResponse, ErrResponse]:
            """
            获取上传凭证
            查询参数:
                - file_name: 文件名
                - file_type: 文件类型 (如: inputs)
            """
            try:
                # 获取查询参数
                file_name = request.query.get("file_name", "")
                file_type = request.query.get("file_type", "")

                if not file_name:
                    logger.error("file_name 参数缺失")
                    return ErrResponse(400)

                # 获取认证头
                auth_header = self._get_auth_header(request)

                # 构建后端API URL
                from urllib.parse import quote

                encoded_filename = quote(file_name, safe="")
                backend_url = f"{BIZYDRAFT_SERVER}/upload/token?file_name={encoded_filename}&file_type={file_type}"

                # 请求后端API
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": auth_header,
                }

                session = self._get_session()
                async with session.get(backend_url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return JsonResponse(200, {"code": 20000, "data": data})
                    else:
                        error_text = await resp.text()
                        logger.error(f"获取上传凭证失败: {resp.status} - {error_text}")
                        return ErrResponse(
                            resp.status, f"获取上传凭证失败: {error_text}"
                        )

            except Exception as e:
                logger.error(f"get_upload_token 处理失败: {e}")
                return ErrResponse(500)
