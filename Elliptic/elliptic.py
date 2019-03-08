from math import sqrt
from random import randint, seed
from numpy import array

# Compound numbers
CARMICHAEL_NUMBERS = list([561, 1105, 1729, 2465, 2821, 6601, 8911, 10585,
                          15841, 29341, 41041, 46657, 52633, 62745,
                          63973, 75361])


# Finds gcd of a pair of given numbers
def gcd(a_value, b_value):

    if a_value < b_value:
        a_value, b_value = b_value, a_value

    while b_value:

        a_value, b_value = b_value, a_value % b_value

    return a_value


# Return s_value and t_value if number is 
# representable in (2**s_value)*t_value format
def find_representation(value):

    s_value = int()

    while value % 2 == 0:
        value /= 2
        s_value += 1

    return s_value, int(value)


# Return stmbol of Yakoby
def yakoby_symbol(a_value, n_value):

    # Preventing of devide by zero
    if a_value == 0 or n_value == 0:
        return 0

    if gcd(a_value, n_value) != 1:
        return ValueError, "Given number are not mutually simple"

    if a_value > n_value:
        if a_value % n_value == 1:
            return 1
        else:
            return yakoby_symbol(a_value % n_value, n_value)
    elif n_value > a_value:
        if n_value % 4 == 1 or a_value % 4 == 1:
            if n_value % a_value == 1:
                return 1
            else:
                return yakoby_symbol(n_value % a_value, a_value)
        elif n_value % 4 != 1 and a_value % 4 != 1:
            if n_value % a_value == 1:
                return -1
            else:
                return -yakoby_symbol(n_value % a_value, a_value)


# Perform a Ferma simplicity test
def ferma_test(simple_value, rounds):

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value in CARMICHAEL_NUMBERS:
        return False

    # Seeding randint function for clear number randomizing
    seed(randint(1, 2048))

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value % 2 is 0:
        return ValueError, "Given number is even"

    # Perform multiple rounds of division
    for _ in range(rounds):
        random_simple = int(1)
        ev_test = int(2)
        while ev_test != 1:
            try:
                random_simple = randint(1, simple_value)
                ev_test = gcd(random_simple, simple_value)
            except ValueError:
                continue
        # Numpy array approach for performing big-integer operations
        devinder = array([random_simple ** (simple_value - 1)], dtype='object')
        remaider = devinder % array([simple_value])
        if remaider != 1:
            return False
        else:
            continue

    return True


# Perform a Nightingale-strassen simplicity test
def nightingale_strassen_sest(simple_value, rounds):

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value in CARMICHAEL_NUMBERS:
        return False

    # Seeding randint function for clear number randomizing
    seed(0)

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value != 2:
        if simple_value % 2 is 0:
            return ValueError, "Given number is even"

    # Perform multiple rounds of division
    for _ in range(rounds):
        random_simple = int(1)
        ev_test = int(2)
        while ev_test != 1:
            # Try | except - statement in case if randint
            # function return an a value close to 2
            try:
                random_simple = randint(1, simple_value)
                ev_test = gcd(random_simple, simple_value)
            except ValueError:
                continue
        devinder = array([random_simple ** ((simple_value - 1) // 2)],
                         dtype='object')
        remaider = devinder % array([simple_value])
        yakoby_symb = yakoby_symbol(devinder, simple_value)
        if remaider != yakoby_symb:
            return False
        else:
            continue

    return True


# Perform a Miller-Rabin simplicity test
def miller_rabin_test(simple_value, rounds):

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value is CARMICHAEL_NUMBERS:
        return False

    simplicity_witness = False

    # Seeding randint function for clear number randomizing
    seed(randint(1, 2048))

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value != 2:
        if simple_value % 2 is 0:
            return ValueError, "Given number is even"

    # Find double representation of given simple value
    repeats, t_value = find_representation(simple_value - 1)

    # Perform multiple rounds of division
    for _ in range(rounds):

        random_simple = int(1)
        ev_test = int(2)
        while ev_test != 1:
            try:
                random_simple = randint(1, simple_value)
                ev_test = gcd(random_simple, simple_value)
            except ValueError:
                continue
        primary_check = array([random_simple ** t_value]
                              % array([simple_value]), dtype='object')[0]
        if primary_check == 1 or primary_check == -1:
            return True
        for deuce_degree in range(repeats):
            devinder = array([random_simple **
                             ((2 ** deuce_degree) * t_value)], dtype='object')
            remaider = devinder % array([simple_value])

            # Given value is compound
            if remaider == 1:
                return False
            # Given value may be simple | Go to the next iteration
            elif remaider == simple_value - 1 or remaider == -1:
                simplicity_witness = True
                break

    return simplicity_witness


# Function finds discriminant of a curve function with given parameters
def find_discriminant(a_value, b_value, field):

    return (4 * (a_value ** 3) + 27 * (b_value ** 2)) % field


# Function determine if a curve with given parameteres exist
def is_curve_exist(a_value, b_value, field, rounds=None):

    # Initializing round value for simplicity test
    r = int(7)
    if rounds is not None:
        r = rounds

    # Checking if given field is a simple value
    if ferma_test(field, r) is not True:
        return ValueError, "Given field is not an a simple number"

    # Find discriminant to ensure that a curve exist
    if find_discriminant(a_value, b_value, field) == 0:
        return ValueError, "Given curve doesn't exist"
    else:
        return True

if __name__ == "__main__":
    print(is_curve_exist(2, 3, 13))
