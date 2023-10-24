# Implementation of the Walk SAT
import random, time, multiprocessing

# Checks each literal within the clause
def checkClause(clause, assignment):
    # Requires that one variable is satisfied to make the clause satisfied
    for variable in clause:
        var = abs(variable)
        if (variable < 0 and not assignment[var]) or (variable >= 0 and assignment[var]):
            # Skip clause
            return True
    
    # Clause is not satisfied
    return False

# Checks if a clause is satisfied
def satisfied(clauses, assignment):
    # Requires that all clauses are satisfied by one of the assignments
    for clause in clauses:
        # Check clause
        if not checkClause(clause, assignment):
            return False
        
    # Clauses are satisfied
    return True

# Returns the number of clauses satisfied
def satisfiedTotal(clauses, assignment):
    totalSatisfied = 0
    for clause in clauses:
        # Check clause
        if checkClause(clause, assignment):
            totalSatisfied += 1
        
    # Clauses are satisfied
    return totalSatisfied

def getBestFlip(clauses, assignment, C):
    # Set up search
    bestVariable = None
    numberSatisfied = -1

    for variable in C:
        # Grab the key
        var = abs(variable)

        # Flip the assignment
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

        if stopEvent.is_set():
            return [False, assignment, satisfiedTotal(clauses, assignment)]

        # Check if our assignment satisfies the clauses
        if satisfied(clauses, assignment):
            return [True, assignment, satisfiedTotal(clauses, assignment)]
    
        # Choose an unsatisfied clause C
        C = random.choice([clause for clause in clauses if not checkClause(clause, assignment)])

        # Prob p: Choose variable alpha in C such that flipping alpha maximizes the number of satisfied clauses
        if random.random() < probability:
            # Select best alpha to flip
            bestAlpha = getBestFlip(clauses, assignment, C)

            # Example: {1: True} becomes {1: False}
            assignment[bestAlpha] = not assignment[bestAlpha]

        # Prob 1-p: Choose random variable alpha in C to flip
        else:
            # Pick a random alpha
            randomAlpha = abs(random.choice(C))

            # Example: {1: True} becomes {1: False}
            assignment[randomAlpha] = not assignment[randomAlpha]
    
    # No solution found within maxFlips, do we restart randomly?
    if random.random() < restartProbability and currentStart < maxRestart:
        return startRun(clauses, allVariables, stopEvent, maxFlips, probability, restartProbability, maxRestart, currentStart+1)
    
    # Otherwise return False
    return [False, assignment, satisfiedTotal(clauses, assignment)]

def walksat(clauses, maxFlips=15000, maxThreads=20, probability=0.5, restartProbability=0.1, maxRestart=5):
    # Grab our CPU Time
    cpuTimeStart = time.time()

    # Get all the variables
    variables = set(abs(variable) for clause in clauses for variable in clause)

    with multiprocessing.Pool(maxThreads) as pool:
        stopEvent = multiprocessing.Manager().Event()
        results = pool.starmap(startRun, [(clauses, variables, stopEvent, maxFlips, probability, restartProbability, maxRestart) for _ in range(maxThreads)])

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