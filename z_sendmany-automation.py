# -*- coding: utf-8 -*-
'''
This program facilitates bulk z_sendmany transactions from a single address to 
a set of addresses. The destination addresses are read from a .csv file into a 
dictionary. The ZenCash core software (zend) must be
running and the user will select the file path, amount, number of confirmations 
before the transactions are accessible to recipient, the base transaction
fee to be applied per input address, the address from which funds will be debited,
and the .csv file containing addresses to which funds will be credited. 

This is a useful program to bulk fund secure node or super node addresses.
'''

import subprocess
# import json

__author__ = "Robert Viglione"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Robert Viglione"
__email__ = "rob@zensystem.io"
__status__ = "Production"

#User inputs
ZENCLI_PATH = "./zen-cli"
FILE_NAME = "addresses"
amount = 42
NUM_CONFIRMS = 1
TX_FEE_BASE = 0.0005
FROM_ADDRESS = ""

#Creating dictionary of input addresses to which funds will be sent
d = {}
with open("./addresses/" + FILE_NAME + '.csv') as f:
    for line in f:
       address = line.rstrip()
       d[address] = amount

#ARG1 will include addresses and amounts to which funds will be credited
ARG1 = "\'["
for i in range(0, len(d)):
    ARG1 += "{\"address\": \"" + d.keys()[i] + "\", " \
            "\"amount\": \"" + str(d.values()[i]) + "\"},"
ARG1 = ARG1[:-1]  # remove comma at the end
ARG1 += "]\'"
# print ARG1

inputs = len(d) #Number of input addresses to which funds will be sent
TX_FEE = TX_FEE_BASE * inputs #Actual TX_FEE will account for multiple inputs

# This is the command that calls z_sendmany will appropriate parameters
command = ZENCLI_PATH + " z_sendmany " + '"' + FROM_ADDRESS + '"' + " " + ARG1 + \
    " " + str(NUM_CONFIRMS) + " " + str(TX_FEE)
# print command

# This is where we send the command to terminal for execution
proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
(out, _) = proc.communicate() #Creates output to check for errors

if len(out) == 0:
    raise Exception("Houston, we have a problem!")
    
print "Funds are on their way!"