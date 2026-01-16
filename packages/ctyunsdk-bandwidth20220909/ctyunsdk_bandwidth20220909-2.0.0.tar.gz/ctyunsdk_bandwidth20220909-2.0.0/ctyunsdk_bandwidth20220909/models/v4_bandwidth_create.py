from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4BandwidthCreateRequest(CtyunOpenAPIRequest):
    clientToken: str  # 客户端存根，用于保证订单幂等性, 长度 1 - 64
    regionID: str  # 创建共享带宽的区域id。
    bandwidth: int  # 共享带宽的带宽峰值，必须大于等于 5。
    cycleType: str  # 订购类型：包年/包月订购，或按需订购。<br>month / year / on_demand
    cycleCount: int  # 订购时长, 当 cycleType = month, 支持续订 1 - 11 个月; 当 cycleType = year, 支持续订 1 - 3 年
    name: str  # 支持拉丁字母、中文、数字，下划线，连字符，中文 / 英文字母开头，不能以 http: / https: 开头，长度 2 - 32
    projectID: Optional[str] = None  # 企业项目 ID，默认为"0"
    lineType: Optional[str] = None  # 线路类型，默认为163，支持163 / bgp / chinamobile / chinaunicom
    demandBillingType: Optional[str] = None  # 付费类型 包含bandwidth(带宽)/peakbandwidth（月95计费，需要lineType为163,cycleType为on_demand） 默认bandwidth
    payVoucherPrice: Optional[str] = None  # 代金券金额，支持到小数点后两位，仅包周期支持代金券

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4BandwidthCreateResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional['V4BandwidthCreateReturnObj'] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4BandwidthCreateReturnObj:
    masterOrderID: Optional[str] = None  # 订单id。
    masterOrderNO: Optional[str] = None  # 订单编号, 可以为 null。
    masterResourceStatus: Optional[str] = None  # 资源状态: started（启用） / renewed（续订） / refunded（退订） / destroyed（销毁） / failed（失败） / starting（正在启用） / changed（变配）/ expired（过期）/ unknown（未知）
    masterResourceID: Optional[str] = None  # 可以为 null。
    regionID: Optional[str] = None  # 可用区id。
    bandwidthID: Optional[str] = None  # 带宽 ID，当 masterResourceStatus 不为 started, 该值可为 null
