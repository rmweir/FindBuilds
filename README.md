### What it does ###
Searches Rancher's PR build logs for given string

### Setup ###
Requires python3

`pip3 install -r requirements.txt`

### Help ###
`python3 start.py help`

### How to use ###

```
python3 start.py "FAILED test_rbac.py::test_project_owner" 4249 -i 500
```

params
```
1. String to look for. Use a specific string which represents your error. 
2. The newest Drone index to start at. This is the ID in a drone url, not the PR or issue ID.
```

options (must be after params)
```
-i: how many logs to go backwards through (default is 250)
```
