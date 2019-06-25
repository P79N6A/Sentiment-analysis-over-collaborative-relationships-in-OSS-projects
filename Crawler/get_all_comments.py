import time
import os
import pandas as pd 
import certifi
import urllib3
import json
from urllib3.exceptions import ReadTimeoutError, ConnectTimeoutError
import csv

def try_read_data(data):
    try:
        return pd.read_json(data)
    except:
        return None

def read_data(data,owner_name, repo_name,issue_id):
    df = try_read_data(data)
    if df.empty:
        print("\tNot Reading",str(issue_id))
        return False
    print("\tReading")
    json_file = open('DB/'+repo_name+'/comments/'+str(issue_id)+'.json','w')
    # json_file = open('DB/'+repo_name+'/comments/'+str(issue_id)+'.json','a')
    for jsonObject in data:
        json_file.write(jsonObject)
    json_file.close()

    return True

def try_wait(remain, st):
	print(remain)
	if 10 > int(remain):
		print('###### WAITING FOR LIMITATION ######')
		time.sleep(st + 3600 - time.time())
		new_st = time.time()
		return new_st
	if 4990 < int(remain):
		print('############ NEW HOUR ##############')
		new_st = time.time()
		return new_st
	return st

def find_repo_comments(url, owner_name, repo_name, st, u_id,issue_id):
    try:
        r = http.request('GET', url, timeout=urllib3.Timeout(connect=2.0, read=4.0), retries=False,
                         headers=headers[u_id])
    except ReadTimeoutError:
        print("ReadTimeoutError")
    except ConnectTimeoutError:
        print("ConnectTimeoutError")
    except e:
        print(e)
    else:
        print(r.status)
        print(u_id)
        u_id = u_id + 1
        u_id = u_id % 6
        if r.status == 301:
            url = r.data.decode().split("url\": \"")[1].split("\"")[0]
            # d = try_read_data(r.data.decode())
            # url = d.loc[0].values[-2]
            print("Redirecting to {}".format(url))
            find_repo_topics(url, owner_name, repo_name, st, u_id)
        elif r.status == 404:
            print("{}/{} not found".format(owner_name, repo_name))
        elif r.status != 200:
            print("{}/{} other reason failed".format(owner_name, repo_name))
        else:
            new_st = try_wait(r.headers['X-RateLimit-Remaining'], st)
            if new_st != st:
                st = new_st
            read_data(r.data.decode(), owner_name, repo_name,issue_id)
    return st, u_id

# http = urllib3.PoolManager()
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
accept = 'application/vnd.github.mercy-preview'

headers = [
			urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot1:sjtucit1'), \
			urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot2:sjtucit2'), \
			urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot3:sjtucit3'), \
			urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot4:sjtucit4'), \
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot5:sjtucit5'), \
			urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot6:sjtucit6')  ]
# for header in headers:
# 	header['Accept'] = accept 

st = time.time()
u_id = 0
print("############ STARTING ############")

# owner  = 'pandas-dev'
# name  = 'pandas'
# owner = 'ipython'
# name = 'ipython'
# owner = 'grpc'
# name = 'grpc'
owner = 'openra'
name = 'openra'

print(owner, name)

path = 'DB/'+name+'/issues/'
files= os.listdir(path)
files.sort()
for file in files:
    if file == '.DS_Store':
        continue
    issue_file_path = os.path.join(path, file)
    issue_jsonObject = open(issue_file_path, 'r').read()
    issues = json.loads(issue_jsonObject)

    for x in issues:
    	issue_id  = x['number']
    	cmt_url = x['comments_url']
    	st, u_id = find_repo_comments(cmt_url, owner, name, st, u_id, issue_id)
