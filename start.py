import csv
import json
import requests
import sys
from functools import partial
from multiprocessing.dummy import Pool

baseurl = "http://drone-pr.rancher.io/api/repos/rancher/rancher/builds"
# baseurl = "http://drone-publish.rancher.io/api/repos/rancher/rancher/builds"
iterations = 250
current = [0]

find_failures = False

# use ["/1/1", "/1/2", "/2/1", "/2/2", "/3/1", "/3/2", "/4/1", "/4/2"] to search everything
# (windows and clone logs)
log_parts = ["/1/2", "/2/2", "/3/2", "/4/2"]

for index, arg in enumerate(sys.argv):
    if arg == "-i":
        iterations = int(sys.argv[index + 1])
    if arg == "-ff":
        find_failures=True
    if arg == "-url":
        baseurl = int(sys.argv[index + 1])


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
    try:
        resp = requests.get(url=url)  # , headers=headers)
        if resp.status_code > 400:
            return ""
    except:
        return ""
    return json.dumps(resp.json())


def isMatch(url, current):
    current[0] += 1
    update_progress(current[0]/(iterations*len(log_parts)))
    logs = download(url)
    if look_for in logs:
        return url


failed = {}


def isFailure(url, current):
    global log_parts
    global failed
    current[0] += 1
    update_progress(current[0]/(iterations*len(log_parts)))
    logs = download(url)
    s_parts = logs.split("FAILED test_")
    num_parts = len(s_parts)
    bad_tests = {}
    if  num_parts > 1:
      for i in range(num_parts):
        if i != 0:
          test_only = s_parts[i]
          test_only = "test_" + test_only.split()[0].split("\n")[0].split("[")[0].split("\\n")[0]
          bad_tests[test_only] = True
    for key in bad_tests.keys():
        if failed.get(key):
            failed[key] += 1
        else:
            failed[key] = 1


if sys.argv[1] == "help":
    print("Syntax: python3 start.py <search string> <last drone build index>")
    print("Syntax (find top 10 failed): python start.py <last drone build index> -ff")
    print("Example: python3 start.py \"not found error\" 2111")
    print("\nOptional flags:\n-i (number of logs to search through\n-url (use specified base url instead of default\n \
            -ff (find top 10 most failed tests")
    exit()

if find_failures:
    drone_index = sys.argv[1]
else:
    look_for = sys.argv[1]
    drone_index = sys.argv[2]

urls = []
for i in range(iterations):
    urls += list(map(lambda x: baseurl + "/" +
                     str((int(drone_index) - i)) + "/logs" + x, log_parts))

pool = Pool(8)
if find_failures:
    found = pool.map(partial(isFailure, current=current), urls)
else:
    found = pool.map(partial(isMatch, current=current), urls)
pool.close()
pool.join()

if find_failures:
    print("Failed Tests:", failed)
    print("Writing to file failures.csv...")
    with open("failures.csv", "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["test", "failures"])
        for key in failed.keys():
            csv_writer.writerow([key, failed[key]])
    print("Write complete.")

else:
    print(list(filter(None.__ne__, found)))
