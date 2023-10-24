# Implementation of the DPLL Function
import time

def DPLL(clauses):
    cpuTimeStart = time.process_time()

    satisfied = runDPLL(clauses)

    cpuTimeEnd = time.process_time()

    return satisfied, cpuTimeEnd-cpuTimeStart

# Main Function
# Inputs: Clauses
# Outputs: True or False on Satisfied
def runDPLL(clauses):
    # Begin Unit Propagation

    # Grab a unit clause if it exists
    unitProp = grabUnits(clauses)

    # While a unit clause exists
    while unitProp is not None:
        # Remove our clauses that are satisfied and update our clause list
        clauses = unitPropagation(unitProp, clauses)
        
        # Check if we have any more clauses
        unitProp = grabUnits(clauses)
    
    # Begin literal Propagation
    literalProp = grabLits(clauses)
    
    # While a literal clause exists
    while literalProp is not None:
        # Set our literal in the clauses and update clause list
        clauses = literalPropagation(literalProp, clauses)

        # Check if any other literal clauses exists
        literalProp = grabLits(clauses)

    # Check for empty clauses
    if any(len(item) == 0 for item in clauses):
        return False

    # Our double checks
    if len(clauses) == 0:
        return True
    
    # Grab our positive and negative literal
    newLiteralPositive, newLiteralNegative = chooseLiteral(clauses)

    return runDPLL(clauses + [[newLiteralPositive]]) or runDPLL(clauses + [[newLiteralNegative]])

# Returns the Unit Clauses
def grabUnits(clauses):
    # Check for a unit clause
    for item in clauses:
        if len(item) == 1:
            return item[0]
        
    # Return None if we didn't find one
    return None

# Returns the Pure Literals
def grabLits(clauses):
    # Dictionary of literals
    literalList = {}

    # Grab each clause
    for item in clauses:
        # Grab each literal in every clause
        for literal in item:
            # Add to our dictionary
            literalList[literal] = True
    
    # Loop through our dictionary
    for literal in literalList.keys():
        # If the negated version doesn't exist, return that literal
        if -literal not in literalList:
            return literal
    
    # No pure literals found, return None
    return None

# Selects the Literal in the Most Clauses
def chooseLiteral(clauses):
    # Select a literal that is in the largest number of clauses
    
    # Dictionary of literals
    literalList = {}

    # Grab each clause
    for item in clauses:
        # Grab each literal in every clause
        for literal in item:
            if literal in literalList:
                literalList[literal] += 1
            else:
                literalList[literal] = 1

     # What is our max value?
    maxValue = max(literalList.values())
    
    # Grab the maximum key
    for key, values in literalList.items():
        if values == maxValue:
            return abs(key), -abs(key)

# Remove the satisified clauses and delete negated literals
def unitPropagation(unitProp, clauses):
    # Begin Unit Propagation

    # New clause holder array
    newClausesHolder = []

    for item in clauses:
        # Skip our satisfied clauses
        if unitProp in item:
            continue

        # New clause list (checks if unitProp is not negated)
        newClause = [literal for literal in item if unitProp != -literal]
        
        # Add clause to our new clause list
        newClausesHolder.append(newClause)

    # Return our new array of clauses
    return newClausesHolder

# Remove the satisfied clauses
def literalPropagation(litProp, clauses):
    # Begin Literal Propagation

    # New clause holder array
    newClausesHolder = [item for item in clauses if litProp not in item]

    # Return our new array of clauses
    return newClausesHolder