'''############ Start of Settings ############'''

# The directory path is the location of our HARD CNF Files
#directoryPath = './HARD CNF Formulas'
directoryPath = './HARD CNF Formulas'

# The excelFilePath is the location of our excel file to export our information
excelFilePath = './Blank.xlsx'

# Walk SAT Settings
WalkIterations = 15000 # Number of iterations
WalkProcess = 15 # Number of runs (it will break into different processes or threads)
WalkProbability = 0.5 # Probability to find most satisfying variable vs. randomly flipping

# G SAT Settings
GIterations = 5000 # Number of iterations
GProcess = 15 # Number of runs (it will break into different processes or threads)
GProbability = 0.5 # Probability to find most satisfying variable vs. randomly flipping

# Random Restart Settings
maxRestarts = 2 # Number of allowed random restarts in both GSAT and WalkSAT
restartProbability = 0.01 # Probability of random restart

'''############ Start of Settings ############'''


'''
######################## Credits ########################

(A) ChatGPT Credit

I used ChatGPT to identify how to setup Threads on WalkSat and GSAT.

Version: GPT-4
Date: October 2nd, 2023
Time Stamp: 12:00 AM
Prompt: "Give an example of threading in python"
Chain: https://chat.openai.com/share/fb087b00-8eee-4250-9614-a708c76a39d1

(B) Python Documentation

I looked up Multiprocessing and used some of the code from the Python Documentation on creating multiprocessing

Accessed: October 2nd, 2023
Link: https://docs.python.org/3/library/multiprocessing.html

(C) DPLL Psuedocode Documentation

I used this wikipedia for pseudocode on the DPLL

https://en.wikipedia.org/wiki/DPLL_algorithm
Accessed: September 29th, 2023

######################## Credits ########################
'''

# Reading the Files
from readFile import grabFile
from readFile import grabDirectory

# Test files
from dpll import DPLL

# Process algorithms
from gsatp import gsat as gp
from walksatp import walksat as wp

# Excel Control
import pandas as pd

# Our main program
def runTest():

    # Starter Excel Information
    dataFrame = pd.DataFrame()
    completedList = {}

    # Grab every directory and clean out the rcnf files
    directoryList = grabDirectory(directoryPath)
    directoryList = [fileName for fileName in directoryList if fileName.endswith('.cnf')]

    # Begin gathering data
    for index, filePath in enumerate(directoryList):
        # Print out an update
        print(f'Current File: {filePath} | Progress: {index}/{len(directoryList)}')

        # Our file
        clauseList, variableNumber, clauseNumber = grabFile(filePath)

        # [Success, CPU Time]
        DPLLInformation = DPLL(clauseList)

        print(f'DPLL Complete, time taken: {DPLLInformation[1]} | Success: {DPLLInformation[0]}')

        # Note the number of WalkThreads is our set restart (15 times)
        WalkInformation = wp(clauseList, WalkIterations, WalkProcess, WalkProbability, restartProbability, maxRestarts)

        print(f'WalkSAT Complete, time taken: {WalkInformation[3]}')

        # Note our GThreads is our set restart (15 times)
        GInformation = gp(clauseList, GIterations, GProcess, GProbability, restartProbability, maxRestarts)

        print(f'GInformation Complete, time taken: {GInformation[3]}')

        if filePath not in completedList:
            # Add our new file to our excel list
            newFrame = pd.DataFrame({
                'File Name': str(filePath),
                'Variables': [variableNumber],
                'Clauses': [clauseNumber],
                'DPLL Satisfied': [DPLLInformation[0]],
                'DPLL CPU Time': [DPLLInformation[1]],
                'Walk SAT Result': [WalkInformation[0]],
                'Walk SAT Satisfied': [WalkInformation[2]],
                'Walk SAT CPU Time': [WalkInformation[3]],
                'G SAT Result': [GInformation[0]],
                'G SAT Satisfied': [GInformation[2]],
                'G SAT CPU Time': [GInformation[3]],
            })
            dataFrame = pd.concat([dataFrame, newFrame], ignore_index=True)
            completedList[filePath] = 0

    print('Uploading DataFrame')

    # Uploading our data
    dataFrame.to_excel(excelFilePath, index=False)

    print('Finished')
    print('Updated filePath List:')
    print(completedList)    

if __name__ == '__main__':
    runTest()