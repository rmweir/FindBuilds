import json
import requests
import sys
from functools import partial
from multiprocessing.dummy import Pool

baseurl = "https://drone-pr.rancher.io/api/repos/rancher/rancher/builds"
iterations = 250
current = [0]
# use ["/1/1", "/1/2", "/2/1", "/2/2", "/3/1", "/3/2"] to search everything
# (windows and clone logs)
log_parts = ["/1/2", "/2/2"]

for index, arg in enumerate(sys.argv):
    if arg == "-i":
        iterations = int(sys.argv[index + 1])


def update_progress(progress):
    """Displays or updates a console progress bar
    Accepts a float between 0 and 1. Any int will be converted to a float.
    A value under 0 represents a 'halt'.
    A value at 1 or bigger represents 100%"""
    barLength = 20  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format(
        "#"*block + "-"*(barLength-block), round(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def download(url):
    resp = requests.get(url=url)  # , headers=headers)
    if resp.status_code > 400:
        return ""

    return json.dumps(resp.json())


def isMatch(url, current):
    current[0] += 1
    update_progress(current[0]/(iterations*len(log_parts)))
    logs = download(url)
    if lookfor in logs:
        return url


if sys.argv[1] == "help":
    print("Syntax: python start.py <search string> <last drone build index>")
    print("Example: python start.py \"not found error\" 2111")
    print("\nOptional flags:\n-i (number of logs to search through")
    exit

lookfor = sys.argv[1]
drone_index = sys.argv[2]

urls = []

for i in range(iterations):
    urls += list(map(lambda x: baseurl + "/" +
                     str((int(drone_index) - i)) + "/logs" + x, log_parts))

pool = Pool(8)
found = pool.map(partial(isMatch, current=current), urls)
pool.close()
pool.join()

print(list(filter(None.__ne__, found)))
