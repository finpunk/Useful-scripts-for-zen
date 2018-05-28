# -*- coding: utf-8 -*-
'''
This program facilitates easiser funding of the ZenCash secure node multisg. Since
we can't send many utxos to the same address with z_sendmany, PART1 of this two-part
script sends precise amounts to a set of own addresses that will then be sent to 
the sec node multisig in PAR2.   

Input files are a .txt with utxo amounts required and another .txt file with available
own wallet addresses.
'''

import subprocess

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
TX_FEE_BASE = 0.0001
MULTISIG_BUFFER = 0.001 #Amount to pad each utxo to increase probability of matching
FROM_ADDRESS = ""
#TO_MULTISIG = "zsf45QuD75XJdm3uLftiW6pucvbhvrbhAhZ" #ZenCash sec node multisig

utxos = []
# Creating list for each utxo per spending batch in multisig 
with open("./sec-node-inputs/" + FILE_NAME_UTXOS + '.txt') as u:
    for line in u:
       utxo = str(float(line.rstrip()) + MULTISIG_BUFFER + TX_FEE_BASE) #Adds 0.001 buffer + 0.0001 future tx fee
       utxos.append(utxo)
       
addresses = []
# Creating list for the addresses to which to disburse utxos
with open("./sec-node-inputs/" + FILE_NAME_ADDRESSES + '.txt') as a:
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
ARG1 = "\'["
for i in range(0, len(utxos)):
    ARG1 += "{\"address\": \"" + addresses[i] + "\", " \
            "\"amount\": \"" + utxos[i] + "\"},"
ARG1 = ARG1[:-1]  # remove comma at the end
ARG1 += "]\'"
print ARG1

inputs = len(utxos) #Number of input addresses to which funds will be sent
TX_FEE = TX_FEE_BASE * inputs #Actual TX_FEE will account for multiple inputs

# This is the command that calls z_sendmany with appropriate parameters
command = ZENCLI_PATH + " z_sendmany " + '"' + FROM_ADDRESS + '"' + " " + ARG1 + \
    " " + str(NUM_CONFIRMS) + " " + str(TX_FEE)
print command

# This is where we send the command to terminal for execution
proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
(out, _) = proc.communicate() #Creates output to check for errors

if len(out) == 0:
    raise Exception("Houston, we have a problem!")
    
print "Funds are on their way!"
