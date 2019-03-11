"""
    Module contains probabilistic simplicity tests functions
    that determine whether given value is an a simple value

"""

from random import randint, seed
from numpy import array

# Compound numbers that hard to identify correctly by probabilistic algorythms 
CARMICHAEL_NUMBERS = list([561, 1105, 1729, 2465, 2821, 6601, 8911, 10585,
                          15841, 29341, 41041, 46657, 52633, 62745,
                          63973, 75361])


def gcd(a_value, b_value):

    """
    Function finds an gcd of a pair of given numbers.

    :param int a_value: first value
    :param int n_value: second value

    """

    if a_value < b_value:
        a_value, b_value = b_value, a_value

    while b_value:

        a_value, b_value = b_value, a_value % b_value

    return a_value


def euler_criterion(a_value, field):

    """
    Function finds Euler criterion which determine whether given number is deduction on given field.
    Possible values: True, False, ValueError

    :param int a_value: given number to find deduction
    :param int field: simple value which is usually field

    """

    criterion = (a_value ** ((field - 1) // 2)) % field

    if criterion == 1:
        return True
    elif criterion - field == -1:
            return False
    else:
        return ValueError, "Something went wrong...\nGiven number is defenitely not deduction"


def find_representation(value):

    """
    Function finds a (2**s_value)*t_value format number representation which is required in miller_rabin_test.

    :param int value: number represestation of which is required

    """

    s_value = int()

    if value % 2 != 0:
        value -= 1

    while value % 2 == 0:
        value /= 2
        s_value += 1

    return s_value, int(value)


def  find_point_representation(value):

    return value // 2, value % 2

    
def ferma_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not with Ferma algorythm.
    Possible values: True, False, ValueError, "Error message"

    :param int simple_value: number that will be checked on simplicity
    :param int rounds: check iteration number

    """

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


def nightingale_strassen_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not with Nightingale-Strassen algorythm.
    Possible values: True, False, ValueError, "Error message"

    :param int simple_value: number that will be checked on simplicity
    :param int rounds: check iteration number

    """

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
        yakoby_symb = int(euler_criterion(devinder, simple_value))
        if remaider != yakoby_symb:
            return False
        else:
            continue

    return True


def miller_rabin_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not with Miller-Rabin algorythm.
    Possible values: True, False, ValueError, "Error message"

    :param int simple_value: number that will be checked on simplicity
    :param int rounds: check iteration number

    """

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


def find_quadratic_noncall(field):

    """
    Function finds a minimal quadratic non deduction of a given field.
    Possible values: 2 .. field - 1

    :param int field: an a curve field

    """

    for deducation in range(2, field):
        # Euler criterion says that if result value is 1 then found number is deducation
        # In other case if result value is -1 then found number is not deducation
        if euler_criterion(deducation, field) is False:
            return deducation


def find_minimal_deduction(t_value, m_value, field):

    """
    Function finds a minimal quadratic deduction of a given field.
    Possible values: 2 .. field - 1

    :param int t_value: an a t value in Tonelli-Shenks algorythm
    :param int m_value: an a m value in Tonelli-Shenks algorythm that is search limit
    :param int field: an a curve field

    """

    for dedon in range(m_value):
        if ((t_value ** (2 ** dedon))) % field == 1:
            return dedon


def root_computation(value, field):

    """
    Function finds a root of a given value by given field with Tonelli-Shenks algorythm
    Possible values: 1 .. field - 1

    :param int value: value from which a root is required
    :param int field: an a curve field

    """

    r_value = int()
    min_denon = int()

    if euler_criterion(value, field) is not True:
        return ValueError

    s_value, q_value = find_representation(field)

    if s_value == 1:
        r_value = value ** ((field - 1) // 4) % field
        return tuple([r_value, -r_value % field])

    z_value = find_quadratic_noncall(field)
    c_value = (z_value ** q_value) % field
    r_value = value ** ((q_value + 1) // 2) % field
    t_value = (value ** q_value) % field
    m_value = s_value

    while t_value != 1:
        if m_value < 3:
            min_denon = 1
        else:
            min_denon = find_minimal_deduction(t_value, m_value, field)
        b_value = (c_value ** (2 ** (m_value - min_denon - 1))) % field
        r_value = (r_value * b_value) % field
        t_value = (t_value * b_value ** 2) % field
        c_value = (b_value ** 2) % field
        m_value = min_denon

    return tuple([r_value, -r_value % field])