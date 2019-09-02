# -*- coding: utf-8 -*-
'''
This is PART2 of the z_sendmany_secnode script. Here we sequentially spend all of the
addresses that were funded in PART1, sending utxos to the sec node multisig.

Same two input files.
'''

import subprocess
import time
import sys

__author__ = "Robert Viglione"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Robert Viglione"
__email__ = "rob@zensystem.io"
__status__ = "Production"

#User inputs
ZENCLI_PATH = "./zen-cli"
FILE_NAME_UTXOS = "utxos"
FILE_NAME_ADDRESSES = "addresses"
NUM_CONFIRMS = 1
TX_FEE_BASE = 0.0002
#MULTISIG_BUFFER = 0.001 #Amount to pad each utxo to increase probability of matching
MULTISIG_BUFFER = 0 #Amount to pad each utxo to increase probability of matching
#FROM_ADDRESS = ""

NODE_TYPE = input("SUPER or SECURE? ")
if NODE_TYPE == "SUPER":
    TO_MULTISIG = "zsoVG9Evw68te8hRAP3xPXSbx9HoH26LUYN" #Horizen SUPER NODE multisig
elif NODE_TYPE == "SECURE":
    TO_MULTISIG = "zsi4CcCUYtR1iNjEyjkLPjSVPzSPa4atxt9" #Horizen SECURE NODE multisig

if (NODE_TYPE != "SUPER") and (NODE_TYPE != "SECURE"):
    sys.exit("Please type in either 'SUPER' or 'SECURE' to indicate node type")

    


utxos = []
# Creating list for each utxo per spending batch in multisig 
with open("./node-inputs/" + FILE_NAME_UTXOS + '.txt') as u:
    for line in u:
       utxo = str(float(line.rstrip()) + MULTISIG_BUFFER) #Adds 0.001 buffer
       utxos.append(utxo)
       
# Order utxos by size
utxos.sort(key=float)

addresses = []
# Creating list for the addresses to which to disburse utxos
with open("./node-inputs/" + FILE_NAME_ADDRESSES + '.txt') as a:
    for line in a:
       address = line.rstrip()
       addresses.append(address)


# Only keep as many addresses as there are utxos to spend
if len(addresses) > len(utxos):
    while len(addresses) > len(utxos):
        addresses = addresses[:-1]
else:
    print "You need to add " + str((len(utxos) - len(addresses))) + " more addresses!"


#Structuring syntax to send a padded utxo to each address in own wallet
for i in range(0,len(utxos)):
#for i in range(0,2): #Testing with just two txs
    ARG1 = "\'["
    ARG1 += "{\"address\": \"" + TO_MULTISIG + "\", " + "\"amount\": \"" + utxos[i] + "\"}"
    ARG1 += "]\'"
    command = ZENCLI_PATH + " z_sendmany " + '"' + addresses[i] + '"' + " " + ARG1 + \
    " " + str(NUM_CONFIRMS) + " " + str(TX_FEE_BASE)
    print command
    
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate() #Creates output to check for errors
    
    if len(out) == 0:
        raise Exception("Houston, we have a problem!")
        
    print "Funds are on their way from: " + addresses[i] 
    time.sleep(3)
