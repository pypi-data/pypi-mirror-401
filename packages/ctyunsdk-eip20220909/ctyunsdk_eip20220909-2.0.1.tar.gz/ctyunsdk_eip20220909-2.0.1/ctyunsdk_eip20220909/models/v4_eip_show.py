from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4EipShowRequest(CtyunOpenAPIRequest):
    regionID: str  # 资源池 ID
    eipID: str  # 弹性公网IP的ID

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipShowResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional['V4EipShowReturnObj'] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipShowReturnObj:
    ID: Optional[str] = None  # eip ID
    name: Optional[str] = None  # eip 名称
    description: Optional[str] = None  # 描述
    eipAddress: Optional[str] = None  # eip 地址
    associationID: Optional[str] = None  # 当前绑定的实例的 ID
    associationType: Optional[str] = None  # 当前绑定的实例类型: LOADBALANCER / INSTANCE / PORTFORWARDING / VIP / PHYSICALINSTANCE / MEMBER_ENI
    privateIpAddress: Optional[str] = None  # 交换机网段内的一个 IP 地址
    bandwidth: Optional[int] = None  # 带宽峰值大小，单位 Mb
    status: Optional[str] = None  # 1\.ACTIVE 2.DOWN 3.ERROR 4.UPDATING 5.BANDING_OR_UNBANGDING 6.DELETING 7.DELETED 8.EXPIRED
    tags: Optional[str] = None  # EIP 的标签集合
    createdAt: Optional[str] = None  # 创建时间
    updatedAt: Optional[str] = None  # 更新时间
    bandwidthID: Optional[str] = None  # 绑定的共享带宽 ID
    bandwidthType: Optional[str] = None  # eip带宽规格：standalone / upflowc
    expiredAt: Optional[str] = None  # 到期时间
    lineType: Optional[str] = None  # 线路类型
    projectID: Optional[str] = None  # 项目ID
    portID: Optional[str] = None  # 绑定的网卡 id
    isPackaged: Optional[bool] = None  # 表示是否与 vm 一起订购
    billingMethod: Optional[str] = None  # 计费类型：periodic 包周期，on_demand 按需
    enableSecondLevelMonitor: Optional[bool] = None  # 是否开启秒级监控
    resourceID: Optional[str] = None  # 资源id
