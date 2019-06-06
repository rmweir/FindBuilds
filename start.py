import requests
import sys
import json
import time

baseurl = ""
iterations = 300

cookie = sys.argv[1]
lookfor = sys.argv[2]
pr_index = sys.argv[3]

matchedlogs = []

log_parts = ["/1/1", "/1/2", "/2/1", "/2/2", "/3/1", "/3/2"]


def download(url):
    headers = {'cookies': cookie}
    request = requests.get(url=url, headers=headers)
    return json.dumps(request.json())


def isMatch(url):
    logs = download(url)
    return logs.find(lookfor) != -1


if sys.argv[1] == "help":
    print("Syntax: python start.py <cookie> <string to look for> <last pr index>")
    print("Example: python start.py asdfasdfsdag \"not found error\" 2111")
else:
    for i in range(iterations):
        urls = list(map(lambda x: baseurl + "/" + str((int(pr_index) - i)) + "/logs" + x, log_parts))
        # print(urls)
        matchedlogs += list(filter(lambda x: isMatch(x), urls))
        time.sleep(.2)
        print("[" + i + "]" + "Matched logs: " + str(list(matchedlogs)))


    print(matchedlogs)
