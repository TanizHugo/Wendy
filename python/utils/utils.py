# -*- coding: utf-8 -*-
import json
import logging
import traceback

import subprocess
import paramiko

Log = logging.getLogger(__name__)


def print_exp(e, limit=-1):
    Log.error('##Exception CATCH: %s    %s  %s' % (type(e), e, 'DD##'))
    stb1 = traceback.extract_stack()
    stb2 = traceback.extract_tb(e.__traceback__)
    stb = stb1[:-1] + stb2
    if limit == -1:
        limit = len(stb)
    beg = 0 if len(stb) - limit < 0 else len(stb) - limit
    for st in stb[beg:]:
        Log.error('##C File:%s line:%d in %s\n##C     %s' % (st[0], st[1], st[2], st[3]))
    Log.error('##########C')


def command_out(cmd):
    res = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    out, err = res.communicate()
    if isinstance(out, bytes):
        out = out.decode(errors='ignore')
    if isinstance(err, bytes):
        err = err.decode(errors='ignore')

    return out, err


def getstatusoutput(cmd, host=None):
    ''' run command either locally or remotely and get output and status '''
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许链接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    status = None
    err = ''
    if host is None:
        status, output = subprocess.getstatusoutput(cmd)
    else:
        ssh.connect(hostname=host)
        result = ssh.exec_command(cmd)
        err = result[2]
        output = result[1]
    ssh.close()
    return status, output, err


def ssh_connection(cmd, hostname=None, user_name="root", password="wuzhou@123", port=22):
    stdout = ''
    # 连接服务器
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许链接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 建立连接
        ssh.connect(hostname=hostname, username=user_name, password=password, port=port)
        # 执行命令 result：stdin, stdout, stderr
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # 解析返回的内容
        stdout = stdout.read().decode()
        stderr = stderr.read().decode()
    except Exception as e:
        print_exp(e)
        stderr = "ssh conntect to {} problem appear".format(hostname)
    ssh.close()
    return stdout, stderr


def all_to_bytes(value, unit):
    if "k" in unit:
        return value * 1024
    elif "M" in unit:
        return value * 1024 * 1024
    elif "G" in unit:
        return value * 1024 * 1024 * 1024


def read_file(path):
    with open(path, "r") as fp:
        return fp.read()


def get_json_file(path):
    with open(path, "r") as fp:
        content = json.loads(fp.read())
    return content


def save_json_file(path, data):
    with open(path, "w") as fp:
        fp.write(json.dumps(data, indent=4))


def array_extend(ary1, ary2):
    ary1 = ary1[:]
    for item in ary2:
        if item not in ary1:
            ary1.append(item)
    return ary1


# 获取用户最后一次登录时间
def last_login(user):
    cmd = 'lastlog -u {0}'.format(user)
    result = command_out(cmd)
    data = '-'
    if not result[1]:
        result = result[0]
        try:
            result = result.split('\n')[1].strip()
            d = result.split(' ')[-5:]
            year = d[4]
            mon = d[1][1:]
            day = d[1]
            h = d[2]
            data = '{0}-{1}-{2} {3}'.format(year, mon, day, h)
        except BaseException:
            pass
    return data


def split_list_by_n(list_collection, n):
    """
    将集合均分，每份n个元素
    :param list_collection:
    :param n:
    :return:返回的结果为评分后的每份可迭代对象
    """
    for i in range(0, len(list_collection), n):
      yield list_collection[i: i + n]