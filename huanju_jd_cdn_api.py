# -*- coding: utf8 -*-

import hashlib, json, requests, re
from datetime import datetime
from dns import resolver

def domain_dns_resolver(url):
    host = re.match(r'(.*)://(.*?)/(.*)', url).group(2)
    try:
        rs = resolver.query(host, "CNAME").response.answer
    except Exception:
        rs = "-"

    if rs == "-":
        cdn = "none"
    else:
        if str(rs[0]).find('alikunlun.com') != -1 or str(rs[0]).find('w.kunlun') != -1:
            cdn = "aliyun"
        elif str(rs[0]).find('cdn.dnsv1.com') != -1:
            cdn = "qq"
        elif str(rs[0]).find('jcloud-cdn.com') != -1:
            cdn = "jd"
        else:
            cdn = "other"
    return cdn

headers = {"Content-Type": "application/json"}

def get_signature():
    import time
    t = time.time()
    time = datetime.fromtimestamp(t).strftime('%Y%m%d')
    str = time + 'YY_cdn6551e783c3b33a1f696356eb2b1b1117'
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    signature = hl.hexdigest()
    return signature

def jdRefreshCdn(url_list):
    refreshDoamins = "http://opencdn.jcloud.com/api/refresh"

    parameters = {
        "username": "YY_cdn",
        "signature": get_signature(),
        "type": "file",
        "instances": url_list
    }

    response = json.loads(requests.post(refreshDoamins, data=json.dumps(parameters), headers=headers).content)
    return response["taskid"]

def jdQueryCdn(taskid):
    queryDoamins = "http://opencdn.jcloud.com/api/refreshQuery"

    parameters = {
        "username": "xxx",
        "signature": get_signature(),
        "taskid": taskid
    }

    response = json.loads(requests.post(queryDoamins, data=json.dumps(parameters), headers=headers).content)
    return response


# url = ["http://mr.5153.com/do_not_delete/noc.gif","http://mr.5153.com/do_not_delete/noc1.gif"]
# jdRefreshCdn(url)

# b = "32569608-42ca-4ec4-a36e-e575db529281"
# print jdQueryCdn(b)

# print domain_dns_resolver(url="http://wan.yy.com/do_not_delete/")
