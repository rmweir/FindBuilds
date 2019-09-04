import requests
import sys
import json
from multiprocessing.dummy import Pool

baseurl = "https://drone-pr.rancher.io/api/repos/rancher/rancher/builds"
iterations = 250

# use ["/1/1", "/1/2", "/2/1", "/2/2", "/3/1", "/3/2"] to search everything
# (windows and clone logs)
log_parts = ["/1/2", "/2/2"]

for index, arg in enumerate(sys.argv):
    if arg == "-i":
        iterations = int(sys.argv[index + 1])


def download(url):
    request = requests.get(url=url)  # , headers=headers)
    return json.dumps(request.json())


def isMatch(url):
    logs = download(url)
    if lookfor in logs:
        return url


if sys.argv[1] == "help":
    print("Syntax: python3 start.py <search string> <last drone build index>")
    print("\nExample: python3 start.py \"not found error\" 2111")
    print("\nOptional flags:\n  -i (number of logs to search backwards through)")
    exit()

lookfor = sys.argv[1]
drone_index = sys.argv[2]

urls = []

for i in range(iterations):
    urls += list(map(lambda x: baseurl + "/" +
                     str((int(drone_index) - i)) + "/logs" + x, log_parts))

pool = Pool(8)
found = pool.map(isMatch, urls)
pool.close()
pool.join()

print(list(filter(None.__ne__, found)))
