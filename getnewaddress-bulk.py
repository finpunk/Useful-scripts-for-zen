# -*- coding: utf-8 -*-
'''
This program generates new addresses in bulk.
'''

import subprocess
import json

__author__ = "Robert Viglione"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Robert Viglione"
__email__ = "rob@zensystem.io"
__status__ = "Production"

#User inputs
ZENCLI_PATH = "./zen-cli/addresses"
NUM_ADDIES = input("How many addresses do you want to create? ")

for i in range(NUM_ADDIES):
    address = subprocess.check_output("./zen-cli getnewaddress", shell=True)
    output = subprocess.check_output("./zen-cli validateaddress " + address, shell=True)
    struct = json.loads(output)
    privkey = subprocess.check_output("./zen-cli dumpprivkey " + struct["address"] + " >> privkeys-generated.txt", shell=True)
    subprocess.call("echo " + (struct["address"]) + " >> addresses-generated.txt", shell=True)
    subprocess.call("echo " + privkey  + " >> privkeys-generated.txt", shell=True)
    
privkeys = []
#Checking how many entries in privkeys-test.txt
with open("privkeys-generated.txt") as f:
    for line in f:
       privkey = line.rstrip()
       if privkey != "":
           privkeys.append(privkey)
print len(privkeys)
       
#Writing cleaner version of privkey.txt
privkeys_file = open('privkeys-test.txt', 'w')
for item in privkeys:
    privkeys_file.write("%s\n" % item)
    
addresses = []
#Checking how many entries in addresses-generated.txt
with open("addresses-generated.txt") as a:
    for line in a:
       address = line.rstrip()
       addresses.append(address)