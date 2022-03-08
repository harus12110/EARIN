import sys
import getopt
import numpy as np


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def isinteger(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def enterscalar(name, print_name):
    if print_name is True:
        print("Please enter the value of scalar " + name)
    while True:
        scalar = input()
        if isfloat(scalar):
            return float(scalar)
        print("Wrong value. Please provide a single real number")


def enterscalarmatrix(x_pos, y_pos):
    while True:
        scalar = input('A[' + str(x_pos) + ',' + str(y_pos) + ']: ')
        if isfloat(scalar):
            return float(scalar)
        print("Wrong value. Please provide a single real number")


def enterscalarvector(pos, name):
    while True:
        scalar = input(name + '[' + str(pos) + ']: ')
        if isfloat(scalar):
            return float(scalar)
        print("Wrong value. Please provide a single real number")


def enterint():
    while True:
        integer = input()
        if isinteger(integer):
            return int(integer)
        print("Wrong value. Please provide a single integer")


# ------ PARSING THE OPTIONS AND THEIR ARGUMENTS ------
argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "m:f:p:s:n:", ["method=", "function=", "points=", "stop="])
except getopt.GetoptError as err:
    print(err)
    sys.exit()

for opt, arg in opts:
    if opt in ['-m', '--method']:
        method = arg    # which method to use
    elif opt in ['-f', '--function']:
        function = arg  # whether we calculate F(x) or G(x)
    elif opt in ['-p', '--points']:
        points = arg    # method of defining starting points (manual/range)
    elif opt in ['-s', '--stop']:
        stop = arg      # chosen stopping condition (number of iterations/desired value/max computation time)
    elif opt in ['-n']:
        n = arg         # number of iterations

if len(opts) != 5:      # check if all 5 options were provided
    print("Not all options were provided")
    sys.exit()

if method not in ['gradient', 'newton']:
    print("wrong method name provided. use -m gradient or -m newton")
    sys.exit()
if function not in ['f', 'g']:
    print("wrong function name provided. use -f f or -f g")
    sys.exit()
if points not in ['manual', 'range']:
    print("wrong points name provided. use -p manual or -p range")
    sys.exit()
if stop not in ['iterations', 'value', 'time']:
    print("wrong stopping condition name provided. use -s iterations, -s value or -s time")
    sys.exit()
if not n.isnumeric():
    print("wrong number of iteration provided. please write an integer after -n")
    sys.exit()

# ------ GET INITIAL DATA FROM THE USER ------

# get the function variables
if function == 'f':
    a = enterscalar('a', True)
    b = enterscalar('b', True)
    c = enterscalar('c', True)
    d = enterscalar('d', True)
else:
    print("Please enter the number of dimensions d")
    d = enterint()
    if d <= 0:
        print("d was set as below 1. Defaulting to 1")
        d = 1
    print("Please insert values in matrix A one by one")
    A = []
    for i in range(d):
        row = []
        for j in range(d):
            x = enterscalarmatrix(i, j)
            row.append(x)
        A.append(row)
    A = np.array(A)
    print("Please insert values in vector b one b one")
    b = []
    for i in range(d):
        x = enterscalarvector(i, 'b')
        b.append(x)
    b = np.array(b)
    c = enterscalar('c', True)

# get the starting point/s
if points == 'manual':
    if function == 'f':
        print("Please enter the value of the starting point")
        starting_point = enterscalar('', False)
    else:
        print("Please insert values in the starting point vector one by one")
        starting_point = []
        for i in range(d):
            x = enterscalarvector(i, 'starting_point')
            starting_point.append(x)
        starting_point = np.array(starting_point)
else:
    print("Please enter the starting point low range end")
    low = enterint()
    print("Please enter the starting high range end")
    high = enterint()
    if low > high:
        print("Low value larger than the high value. Swapping values")
        temp = low
        low = high
        high = temp
    if function == 'f':
        starting_point = np.random.uniform(low, high)
    else:
        starting_point = [np.random.uniform(low, high) for _ in range(d)]
    
# get the stopping condition value
max_iterations = 10000  # max number of iterations
max_time = 3600         # max computation time (in seconds)
value_condition = False
if stop == 'iterations':
    print("Please enter the maximum number of iterations (stop condition)")
    max_iterations = enterint()
elif stop == 'value':
    print("Please enter the value of desired value (stop condition)")
    value_to_reach = enterscalar('', False)
    value_condition = True
else:
    print("Please enter the maximum computation time (in seconds)(stop condition)")
    max_time = enterscalar('', False)

# ------ MAIN LOOP ------

n = int(n)
if n == 0:
    n = 1
results = []
for i in range(n):
    print('batch iteration ' + str(i) + ': ')
    print('starting point/s: ' + str(starting_point))

    # do main functions here
    if method == 'gradient':
        if function == 'f':
            temp_result = 1
        else:   # function == 'g'
            temp_result = 2
    else:   # method == 'newton'
        if function == 'f':
            temp_result = 3
        else:   # function == 'g'
            temp_result = 4

    results.append(temp_result)

    if i != n - 1:
        if stop == 'manual':
            if function == 'f':
                print("Please enter the value of the starting point")
                starting_point = enterscalar('', False)
            else:
                print("Please insert values in the starting point vector one by one")
                starting_point = []
                for j in range(d):
                    x = enterscalarvector(j, 'starting_point')
                    starting_point.append(x)
                starting_point = np.array(starting_point)
        else:
            if function == 'f':
                starting_point = np.random.uniform(low, high)
            else:
                starting_point = [np.random.uniform(low, high) for _ in range(d)]


results = np.array(results)
print('\nResults: ' + str(results))
print('Mean value: ' + str(np.average(results)))
print('Standard deviation: ' + str(np.std(results)))
