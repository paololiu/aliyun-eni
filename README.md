# aliyun-eni
通过阿里云的弹性网卡实现keepalived高可用

## 环境
阿里云两台云主机，一块弹性网卡。

## 系统
建议使用centos 7.3或者centos 6.8以上版本，这样弹性网卡可以自动识别，其他版本的操作系统需要手动配置网卡。

安装keepalived，没什么特别要求，yum安装就可以了

安装python3环境，以及几个相关的包

```
pip3 install aliyun-python-sdk-core-v3
pip3 install aliyun-python-sdk-ecs
pip install retry
```

## 脚本配置
弹性网卡操作脚本eni.py

```
# 使用阿里云Python SDK，需要一个RAM账号以及一对AccessKey ID和AccessKey Secret。
# 可以在阿里云控制台中的AccessKey管理页面上创建和查看的AccessKey
accessKeyId = "xxxxxxxxxxxxxxxxxxxxxxxx"
accessSecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 地域id可以通过阿里云api的DescribeRegions接口查询
# https://help.aliyun.com/document_detail/25609.html?spm=a2c4g.11186623.2.17.46e64f392ieIml
regionId = "cn-shanghai"

# 弹性网卡id
networkInterfaceId = "eni-xxxxxxxxxxxxxxxxxxxx"
```

绑定网卡attach.sh

```
# i-uf6h0rv0h9j8tktmlcjn，当前主机id
/etc/keepalived/eni.py attach i-uf6h0rv0h9j8tktmlcjn

```
解绑网卡detach.sh

```
# i-uf6h0rv0h9j8tktmlcjn，当前主机id
/etc/keepalived/eni.py detach i-uf6h0rv0h9j8tktmlcjn
```

另外keepalived.conf要注意一个地方，阿里云vpc网络是不支持网络广播的，所以要配置unicast_src_ip和unicast_peer

```
#本机本地IP
unicast_src_ip 172.16.6.166
unicast_peer {
  172.16.6.167   ##（对端IP地址）此地址一定不能忘记
}
```
因为没有虚拟IP，也就不要配置virtual_ipaddress了。当状态是master时调用attach.sh绑定网卡，其他情况则调用detach.sh解绑网卡

```
notify_master /etc/keepalived/attach.sh
notify_backup /etc/keepalived/detach.sh
notify_fault /etc/keepalived/detach.sh
notify_stop /etc/keepalived/detach.sh
```
