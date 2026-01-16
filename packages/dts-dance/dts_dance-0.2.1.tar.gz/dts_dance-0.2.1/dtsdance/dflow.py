from typing import Any, cast, Optional
from loguru import logger
from .bytecloud import ByteCloudClient
import requests


class TaskNotFound(Exception):
    pass


class DFlowNotFound(Exception):
    pass


class DFlowClient:

    def __init__(self, bytecloud_client: ByteCloudClient) -> None:
        self.bytecloud_client = bytecloud_client

    def _make_request(self, method: str, url: str, headers: dict[str, str], json_data: Optional[dict] = None) -> dict[str, Any]:
        """
        发送 HTTP 请求的通用方法

        Args:
            method: HTTP 方法 (GET/POST)
            url: 请求 URL
            headers: 请求头
            json_data: POST 请求的 JSON 数据

        Returns:
            dict[str, Any]: 解析后的 JSON 响应
        """
        response = None
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=json_data, headers=headers)
            else:
                raise ValueError(f"不支持的 HTTP 方法: {method}")

            # 检查响应状态码
            response.raise_for_status()

            # 解析 JSON 响应
            return response.json()

        except Exception as e:
            error_msg = f"_make_request occur error, error: {e}"
            if response is not None:
                error_msg += f", response.text: {response.text}"
            logger.warning(error_msg)
            raise

    def get_task_info(self, site: str, task_id: str) -> dict[str, Any]:
        """
        获取 DFlow 任务信息

        Args:
            site: 站点名称
            task_id: DFlow 任务 ID

        Returns:
            dict[str, Any]: DFlow 任务信息，包含 create_time 等字段
        """
        # 构建 API URL
        site_info = self.bytecloud_client.get_site_info(site)
        url = f"{site_info.endpoint}/api/v1/bytedts/api/bytedts/v3/DescribeTaskInfo"

        # 构建请求数据
        json_data = {"id": int(task_id)}

        response_data = self._make_request("POST", url, self.bytecloud_client.build_request_headers(site), json_data)

        message = response_data.get("message")
        # logger.debug(f"get_task_info {site} {task_id}, message: {message}")

        if message == "task not exists":
            raise TaskNotFound(f"获取 DFlow 任务信息失败，站点: {site}, 任务 ID: {task_id} 不存在")

        try:
            data = cast(dict, response_data.get("data", {}))
            task = cast(dict, data.get("task", {}))
            # 提取核心信息
            filtered_data = {
                "task_id": task.get("id", ""),
                "status": task.get("status", ""),
                "desc": task.get("desc", ""),
                "create_time": task.get("create_time", 0),
            }

            return filtered_data

        except (KeyError, AttributeError, Exception) as e:
            raise Exception(f"无法从响应中提取 DFlow 任务信息数据: {str(e)}")

    def get_dflow_info(self, site: str, dflow_id: str) -> dict[str, Any]:
        """
        获取 DFlow 进程信息

        Args:
            site: 站点名称
            dflow_id: DFlow 进程 ID

        Returns:
            dict[str, Any]: DFlow 进程信息，包含 create_time 等字段
        """
        # 构建 API URL
        site_info = self.bytecloud_client.get_site_info(site)
        url = f"{site_info.endpoint}/api/v1/bytedts/api/bytedts/v3/DescribeDFlowDetail"

        # 构建请求数据
        json_data = {"dflow_id": int(dflow_id)}

        response_data = self._make_request("POST", url, self.bytecloud_client.build_request_headers(site), json_data)

        message = response_data.get("message", "")
        # logger.debug(f"get_dflow_info {site} {dflow_id}, message: {message}")

        if "dflow not found" in message:
            raise DFlowNotFound(f"获取 DFlow 进程信息失败，站点: {site}, 进程 ID: {dflow_id} 不存在")

        try:
            data = cast(dict, response_data.get("data", {}))
            dflow = cast(dict, data.get("dflow", {}))
            # 提取核心信息
            filtered_data = {
                "dflow_id": dflow.get("id", ""),
                "task_id": dflow.get("task_id", ""),
                "app": dflow.get("app", ""),
                "schedule_plan_name": dflow.get("schedule_plan_name", ""),
                "running_state.healthy_status": dflow.get("running_state", {}).get("healthy_status", ""),
            }

            return filtered_data

        except (KeyError, AttributeError, Exception) as e:
            raise Exception(f"无法从响应中提取 DFlow 进程信息数据: {str(e)}")

    def generate_task_url(self, site: str, task_id: str) -> str:
        """
        获取 DFlow 任务详情页面的 URL

        Args:
            site: 站点名称
            task_id: DFlow 任务 ID

        Returns:
            str: DFlow 任务详情页面的 URL
        """
        # 根据环境生成对应的 scope 参数
        site_info = self.bytecloud_client.get_site_info(site)
        return f"{site_info.endpoint}/bytedts/datasync/detail/{task_id}?scope={site}"

    def init_resources(self, site: str, ctrl_env: str) -> bool:
        """
        初始化 CTRL 环境资源

        Args:
            site: 站点名称
            ctrl_env: 控制环境

        Returns:
            bool: CTRL 环境资源初始化结果
        """
        # 构建 API URL
        site_info = self.bytecloud_client.get_site_info(site)
        url = f"{site_info.endpoint}/api/v1/bytedts/api/bytedts/v3/InitSystemResource"

        # 构建请求数据
        json_data = {"ctrl_env": ctrl_env}

        response_data = self._make_request("POST", url, self.bytecloud_client.build_request_headers(site), json_data)

        message = response_data.get("message")
        logger.info(f"int_resources {site} {ctrl_env}, message: {message}")

        return message == "ok"

    def list_resources(self, site: str, ctrl_env: str) -> list[str]:
        """
        列举 CTRL 环境资源列表

        Args:
            site: 站点名称
            ctrl_env: 控制环境

        Returns:
            list[str]: CTRL 环境资源列表
        """
        # 构建 API URL
        site_info = self.bytecloud_client.get_site_info(site)
        url = f"{site_info.endpoint}/api/v1/bytedts/api/bytedts/v3/DescribeResources"

        # 构建请求数据
        json_data = {"offset": 0, "limit": 10, "ctrl_env": ctrl_env}

        response_data = self._make_request("POST", url, self.bytecloud_client.build_request_headers(site), json_data)

        try:
            data = cast(dict, response_data.get("data", {}))
            items = cast(list, data.get("items", []))
            return [item["name"] for item in items]
        except (KeyError, AttributeError, Exception) as e:
            raise Exception(f"无法从响应中提取 CTRL 环境资源列表数据: {str(e)}")
