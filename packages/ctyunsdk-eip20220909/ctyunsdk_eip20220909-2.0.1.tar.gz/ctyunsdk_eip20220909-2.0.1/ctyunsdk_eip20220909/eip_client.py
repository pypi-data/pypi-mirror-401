from ctyun_python_sdk_core import CtyunClient, Credential, ClientConfig, CtyunRequestException

from .models import *


class EipClient:
    def __init__(self, client_config: ClientConfig):
        self.endpoint = client_config.endpoint
        self.credential = Credential(client_config.access_key_id, client_config.access_key_secret)
        self.ctyun_client = CtyunClient(client_config.verify_tls)

    def v4_eip_delete(self, request: V4EipDeleteRequest) -> V4EipDeleteResponse:
        """调用此接口可删除 EIP。"""
        url = f"{self.endpoint}/v4/eip/delete"
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
            return self.ctyun_client.handle_response(response, V4EipDeleteResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_create(self, request: V4EipCreateRequest) -> V4EipCreateResponse:
        """调用此接口可创建弹性公网IP（Elastic IP Address，简称EIP）。"""
        url = f"{self.endpoint}/v4/eip/create"
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
            return self.ctyun_client.handle_response(response, V4EipCreateResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_new_list(self, request: V4EipNewListRequest) -> V4EipNewListResponse:
        """调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。"""
        url = f"{self.endpoint}/v4/eip/new-list"
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
            return self.ctyun_client.handle_response(response, V4EipNewListResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_show(self, request: V4EipShowRequest) -> V4EipShowResponse:
        """调用此接口可查看EIP详情。"""
        url = f"{self.endpoint}/v4/eip/show"
        method = 'GET'
        try:
            headers = request.get_headers() or {} 
            params = request.to_dict()
            response = self.ctyun_client.request(
                url=url,
                method=method,
                credential=self.credential,
                headers=headers,
                params=params
            ) 
            return self.ctyun_client.handle_response(response, V4EipShowResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_attach_port_bm(self, request: V4EipAttachPortBmRequest) -> V4EipAttachPortBmResponse:
        """调用此接口可将弹性公网IP（Elastic IP Address，简称EIP）与物理机网卡进行绑定。"""
        url = f"{self.endpoint}/v4/eip/attach-port-bm"
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
            return self.ctyun_client.handle_response(response, V4EipAttachPortBmResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_attach_port_vm(self, request: V4EipAttachPortVmRequest) -> V4EipAttachPortVmResponse:
        """调用此接口可将弹性公网IP（Elastic IP Address，简称EIP）与云主机网卡进行绑定。"""
        url = f"{self.endpoint}/v4/eip/attach-port-vm"
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
            return self.ctyun_client.handle_response(response, V4EipAttachPortVmResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_associate(self, request: V4EipAssociateRequest) -> V4EipAssociateResponse:
        """调用此接口可将弹性公网IP（Elastic IP Address，简称EIP）与相关云产品上绑定。"""
        url = f"{self.endpoint}/v4/eip/associate"
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
            return self.ctyun_client.handle_response(response, V4EipAssociateResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_change_name(self, request: V4EipChangeNameRequest) -> V4EipChangeNameResponse:
        """调用此接口修改 EIP 名字。"""
        url = f"{self.endpoint}/v4/eip/change-name"
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
            return self.ctyun_client.handle_response(response, V4EipChangeNameResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))

    def v4_eip_disassociate(self, request: V4EipDisassociateRequest) -> V4EipDisassociateResponse:
        """调用此接口可将弹性公网IP从绑定的云产品上解绑。"""
        url = f"{self.endpoint}/v4/eip/disassociate"
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
            return self.ctyun_client.handle_response(response, V4EipDisassociateResponse)
        except Exception as e:
            raise CtyunRequestException(str(e))



