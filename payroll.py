# -*- coding: utf-8 -*-
'''
This program facilitates payroll by batch sending zen from input file.   

'''

import subprocess
import csv

__author__ = "Robert Viglione"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Robert Viglione"
__email__ = "rob@zensystem.io"
__status__ = "Production"

#User inputs
ZENCLI_PATH = "./zen-cli"
FILE_NAME = "payroll"
NUM_CONFIRMS = 1
TX_FEE_BASE = 0.0001

FROM_ADDRESS = "zngBRTnCFzT3dTizixP6cCUwKBGUAjzmN9a" #secure nodes

payroll = []
# Creating list of tuples for payroll data (name, address, amount)
with open("./payroll/" + FILE_NAME + '.csv', 'rb') as f:
    reader = csv.reader(f)
    #payroll = list(reader) #packaging as list
    payroll = map(tuple, reader) #packaging as tuple 

#Checking sum of utxos
funds_total = 0
for i in range(len(payroll)):
    funds_total += float(payroll[i][2])

print "You need to fund the sending address: " + str(funds_total)


check_amount = float(subprocess.check_output("./zen-cli z_getbalance " + FROM_ADDRESS, shell=True))
change_amount = check_amount - TX_FEE_BASE*len(payroll) - funds_total

#Structuring syntax to send a padded utxo to each address in own wallet
ARG1 = "\'["
for i in range(len(payroll)):
    ARG1 += "{\"address\": \"" + payroll[i][1] + "\", " \
            "\"amount\": \"" + payroll[i][2] + "\"}," \

ARG1 += "{\"address\": \"" + FROM_ADDRESS + "\", " \
            "\"amount\": \"" + str(change_amount) + "\"}"

ARG1 += "]\'"
print ARG1

inputs = len(payroll) #Number of input addresses to which funds will be sent
TX_FEE = TX_FEE_BASE * inputs #Actual TX_FEE will account for multiple inputs

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