import os
from typing import Optional, Union, List, Dict, Any, Required
from pydantic import BaseModel, Field, model_validator
from urllib.parse import urlencode, quote
import subprocess

import httpx

from ..log import log

ROAMING_DIR = os.getenv('APPDATA')

class SzResponse:
    def __init__(self, code: str, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
    
    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


class QueryAppParamRequest(BaseModel):
    name: Optional[str] = Field(None, description="流程名称")
    flowId: Optional[str] = Field(None, description="流程ID")
    version: Optional[str] = Field(None, description="流程包的版本号")
    desc: Optional[str] = Field(None, description="流程包的描述信息")
    runtimeVersion: Optional[str] = Field(None, description="流程ID")

    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_field(cls, values):
        required_fields = ['name', 'flowId', 'version', 'desc', 'runtimeVersion']
        filled_fields = [field for field in required_fields if field in values and values[field] is not None]

        if not filled_fields:
            raise ValueError('必须至少填写 name, flowId, version, desc, runtimeVersion 中的一个字段')

        return values


class QueryAppParamResponse(QueryAppParamRequest):
    paramValue: str = Field(None, description="流程入参，支持字符串、数字、布尔值、列表等")

    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_field(cls, values):
        return values

    def matches_filters(self, **filters):
        """检查对象是否匹配给定的过滤条件"""
        for field, value in filters.items():
            if value is not None and value != "":
                field_value = getattr(self, field, "")
                if isinstance(field_value, str) and isinstance(value, str):
                    if value.lower() not in field_value.lower():
                        return False
                else:
                    if value != field_value:
                        return False
        return True

    class Config:
        extra = "ignore"


class queryTaskListResponse(BaseModel):
    taskId: Optional[str] = Field(..., description="任务ID")
    taskName: Optional[str] = Field(..., description="任务名称")
    flowInfos: List[QueryAppParamResponse] = Field(..., description="任务里面的流程信息")

    class Config:
        extra = "ignore"


class RunFlowRequest(BaseModel):
    FlowId: Optional[str] = Field(None, description="流程ID")
    Name: Optional[str] = Field(None, description="任务名")

    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_field(cls, values):
        required_fields = ['FlowId', 'Name']
        filled_fields = [field for field in required_fields if field in values and values[field] is not None]

        if not filled_fields:
            raise ValueError('必须至少填写 FlowId, Name 中的一个字段')

        return values


class RunTaskRequest(BaseModel):
    Id: Optional[str] = Field(None, description="任务ID")
    Name: Optional[str] = Field(None, description="任务名")

    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_field(cls, values):
        required_fields = ['Id', 'Name']
        filled_fields = [field for field in required_fields if field in values and values[field] is not None]

        if not filled_fields:
            raise ValueError('必须至少填写 Id, Name 中的一个字段')

        return values


class CreateTaskRequestFlow(BaseModel):
    FlowId: str = Field(None, description="流程ID")
    Name: str = Field(None, description="任务名")


class CreateTaskRequest(BaseModel):
    TaskName: str = Field(..., description="任务名")
    CronExpressionText: str = Field(..., description="Cron表达式")
    FlowInfos: List[CreateTaskRequestFlow] = Field(..., description="流程信息")


def log_response(response):
    request = response.request
    log.debug(str.lstrip(f""".........................................
                            状态码: {response.status_code}
                            响应体: {response.read()}""")
              )


def get_flows(params):
    log.info(f"get_flows params: {params}")
    query_string = "?size=100"
    name_param = params.get("name")
    if name_param:
        query_string += f"&keyword={quote(name_param)}"
    base_url = "http://127.0.0.1:15000/api/flows/query"
    full_url = base_url + query_string
    with httpx.Client(
        mounts={"http://": None, "https://": None},
        event_hooks={"response": [log_response]}
    ) as client:
        response = client.get(full_url, timeout=60)

    if response.status_code != 200:
        return SzResponse("1", "", []).to_dict()
    else:
        ret = response.json()
        return SzResponse("0", "", ret["data"]["data"]).to_dict()


def get_tasks():
    url = "http://127.0.0.1:15000/api/bottasks/query?size=100&taskType=0"
    with httpx.Client(
        mounts={"http://": None, "https://": None},
        event_hooks={"response": [log_response]}
    ) as client:
        response = client.get(url, timeout=60)

    if response.status_code != 200:
        return SzResponse("1", "", []).to_dict()
    else:
        ret = response.json()
        return SzResponse("0", "", ret["data"]["data"]).to_dict()


def run_flow(params):
    url = "http://127.0.0.1:15000/api/flows/run"
    if not params.get("FlowId"):
        params.pop("FlowId", None)

    with httpx.Client(
        mounts={"http://": None, "https://": None},
        event_hooks={"response": [log_response]}
    ) as client:
        response = client.post(url, json=params, timeout=60)

    if response.status_code != 200:
        return SzResponse("1", "", []).to_dict()
    else:
        ret = response.json()
        if ret.get("isSuccess"):
            return SzResponse("0", "", ret["data"]).to_dict()
        else:
            return SzResponse("1", "", ret["message"]).to_dict()


def run_task(params):
    url = "http://127.0.0.1:15000/api/bottasks/trigger"
    if not params.get("Id"):
        params.pop("Id", None)

    if "Name" in params and params.get("Name") is None:
        params["Name"] = ""

    with httpx.Client(
        mounts={"http://": None, "https://": None},
        event_hooks={"response": [log_response]}
    ) as client:
        response = client.post(url, json=params, timeout=60)

    if response.status_code != 200:
        return SzResponse("1", "", []).to_dict()
    else:
        ret = response.json()
        if ret.get("isSuccess"):
            return SzResponse("0", "", ret["data"]).to_dict()
        else:
            return SzResponse("1", "", ret["message"]).to_dict()


def create_tasks(params):
    url = "http://127.0.0.1:15000/api/bottasks/create"

    with httpx.Client(
            mounts={"http://": None, "https://": None},
            event_hooks={"response": [log_response]}
    ) as client:
        response = client.post(url, json=params, timeout=60)

    if response.status_code != 200:
        return SzResponse("1", "", "任务创建失败!").to_dict()
    else:
        ret = response.json()
        if ret.get("isSuccess"):
            return SzResponse("0", "", ret["data"]).to_dict()
        else:
            return SzResponse("1", "", ret["message"]).to_dict()


def check_bot_status() -> Dict:
    url = "http://127.0.0.1:15000/v1/appstates/status"
    with httpx.Client(
            mounts={"http://": None, "https://": None},
            event_hooks={"response": [log_response]}
    ) as client:
        response = client.get(url, timeout=5)
        
    if response.status_code != 200:
       return SzResponse("2", "机器人状态查询服务异常, 请检查机器人是否正常启动!").to_dict()

    ret = response.json()

    if ret['data']['userStatus'] != 20:
        return SzResponse("3", "机器人未登录!").to_dict()

    if ret['data']['botMode'] != "ByLocal":
        return SzResponse("1", "机器人非单机模式,不能处理流程或任务!").to_dict()

    if ret['isSuccess'] and ret['data']['botStatus'] == 1:
        return SzResponse("0", "机器人已就绪, 可以运行流程!").to_dict()
    else:
        status_text = {
            2: "忙碌"
        }.get(ret['data']['botStatus'], "未知状态")
        return SzResponse("1", f"机器人已登录, 状态: {status_text}, 无法运行流程!").to_dict()


def open_bot(bot_path: str, start_mode: str=None):
    try:
        log.info(f"开始通过 Explorer 启动机器人: {bot_path}")
        abs_path = os.path.abspath(bot_path)
        subprocess.Popen(f'explorer.exe "{abs_path}"', shell=True)
        log.info(f"Explorer 已接管启动任务")
    except Exception as e:
        log.exception(f"通过 Explorer 启动失败: {e}")
