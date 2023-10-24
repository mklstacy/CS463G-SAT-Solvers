# Implementation of the GSAT
import random, time, multiprocessing

def checkClause(clause, assignment):
    # Requires that one variable is satisfied to make the clause satisfied
    for variable in clause:
        var = abs(variable)
        if (variable < 0 and not assignment[var]) or (variable >= 0 and assignment[var]):
            # Finished
            return True
    
    # Clause is not satisfied
    return False

def satisfied(clauses, assignment):
    # Requires that all clauses are satisfied by one of the assignments
    for clause in clauses:
        # Check clause
        if not checkClause(clause, assignment):
            return False
        
    # Clauses are satisfied
    return True

def satisfiedTotal(clauses, assignment):
    # Returns the sum of the satisfied clauses
    return sum(checkClause(clause, assignment) for clause in clauses)

def getBestFlip(clauses, assignment):
    # Set up search
    bestVariable = None
    numberSatisfied = -1

    for var, _ in assignment.items():

        # Check negation of variable first
        assignment[var] = not assignment[var]

        # How many clauses are satisfied?
        testCount = sum(checkClause(clause, assignment) for clause in clauses)
        # If we have a new max, set it
        if testCount > numberSatisfied:
            bestVariable = var
            numberSatisfied = testCount
        
        # Unflip the assignment
        assignment[var] = not assignment[var]

    # Return the best alpha variable
    return bestVariable

def startRun(clauses, allVariables, stopEvent, maxFlips, probability, restartProbability, maxRestart, currentStart=0):

    # Initalize assignment
    assignment = {variable: random.choice([True, False]) for variable in allVariables}

    # Loop through the number of flips allowed
    for _ in range(maxFlips):
        
        # Check if a solution already found
        if stopEvent.is_set():
            return [False, assignment, satisfiedTotal(clauses, assignment)]

        # Check if our assignment satisfies the clauses
        if satisfied(clauses, assignment):
            stopEvent.set()
            return [True, assignment, satisfiedTotal(clauses, assignment)]

        # Prob p: Choose variable alpha that has best number of clauses to satisfy
        if random.random() < probability:
            # Select best alpha to flip
            bestAlpha = getBestFlip(clauses, assignment)

            # Example: {1: True} becomes {1: False}
            assignment[bestAlpha] = not assignment[bestAlpha]

        # Prob 1-p: Choose random variable alpha in C to flip
        else:
            # Pick a random alpha
            randomAlpha = random.choice(allVariables)

            # Example: {1: True} becomes {1: False}
            assignment[randomAlpha] = not assignment[randomAlpha]
    
    # Grab our satisfied total
    totalSatisfied = satisfiedTotal(clauses, assignment)

    # No solution found within maxFlips, update our environment
    # Check if we should update our assignment
    if random.random() < restartProbability:
        return startRun(clauses, allVariables, stopEvent, maxFlips, probability, restartProbability, maxRestart, currentStart+1)
    
    # Else return false
    return [False, assignment, totalSatisfied]

def gsat(clauses, maxFlips=5000, maxThreads=15, probability=0.5, restartProbability=0.01, maxRestarts=2):
    # Grab our CPU Time
    cpuTimeStart = time.time()

    # Get all the variables
    variables = set(abs(variable) for clause in clauses for variable in clause)

    # Convert the variables to a list
    listVariables = list(variables)

    # Our process environment
    with multiprocessing.Pool(maxThreads) as pool:
        stopEvent = multiprocessing.Manager().Event()
        results = pool.starmap(startRun, [(clauses, listVariables, stopEvent, maxFlips, probability, restartProbability, maxRestarts) for _ in range(maxThreads)])

    # Check for solution
    if stopEvent.is_set():
        for item in results:
            if item[0] == True:
                # Grab our CPU Time
                cpuTimeEnd = time.time()
                return item[0], item[1], item[2], cpuTimeEnd-cpuTimeStart
    
    # Grab our max item
    maxSatisfied = 0
    maxItem = None
    for item in results:
        if item[2] > maxSatisfied:
            maxItem = item
            maxSatisfied = item[2]

    # Grab our CPU Time
    cpuTimeEnd = time.time()

    return maxItem[0], maxItem[1], maxItem[2], cpuTimeEnd-cpuTimeStart