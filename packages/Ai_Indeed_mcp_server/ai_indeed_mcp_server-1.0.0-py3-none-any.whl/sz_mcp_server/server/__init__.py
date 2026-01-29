from typing import List
from mcp.server.fastmcp import FastMCP

from . import local_tools
from . import utils
from ..log import log

# Initialize FastMCP server
mcp = FastMCP("sz_mcp_server")

    
@mcp.tool(name="queryAppParam", description="当用户询问某个流程包的详细信息时使用此工具")
def get_package_info(request: utils.QueryAppParamRequest) -> List[utils.QueryAppParamResponse]:
    filters = {
        "name": request.name if request.name else "",
        "flowId": request.flowId if request.flowId else "",
        "version": request.version if request.version else "",
        "desc": request.desc if request.desc else "",
        "runtimeVersion": request.runtimeVersion if request.runtimeVersion else ""
    }

    active_filters = {k: v for k, v in filters.items() if v is not None and v != ""}

    pkgs_data = utils.get_flows(active_filters)["data"]
    pkgs_data = [utils.QueryAppParamResponse(**pkg) for pkg in pkgs_data]
    filtered_packages = [
        package for package in pkgs_data
        if package.matches_filters(**active_filters)
    ]

    filtered_packages = [pkg.model_dump() for pkg in filtered_packages]

    return filtered_packages


@mcp.tool(name="queryAppList", description="当用户询问全部流程时使用此工具")
def get_package_info_list() -> List[utils.QueryAppParamResponse]:
    pkgs_data = utils.get_flows({})["data"]
    return [utils.QueryAppParamResponse(**pkg) for pkg in pkgs_data]


@mcp.tool(name="queryTaskList", description="当用户询问全部任务时使用此工具")
def get_task_list() -> List[utils.queryTaskListResponse]:
    tasks = utils.get_tasks()["data"]
    return  [utils.queryTaskListResponse(**task).model_dump() for task in tasks]


@mcp.tool(name="runApp", description="当用户要求执行流程时使用此工具")
def start_flow(request: utils.RunFlowRequest) -> str:
    bot_data = utils.check_bot_status()
    if bot_data["code"] != "0":
        return bot_data["message"]
    else:
        ret = utils.run_flow(request.model_dump())
        if ret.get("code") == "0":
            return f"{ret['data']['jobName']} {ret['data']['jobId']} 流程开始执行..."
        else:
            return f" {ret['data']}"


@mcp.tool(name="startTask", description="当用户要求执行任务时使用此工具")
def start_task(request: utils.RunTaskRequest)-> str:
    bot_data = utils.check_bot_status()
    if bot_data["code"] != "0":
        return bot_data["message"]
    else:
        ret = utils.run_task(request.model_dump())
        if ret.get("code") == "0":
            return f"{ret['data']['jobName']} {ret['data']['jobId']} 任务开始执行..."
        else:
            return f"{ret['data']}"


@mcp.tool(name="createTask", description="当用户要求创建任务时使用此工具")
def create_task(request: utils.CreateTaskRequest)-> str:
    bot_data = utils.check_bot_status()
    if bot_data["code"] != "0":
        return bot_data["message"]
    else:
        ret = utils.create_tasks(request.model_dump())
        if ret.get("code") == "0":
            return f"{ret['data']['taskName']} {ret['data']['taskId']} 任务创建成功..."
        else:
            return f"{ret['data']}"


__all__ = ["mcp", "local_tools"]