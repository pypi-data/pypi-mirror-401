from typing import Optional, List, Dict

from ctyun_python_sdk_core.ctyun_openapi_request import CtyunOpenAPIRequest
from ctyun_python_sdk_core.ctyun_openapi_response import CtyunOpenAPIResponse
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class V4BandwidthDeleteRequest(CtyunOpenAPIRequest):
    clientToken: str  # 客户端存根，用于保证订单幂等性, 长度 1 - 64
    regionID: str  # 共享带宽的区域id。
    bandwidthID: str  # 共享带宽id。
    projectID: Optional[str] = None  # 企业项目 ID，默认为"0"

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4BandwidthDeleteResponse(CtyunOpenAPIResponse):
    statusCode: Optional[int] = None  # 返回状态码（800为成功，900为失败）
    errorCode: Optional[str] = None  # 错误码，为product.module.code三段式码
    error: Optional[str] = None  # 错误码，为product.module.code三段式码
    message: Optional[str] = None  # 失败时的错误描述，一般为英文描述
    description: Optional[str] = None  # 失败时的错误描述，一般为中文描述
    returnObj: Optional['V4BandwidthDeleteReturnObj'] = None  # 成功时返回的数据

    def __post_init__(self):
        super().__init__()


@dataclass_json
@dataclass
class V4BandwidthDeleteReturnObj:
    masterOrderID: Optional[str] = None  # 55d531d7bf2d47658897c42ffb918423
    masterOrderNO: Optional[str] = None  # 20221021191602644224
    masterResourceStatus: Optional[str] = None  # started
    masterResourceID: Optional[str] = None  # d48cace2da7b4c81b4c0444768a04608
    regionID: Optional[str] = None  # 81f7728662dd11ec810800155d307d5b
    bandwidthID: Optional[str] = None  # bandwidth-xxxx
