from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4EipNewListRequest(CtyunOpenAPIRequest):
    clientToken: str  # 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
    regionID: str  # 资源池 ID
    projectID: Optional[str] = None  # 企业项目 ID，默认为"0"
    page: Optional[int] = None  # 分页参数
    pageNo: Optional[int] = None  # 列表的页码，默认值为 1, 推荐使用该字段, page 后续会废弃
    pageSize: Optional[int] = None  # 每页数据量大小，取值 1-50
    ids: Optional[List[str]] = None  # 是 Array 类型，里面的内容是 String
    status: Optional[str] = None  # eip状态 ACTIVE（已绑定）/ DOWN（未绑定）/ FREEZING（已冻结）/ EXPIRED（已过期），不传是查询所有状态的 EIP
    ipType: Optional[str] = None  # ip类型 ipv4 / ipv6
    eipType: Optional[str] = None  # eip类型 normal / cn2
    ip: Optional[str] = None  # 弹性 IP 的 ip 地址
    associationID: Optional[str] = None  # eip 绑定的资源 id

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipNewListResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional['V4EipNewListReturnObj'] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipNewListReturnObj:
    eips: Optional[List['V4EipNewListReturnObjEips']] = None
    totalCount: Optional[int] = None  # 列表条目数
    currentCount: Optional[int] = None  # 分页查询时每页的行数
    totalPage: Optional[int] = None  # 总页数


@dataclass_json
@dataclass
class V4EipNewListReturnObjEips:
    ID: Optional[str] = None
    name: Optional[str] = None
    eipAddress: Optional[str] = None
    description: Optional[str] = None
    associationID: Optional[str] = None
    associationType: Optional[str] = None
    privateIpAddress: Optional[str] = None
    bandwidthID: Optional[str] = None
    bandwidth: Optional[int] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    expiredAt: Optional[str] = None
    projectID: Optional[str] = None
    lineType: Optional[str] = None
    portID: Optional[str] = None
    isPackaged: Optional[bool] = None
    enableSecondLevelMonitor: Optional[bool] = None
    billingMethod: Optional[str] = None
    bandwidthType: Optional[str] = None
    resourceID: Optional[str] = None
