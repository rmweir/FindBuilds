import requests
import sys
import json
import time

baseurl = "https://drone-pr.rancher.io/api/repos/rancher/rancher/builds"
iterations = 250

matchedlogs = []

# use ["/1/1", "/1/2", "/2/1", "/2/2", "/3/1", "/3/2"] to search everything (windows and clone logs)
log_parts = ["/1/2", "/2/2"]

for index, arg in enumerate(sys.argv):
    if arg == "-i":
        iterations = int(sys.argv[index + 1])

def download(url):
    request = requests.get(url=url)  # , headers=headers)
    return json.dumps(request.json())


def isMatch(url):
    logs = download(url)
    return logs.find(lookfor) != -1


if sys.argv[1] == "help":
    print("Syntax: python start.py <string to look for> <last drone build index>")
    print("Example: python start.py \"not found error\" 2111")
    print("\nOptional flags:\n-i (number of logs to search through")
else:
    lookfor = sys.argv[1]
    drone_index = sys.argv[2]
    for i in range(iterations):
        urls = list(map(lambda x: baseurl + "/" + str((int(drone_index) - i)) + "/logs" + x, log_parts))
        # print(urls)
        matchedlogs += list(filter(lambda x: isMatch(x), urls))
        time.sleep(.1)
        print("[" + str(i) + "]" + "Matched logs: " + str(list(matchedlogs)))


    print(matchedlogs)
