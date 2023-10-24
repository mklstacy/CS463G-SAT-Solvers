import os

# Returns our list of clauses
def grabFile(filePath):
    clauseHolder = []
    with open(filePath, 'r') as f:
        for newLine in f:
            # Grab the next line, then strip it into components
            newLine = newLine.strip()

            # Check if we have a 'c' or '%' or '0', skip if yes
            if newLine.startswith('c') or newLine.startswith('%') or newLine.startswith('0'):
                continue

            # Check if we have a p to grab the information
            if newLine.startswith('p'):
                # Example of CNF File Format
                # p cnf 20  91 
                _, _, variableNumber, clauseNumber = newLine.split()
                continue
            
            # Skip empty lines
            if not newLine:
                continue

            # Try to convert our clauses to integers
            try:
                newClause = list(map(int, newLine.split()))
            except ValueError:
                # Error in parsing, skip
                print(f'Error parsing: {newLine}')
                continue

            # Add to our clauseHolder after removing the 0
            if newClause[-1] == 0:
                newClause = newClause[:-1]

            clauseHolder.append(newClause)

    # Return our list of clauses
    return clauseHolder, int(variableNumber), int(clauseNumber)

# Grabs our file information
def grabDirectory(directoryPath):
    # Empty array
    filePaths = []
    
    # Traverse through all files and subdirectories in the given directory
    for root, _, files in os.walk(directoryPath):
        for fileName in files:
            newPath = os.path.join(root, fileName)
            filePaths.append(newPath)
    
    return filePaths