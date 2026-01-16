from ctyun_python_sdk_core import CtyunClient, Credential, ClientConfig, CtyunRequestException

from .models import *


class BandwidthClient:
    def __init__(self, client_config: ClientConfig):
        self.endpoint = client_config.endpoint
        self.credential = Credential(client_config.access_key_id, client_config.access_key_secret)
        self.ctyun_client = CtyunClient(client_config.verify_tls)

    def v4_bandwidth_create(self, request: V4BandwidthCreateRequest) -> V4BandwidthCreateResponse:
        """调用此接口可创建共享带宽。"""
        url = f"{self.endpoint}/v4/bandwidth/create"
        method = 'POST'
        try:
            headers = request.get_headers() or {} 
            body = request.to_dict()
            response = self.ctyun_client.request(
                url=url,
                method=method,
                credential=self.credential,
                headers=headers,
                body=body
            ) 
            return self.ctyun_client.handle_response(response, V4BandwidthCreateResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_bandwidth_delete(self, request: V4BandwidthDeleteRequest) -> V4BandwidthDeleteResponse:
        """调用此接口可删除共享带宽。"""
        url = f"{self.endpoint}/v4/bandwidth/delete"
        method = 'POST'
        try:
            headers = request.get_headers() or {} 
            body = request.to_dict()
            response = self.ctyun_client.request(
                url=url,
                method=method,
                credential=self.credential,
                headers=headers,
                body=body
            ) 
            return self.ctyun_client.handle_response(response, V4BandwidthDeleteResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_bandwidth_disassociate_eip(self, request: V4BandwidthDisassociateEipRequest) -> V4BandwidthDisassociateEipResponse:
        """调用此接口可从共享带宽移出EIPs。"""
        url = f"{self.endpoint}/v4/bandwidth/disassociate-eip"
        method = 'POST'
        try:
            headers = request.get_headers() or {} 
            body = request.to_dict()
            response = self.ctyun_client.request(
                url=url,
                method=method,
                credential=self.credential,
                headers=headers,
                body=body
            ) 
            return self.ctyun_client.handle_response(response, V4BandwidthDisassociateEipResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_bandwidth_associate_eip(self, request: V4BandwidthAssociateEipRequest) -> V4BandwidthAssociateEipResponse:
        """调用此接口可添加EIPs至共享带宽。"""
        url = f"{self.endpoint}/v4/bandwidth/associate-eip"
        method = 'POST'
        try:
            headers = request.get_headers() or {} 
            body = request.to_dict()
            response = self.ctyun_client.request(
                url=url,
                method=method,
                credential=self.credential,
                headers=headers,
                body=body
            ) 
            return self.ctyun_client.handle_response(response, V4BandwidthAssociateEipResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))



