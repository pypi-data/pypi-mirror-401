from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4EipCreateRequest(CtyunOpenAPIRequest):
    clientToken: str  # 客户端存根，用于保证订单幂等性, 长度 1 - 64
    regionID: str  # 资源池 ID
    cycleType: str  # 订购类型：month（包月） / year（包年） / on_demand（按需）
    cycleCount: int  # 订购时长, 当 cycleType = month, 支持续订 1 - 11 个月; 当 cycleType = year, 支持续订 1 - 3 年, 当 cycleType = on_demand 时，可以不传
    name: str  # 支持拉丁字母、中文、数字，下划线，连字符，中文 / 英文字母开头，不能以 http: / https: 开头，长度 2 - 32
    projectID: Optional[str] = None  # 不填默认为默认企业项目，如果需要指定企业项目，则需要填写
    bandwidth: Optional[int] = None  # 弹性 IP 的带宽峰值，默认为 1 Mbps
    bandwidthID: Optional[str] = None  # 当 cycleType 为 on_demand 时，可以使用 bandwidthID，将弹性 IP 加入到共享带宽中
    demandBillingType: Optional[str] = None  # 按需计费类型，当 cycleType 为 on_demand 时生效，支持 bandwidth（按带宽）/ upflowc（按流量）
    lineType: Optional[str] = None  # 线路类型，默认为163，支持163 / bgp / chinamobile / chinaunicom
    payVoucherPrice: Optional[str] = None  # 代金券金额，支持到小数点后两位，仅包周期支持代金券
    segmentID: Optional[str] = None  # 专属 eip 地址池 segment id
    exclusiveName: Optional[str] = None  # 专属 eip 地址池名字

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipCreateResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional['V4EipCreateReturnObj'] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4EipCreateReturnObj:
    masterOrderID: Optional[str] = None  # 订单id。
    masterOrderNO: Optional[str] = None  # 订单编号, 可以为 null。
    masterResourceStatus: Optional[str] = None  # 资源状态: started（启用） / renewed（续订） / refunded（退订） / destroyed（销毁） / failed（失败） / starting（正在启用） / changed（变配）/ expired（过期）/ unknown（未知）
    masterResourceID: Optional[str] = None  # 可以为 null。
    regionID: Optional[str] = None  # 可用区id。
    eipID: Optional[str] = None  # 弹性 IP id，当 masterResourceStatus 不为 started 时，该值可能为 null
