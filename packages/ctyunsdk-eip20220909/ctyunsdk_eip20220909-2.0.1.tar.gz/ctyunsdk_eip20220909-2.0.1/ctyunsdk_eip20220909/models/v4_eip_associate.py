from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4EipAssociateRequest(CtyunOpenAPIRequest):
    clientToken: str  # 客户端存根，用于保证订单幂等性, 长度 1 - 64
    regionID: str  # 资源池 ID
    eipID: str  # 绑定云产品实例的 EIP 的 ID
    associationID: str  # 绑定的实例的 ID
    associationType: int  # 绑定的实例类型：1 ECS 云主机 VM，2 VIP, 3 BM, 4 成员网卡
    projectID: Optional[str] = None  # 企业项目 ID，默认为"0"

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipAssociateResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional[object] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


