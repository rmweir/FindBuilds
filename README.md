### What it does ###
Searches Rancher's PR build logs for given string

### Setup ###
must have python3

pip3 install -r requirements.txt

### Help ###
python start.py help

### How to use ###
params: string to look for, newest drone index to start at

options (must be after params): -i: how many logs to go through (default is 250)

search example: python3 start.py "someuniquetest failed" 3766 -i 500

list example: python3 start.py {id} -ff
