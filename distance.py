#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# file: 'distance.py'
"""
Module: distance

Utilities for manipulation of feet, inches and fractions of an inch.

Provides a class Distance with the following:
Operators:
    +, -, *, /, **, as well as +=, -=, *= and /=.
        The second operand can be an instance of the class or a number.
Methods:
    def __init__(self, feet, inches, numerator=0, denominator=1):
    def value(self):
        Returns the distance in inches as a float.
    def show(self, inches_only = False, accuracy=16):
        Returns a formated string showing 
            [feet,] inches, numerator, denominator.
        If you want only inches (no feet) set inches_only to True.
        Accuracy to the nearest 1/16th is assumed but can be changed.
    def sqrt(self):
        Returns another instance that is its square root.
    def new(self):
        Returns another instance with the same value. 
        Use this rather than an assignment.

Also provides the following function:
def distances(distance, n_steps):
    Returns an array of distances (as floating point inches)
    marking off <distance> into <n_steps> equal length segments
    starting at 0 and going up to distance.
"""

import math

EPSILON = 0.00001

class Distance(object):

    INCHES = 12  # Inches in a foot.

    def __init__(self, feet, inches, numerator=0, denominator=1):
        """Sets distance in decimal inches.

        Input as described.  If there is no fractional part,
        default positional arguments are provided (0 for numerator
        and 1 for denominator.)
        First two parameters may be any type that can be converted
        to float.  The default parameters, if provided, must be able
        to be converted to integer type.
        (DON'T ENTER 0 for last paramter- mustn't divide by 0!)
        """
        self.decimal_inches = (float(feet) * Distance.INCHES
                                + float(inches)
#                               + int(numerator) / int(denominator))
                                + float(numerator) / float(denominator))

    @property
    def value(self):
        """
        Returns decimal inches.
        """
        return self.decimal_inches

    def new(self):
        """
        Returns another instance with the same value.
        """
        return Distance(0, self.value)

    def how_many_in(self, other):
        """
        Returns a float indicating how many times
        self fits into other.
        """
#       print("other.value is {:.1f}; self.value is {:.1f}"
#           .format(other.value, self.value))
        return other.value / self.value

    def __add__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches + inches
        return ret

    def __iadd__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        self.decimal_inches += inches
        return self

    def __sub__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches - inches
        return ret

    def __isub__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        self.decimal_inches -= inches
        return self

    def __mul__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches * inches
        return ret

    def __imul__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        self.decimal_inches *= inches
        return self

    def __truediv__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return Distance(0, self.decimal_inches / inches)
        ret = Distance(0, 0)

    def __itruediv__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        self.decimal_inches /= inches
        return self

    def __pow__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return Distance(0, self.decimal_inches ** inches)

    def __lt__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return self.decimal_inches < inches

    def __le__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return self.decimal_inches <= inches

    def __eq__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        if abs(self.decimal_inches - inches) > EPSILON:
            return False
        else:
            return True
        return self.decimal_inches == inches

    def __ne__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        if abs(self.decimal_inches - inches) <= EPSILON:
            return False
        else:
            return True

    def __ge__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return self.decimal_inches >= inches

    def __gt__(self, other):
        if isinstance(other, Distance):
            inches = other.decimal_inches
        else:
            inches = other
        return self.decimal_inches > inches

    def sqrt(self):
        """
        Returns another instance that is its square root.
        """
        return Distance(0, math.sqrt(self.decimal_inches))

    def show(self, inches_only = False, accuracy=16):
        """Returns a string representation:
            feet|none, inches, numerator, denominator.

        Assumes you want feet, inches, fractions of an inch.
        If you want only inches (no feet) set inches_only to True.
        Accuracy to the nearest 1/16th is assumed but can be changed.
        """
        inches, decimal = divmod(self.decimal_inches, 1)
        fraction, decimal = divmod(decimal * accuracy, 1)
        if decimal >= 0.5:
            fraction += 1
        while fraction % 2 == 0 and fraction > 0:
            fraction /= 2
            accuracy /= 2
        if inches_only or self.value < Distance.INCHES:
            args = int(inches), int(fraction), int(accuracy)
            if args[1]:
                return """{}"{}/{}""".format(*args)
            else:
                return '{}"'.format(args[0])
        else:
            feet, inches = divmod(inches, 12)
            args = int(feet), int(inches), int(fraction), int(accuracy)
            if args[2]:
                return """{}'{}"{}/{}""".format(*args)
            else:
                return "{}'{}\"".format(*args[:2])

    __str__ = show

def hypoteneuse(side1, side2):
    """Returns the hypoteneuse using the two sides.
    An attempt is made to interpret each parameter
    as an instance of Distance.
    Returns None if unsuccessfull."""
    sum_of_squares = Distance(0, 0)
    for side in (side1, side2,):
        if type(side)==Distance:
            sum_of_squares += side**2
        else:
            try:
                sum_of_squares += Distance(*side)**2
            except ValueError:
                return
    return sum_of_squares.sqrt()

def remaining_side(hypotenuse, side1):
    """
    length = math.sqrt(diag**2 - width**2)
    """
    params = [hypotenuse, side1]
    for i in range(len(params)):
        if type(params[i]) != Distance:
            try:
                params[i] = Distance(*params[i])
            except ValueError:
                return
    ret = (params[0]**2 - params[1]**2).sqrt()
    assert(type(ret) == Distance)
    return ret

def distances(distance, n_steps):
    """ Returns an array of distances (as floating point inches)
    marking off <distance> into <n_steps> equal length segments
    starting at 0 and going up to distance.
    """
    ret = []
    for i in range(n_steps + 1):
        ret.append(distance * i / n_steps)
    return ret

def lay_out(span, gauge, n_spaces):
    """The first two parameters can be either instances of the Distance
    class or tuples suitable for turning into instances there of.
    The third is an integer.
    Assume we have a 'span' length opening that we want to divide into
    'n_spaces' spaces using dividers that are themselves 'gauge' wide.
    Returned is an array of instances of the Distance class.
    The array values begin with 0 and end with span.
    Intervening pairs are points marking the location of each side of each
    divider.  The second item in the array provides the gap.
    """
    if type(span) == tuple:
        span = Distance(*span)
    if type(gauge) == tuple:
        gauge = Distance(*gauge)
    gap =  (span - gauge * (n_spaces -1)) / n_spaces
    ret = []
    ret.append(Distance(0, 0))
    running_total = gap.new()
    ret.append(running_total.new())
    while (span - running_total) > EPSILON:
#       print("running_total is {}".format(running_total))
        running_total += gauge
        ret.append(running_total.new())
        running_total += gap
        ret.append(running_total.new())
#   print("Running total and span are {} & {} respectively."
#       .format(running_total.show(), span.show()))
    assert(running_total == span)
    return ret


def test():
    while True:
        tup = input(
            "Provide feet, inches, fraction, denominator: ")
        tup = tup.split()
        di = Distance(*tup)
        print("{} is represented internally as {}.".format(tup, di.value))
        di1 = Distance(*[int(val) for val in tup])
        print('Represents {}"'.format(di1.show()))
        print('And converts back to {} or {}.'
                                .format(di.show(),
                                        di.show(inches_only = True)))

def receiver_platform():
    opening = (0, 43)
    gauge = (0, 0, 1, 8)
    ret = []
    for n in range(5, 11):
        gap = (span - thickness * n) / (n + 1)
        ret.append("With {} cross members, gaps will be {}."
                .format(n, gap.show()))
    return ret

def show(inches):
    for inch in inches:
        print("{:6.2f} inches => {}."
                .format(inch, Distance(0, inch).show()))

def loft_cart(spaces, guage, n_openings):
    """Assume we have several openings the sizes of which are
    provided as the first parameter: a tuple of tuples.
    We want to divide each of them into <n_openings> using
    divider of dimention provided as the second parameter:
    also a tuple.  First and second parameters are tuples
    of the form suitable to create an instance of Distance.
    Returned is a string suitable for printing providing the
    lay out."""
    ret = ''
    for i, space in enumerate(spaces, start=1):
        dist = distance.Distance(*space)
        ret += ("""{n}. For a {size} space, lay out is:\n{layout}.\n"""
            .format(n = i,
                    size = dist.show(),
                    layout = (', '.join([d.show() for d in
                                distance.lay_out(dist,
                                        distance.Distance(*guage),
                                        n_openings)])),
                    ))
    return ret

def choose():
    my_dimensions = (
                7,
                7.25,
                9,
                10.5,
                10.75,
                12,
                16,
                17,
                20.5,
                29,
                30,
                32,
                36,
                36 + 1/8,
                43,
                46,
                54,
                55,
                57,
                61,
                67,
                77.5,
                89,
                90,
                102,
                )

    #   test()
    #   show(my_dimensions)
    bad_code = """
    array = platform()
    for line in array:
        print(line)

    array = distances(43, 8)
    for item in array:
        d = Distance(0, item)
        print('{}, '.format(d.show()), end='')
    print()
    """

    begin = 5
    end = 12
    opening = (0, 43)
    gauge = (0, 0, 1, 8)
    print("Number of openings     Size of gap")
    data = []
    for n in range(5, end + 1):
        l = lay_out(opening, gauge, n)
        data.append(l)
    for n, item in enumerate(data, begin):
        print("{:^19}     {:^11}".format(n, item[1].show()))

    which = int(input("Pick one to get a lay out: "))
    print("For span of {}, using {} dividers ({} openings) of gauge {}:"
            .format(Distance(*opening).show(inches_only=True),
                    which-1,
                    which,
                    Distance(*gauge).show(inches_only=True)))
    print("The layout will be:")
    for d in data[which-begin]:
        print('{}, '.format(d.show(inches_only=True)), end='')
    print()
    later = """
    print("We are working with a {} opening and {} cross members."
                                .format(Distance(*opening)))
"""

def rack():
    print("Suggested markings for threaded holes, top to bottom:")
    offset = Distance(0, 1)
    limit = Distance(2,0)
    line = [Distance(0,0)]
    line.append(Distance(0, 0.25) + offset)
    while line[-1] < limit:
        for i in range(2):
            line.append(Distance(0, 0.625) + line[-1])
        line.append(Distance(0, 0.5) + line[-1])
    for d in line:
        print(d.show(inches_only=True))

def railing(height, between_end_posts, gauge, n_openings):
    ret = []
    golden_ratio = 1.618
    ret.append("\n  Span between end posts is {}."
            .format(between_end_posts.show()))
    rail_layout = lay_out(between_end_posts, gauge, n_openings)
    ret.append("  Golden ratio of {}ft is {}."
        .format(height.show(), (height * golden_ratio).show()))
    ret.append("  The lay out assuming {} openings:"
                    .format(n_openings))
    for mark in rail_layout:
        ret.append('\t{}'.format(mark.show()))
    ret.append(" A post height of {} / span of {} maintains the goldenratio."
            .format((rail_layout[1]/golden_ratio).show(),
                        rail_layout[1]))
    return '\n'.join(ret)

span = Distance(16,3, 1, 8)
n_openings = 3
height = Distance(3, 0)
gauge = Distance(0, 2)
between_end_posts = span - Distance(0, 2)

data1 = (Distance(3, 0),  # height
        Distance(16, 3, 1, 8) - Distance(0, 2),  # between_end_posts
        Distance(0, 2),  # gauge
        3)  # n_openings

data2 = (Distance(3, 0),  # height
        Distance(11, 3) - Distance(0, 2) * 2,  # between_end_posts
        Distance(0, 2),  # gauge
        2)  # n_openings


def house_boat_railing_driver():
    print("\nRailing for house boat:")
    print("\nShore side-", end='')
    railing(*data1)
    print("\nRamp side-", end='')
    railing(*data2)

def hughs_pole_driver():
    measurements = [
        86, 73, 68, 66, 43, 40, 38, 16, 15,
        ]
    for x in measurements:
        print("{}: {}".format(x, Distance(0, x).show()))

def rvport():
    measurements = [
        87.5, 145.875, 122.5, 37, (153 + 5/8), 177, (86 + 9/16), 
        (57 + 3/8), 47, 31, 41, 83, (57 + 5/8), 94, 29.175, 9,
        33.5, 77, (77/2), 173.1, 46.68, 89.5,   

        ]
    d = Distance(7, 10)
    halfd = d / 2
    print("Half of {} is {}"
                .format(d.show(), halfd.show()))
    for x in measurements:
        print("{}: {}".format(x, Distance(0, x).show()))

def clay_bricks():
    depth = Distance(2.5, 0)
    width = Distance(3.5, 0)
    length = Distance(4, 0)

    brick_d = Distance(0, 2.25)
    brick_w = Distance(0, 4)
    brick_l = Distance(0, 8)

    coverage_area_needed = (
        width * length +
        depth * length * Distance(0, 2) +
        depth * width * Distance(0, 2)
        )

    coverage_of_1_brick = brick_w * brick_l

    enough2cover_floor = width * length / coverage_of_1_brick
    print("#########  REPORT ###########")
    print("To cover just the foor, will need {} bricks."
            .format(enough2cover_floor.value))
    bricks_needed = coverage_area_needed/coverage_of_1_brick
    bricks_needed = bricks_needed.value
    print(
    "To cover bottom and sides: need {} bricks, costing ${:0.2f}."
            .format(bricks_needed, .5*bricks_needed))
    print("Let's hope they weigh no more than {}lbs each."
            .format(700/bricks_needed))
    print("Suggest buying just 100 bricks.")

def june_bricks():
    depth = Distance(2.5, 0)
    width = Distance(3.5, 0)
    length = Distance(4, 0)

    brick_d = Distance(0, 2.25)
    brick_w = Distance(0, 5.5)
    brick_l = Distance(0, 9.5)

    coverage_area_needed = (
        width * length +
        depth * length * Distance(0, 2) +
        depth * width * Distance(0, 2)
        )

    coverage_of_1_brick = brick_w * brick_l

    enough2cover_floor = width * length / coverage_of_1_brick
    print("#########  REPORT ###########")
    print("To cover just the foor, will need {} bricks."
            .format(enough2cover_floor.value))
    bricks_needed = coverage_area_needed/coverage_of_1_brick
    bricks_needed = bricks_needed.value
    print(
    "To cover bottom and sides: need {} bricks, costing ${:0.2f}."
            .format(bricks_needed, .5*bricks_needed))
    print("Let's hope they weigh no more than {}lbs each."
            .format(700/bricks_needed))
    print("Suggest buying just 100 bricks.")

def rv():
    for distance in (lay_out(Distance(17, 9), Distance(0,0), 5)):
        print(distance.show())

def brick_walls(brick, extra_info=None):
    print("\nCalculate Walls:")
    if extra_info:
        print(extra_info)
    brick_length = brick["l"]
    brick_width = brick["w"]
    end = Distance(0, 33)
    side = Distance(0, 36, 1, 2)
    height = Distance(0, 22, 1, 2)
    n_bricks_end = brick_length.how_many_in(end)
    n_bricks_side = brick_length.how_many_in(side)
    n_bricks_high = brick_width.how_many_in(height)
    height_of_5_brick_widths = brick_width * 5
    print('To span 33" it takes {:.2f} brick lengths.'
        .format(n_bricks_end))
    print('To span 36-1/2" it takes {:.2f} brick lengths.'
        .format(n_bricks_side))
    print('To come up to a height of 22-1/2" we need {:.2f} rows.'
        .format(n_bricks_high))
    print('Five rows would give us a distance of {}'
        .format(height_of_5_brick_widths.show()))
    print(' ... or {}'
        .format(height_of_5_brick_widths.show(inches_only=True)))

def brick_floor(brick, extra_info = None):
    print("\nCalculate Floor:")
    if extra_info:
        print(extra_info)
    brick_length = brick["l"]
    brick_width = brick["w"]
    width = Distance(0, 35)
    length = Distance(0, 39)
    n_bricks_width = brick_width.how_many_in(width)
    n_bricks_length = brick_length.how_many_in(length)
    print('To span 35" it takes {:.2f} brick widths.'
        .format(n_bricks_width))
    print('To span 39" it takes {:.2f} brick lengths.'
        .format(n_bricks_length))

def extra(brick):
    if brick['w'] == Distance(0, 4, 1, 2):
        age = 'new'
    else:
        age = 'old'
    return ("\t(with ({}) bricks {} x {} x {})"
        .format(age,
                brick['l'].show(),
                brick['w'].show(),
                brick['h'].show()))

old = dict(
    l=Distance(0,9),
    w=Distance(0,4, 5, 16),
    h=Distance(0,2, 1, 2),
    )

new = dict(
    l=Distance(0,9),
    w=Distance(0,4, 1, 2),
    h=Distance(0,2, 5, 16),
    )

def basement_framing(vertical):
    """
    diag**2 = length**2 + width**2
    length**2 = diag**2 - width**2
    length = math.sqrt(diag**2 - width**2)
    """
    for stud_size in (Distance(0, 3, 1, 2), Distance(0, 5, 1, 2)):
        print("{}: {} ({})".format(
            stud_size.show(),
            remaining_side(vertical, stud_size).show(accuracy=32),
            (vertical - remaining_side(
                vertical, stud_size)).show(accuracy=32),
            ))

def test_remaining_side():
    remaining2x4 = remaining_side(
        (8, 0), (0, 3, 1, 2))
    remaining2x6 = remaining_side(
        (8, 0), (0, 5, 1, 2))

    fractional2x4 = remaining2x4 - Distance(8, 0)
    fractional2x6 = remaining2x6 - Distance(8, 0)
    print(remaining2x4, fractional2x4.show(accuracy=32))
    print(remaining2x6, fractional2x6.show(accuracy=32))

    fractional2x4 = Distance(8, 0) - remaining2x4
    fractional2x6 = Distance(8, 0) - remaining2x6
    print("{} = {} - {}".format(
        fractional2x4.show(accuracy=32),
        Distance(8,0).show(accuracy=32),
        remaining2x4.show(accuracy=32),
        ))
    print(remaining2x4, fractional2x4.show(accuracy=32))
    print(remaining2x6, fractional2x6.show(accuracy=32))

if __name__ == "__main__":
#   brick_floor(old, extra_info=extra(old))
#   brick_walls(new, extra_info=extra(new))
#   print("Running Python3 script: 'british.py'.......")
#   rack()
#   house_boat_railing_driver()
#   hughs_pole_driver()
#   rvport()
#   clay_bricks()
#   june_bricks()
#   rv()
#   print("running basement_framing(Distance(8, 0)):")
#   basement_framing(Distance(8, 0))
#   print("\nrunning test_remaining_side():")
#   test_remaining_side()
    rk5600 = dict(
        height=Distance(0, 139),
        diameter=Distance(0,123),
        )
    print("RK5600: {height} high, {diameter} in diameter."
        .format(**rk5600))
    rk3000 = dict(
        height=Distance(0, 124),
        diameter=Distance(0,96),
        )
    print("RK3000: {height} high, {diameter} in diameter."
        .format(**rk3000))
    rk1760 = dict(
        height=Distance(0, 89),
        diameter=Distance(0,87),
        )
    print("RK1760: {height} high, {diameter} in diameter."
        .format(**rk1760))

