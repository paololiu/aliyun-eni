#!/usr/bin/python3

import sys

from retry import retry

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.AttachNetworkInterfaceRequest import AttachNetworkInterfaceRequest
from aliyunsdkecs.request.v20140526.DetachNetworkInterfaceRequest import DetachNetworkInterfaceRequest

# pip3 install aliyun-python-sdk-core-v3
# pip3 install aliyun-python-sdk-ecs
# pip install retry

# 使用阿里云Python SDK，需要一个RAM账号以及一对AccessKey ID和AccessKey Secret。
# 可以在阿里云控制台中的AccessKey管理页面上创建和查看的AccessKey
accessKeyId = "xxxxxxxxxxxxxxxxxxxxxxxx"
accessSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 地域id可以通过阿里云api的DescribeRegions接口查询
# https://help.aliyun.com/document_detail/25609.html?spm=a2c4g.11186623.2.17.46e64f392ieIml
regionId = "cn-shanghai"

instanceId = sys.argv[2]
# 弹性网卡id
networkInterfaceId = "eni-xxxxxxxxxxxxxxxxxxxx"


@retry(exceptions=Exception, tries=3, delay=1)
def attach(client):
    request = AttachNetworkInterfaceRequest()
    request.set_accept_format('json')
    request.set_NetworkInterfaceId(networkInterfaceId)
    request.set_InstanceId(instanceId)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


@retry(exceptions=Exception, tries=3, delay=1)
def detach(client):
    request = DetachNetworkInterfaceRequest()
    request.set_accept_format('json')
    request.set_NetworkInterfaceId(networkInterfaceId)
    request.set_InstanceId(instanceId)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


def main():
    client = AcsClient(accessKeyId, accessSecret, regionId)
    if sys.argv[1] == "attach":
        attach(client)
    elif sys.argv[1] == "detach":
        detach(client)
    else:
        print("parameter error。./%s [attach|detach]" % sys.argv[0])


if __name__ == "__main__":
    main()

