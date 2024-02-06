import os
import yaml
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer





def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print(s.getsockname()[0])
    return s.getsockname()[0]




def get_yaml():
    file_yaml = 'configure.yaml'
    rf = open(file=file_yaml, mode='r', encoding='utf-8')
    crf = rf.read()
    rf.close()  # 关闭文件
    yaml_data = yaml.load(stream=crf, Loader=yaml.FullLoader)
    # print(yaml_data)
    return yaml_data

def ftp_server():
    # 定义变量
    username = os.getlogin()   # 用户名
    scan_path = "/home/{}/scan".format(username)   #扫描路径
    os.makedirs( scan_path, 777 ,True)
    ip = get_ip()  # ip地址
    yaml_data = get_yaml()     # 获取yaml的数据
    user = yaml_data['user']   # 虚拟账号
    passwd = yaml_data['passwd']   # 虚拟账号密码
    port = yaml_data['port']  # 端口号  
    # print(username, scan_path, ip, user, passwd, port)

    authorizer = DummyAuthorizer()
    authorizer.add_user(user, passwd, scan_path, perm='elradfmw')
    handler = FTPHandler
    # handler.encoding = 'gbk'
    handler.authorizer = authorizer

    # 监听ip 和 端口,因为linux里非root用户无法使用21端口，所以我使用了2121端口
    server = FTPServer((ip, port), handler)

    # 开始服务
    server.serve_forever()
    

# get_ip()
# get_yaml()
ftp_server()