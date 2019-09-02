# -*- coding: utf-8 -*-
'''
This program facilitates easiser funding of the Horizen secure and super node multisigs. Since
we can't send many utxos to the same address with z_sendmany, PART1 of this two-part
script sends precise amounts to a set of own addresses that will then be sent to 
the sec node multisig in PART2.   

Input files are a .txt with utxo amounts required and another .txt file with available
own wallet addresses.
'''

import subprocess
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


NODE_TYPE = input("SUPER or SECURE? ")
if NODE_TYPE == "SUPER":
    FROM_ADDRESS = "INPUT_SUPER_NODE_ADDRESS" #SUPER nodes
elif NODE_TYPE == "SECURE":
    FROM_ADDRESS = "INPUT_SECURE_NODE_ADDRESS" #SECURE nodes

if (NODE_TYPE != "SUPER") and (NODE_TYPE != "SECURE"):
    sys.exit("Please type in either 'SUPER' or 'SECURE' to indicate node type")



utxos = []
# Creating list for each utxo per spending batch in multisig 
with open("./node-inputs/" + FILE_NAME_UTXOS + '.txt') as u:
    for line in u:
       utxo = str(float(line.rstrip()) + TX_FEE_BASE) 
       utxos.append(utxo)

# Order utxos by size
utxos.sort(key=float)

#Checking sum of utxos
utxos_total = 0
for i in utxos:
    utxos_total += float(i)

print "You need to fund " + FROM_ADDRESS + " : " + str(utxos_total)
       
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

inputs = len(utxos) #Number of input addresses to which funds will be sent
TX_FEE = TX_FEE_BASE * inputs #Actual TX_FEE will account for multiple inputs

check_amount = float(subprocess.check_output("./zen-cli z_getbalance " + FROM_ADDRESS, shell=True))
change_amount = round((check_amount - TX_FEE_BASE*len(utxos) - utxos_total),8)

#Structuring syntax to send a padded utxo to each address in own wallet
ARG1 = "\'["
for i in range(0, len(utxos)):
    ARG1 += "{\"address\": \"" + addresses[i] + "\", " \
            "\"amount\": \"" + utxos[i] + "\"}," \

ARG1 += "{\"address\": \"" + FROM_ADDRESS + "\", " \
            "\"amount\": \"" + str(change_amount) + "\"}"

ARG1 += "]\'"
print ARG1



# This is the command that calls z_sendmany will appropriate parameters
command = ZENCLI_PATH + " z_sendmany " + '"' + FROM_ADDRESS + '"' + " " + ARG1 + \
    " " + str(NUM_CONFIRMS) + " " + str(TX_FEE)
print command

# This is where we send the command to terminal for execution
proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
(out, _) = proc.communicate() #Creates output to check for errors

if len(out) == 0:
    raise Exception("Houston, we have a problem!")
    
print "Funds are on their way!"