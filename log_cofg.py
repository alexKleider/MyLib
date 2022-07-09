#!/usr/bin/env python

# File: Mymath/log_cofg.py

"""
        ## Log Center of Gravity ##

Usage:
    ./log_cofg.py [-O]  -? | --help | --version
    ./log_cofg.py [-O -i] --d1=<diameter1> --d2=<diameter2> --len=<length>

Options:
    -?  Print what commands are available and in in what format.
    -h --help  Print this docstring. Best piped through pager.
    --version  Print version.
    -O  If this option is set:
            all command line parameters are displayed.
            The user is then asked whether or not to continue.
            (Used for debuging.)
    --d1 <diameter1>  a diameter at one end
    --d2 <diameter2>  the diameter at the other end
    --len <log_length>  length 
    -i  if this option is set, "imperial" units are assumed and the
        diameters will be treated as inches and length as feet.
        If not set, diameters and length are assumed to be in the same
        units.
"""

addendum2docstring = """
Need for ability to calculate "volume_centre"[1] of a "cylindroid"
object. "Cylindroid" in that the:
Logs tend to be of smaller diameter at one end than the other.
When lifting with a fork lift, it's desirable (_necessary_) to have
the centre of gravity between the forks
I tried and failed to reduce the solution to a simple algebraic
equation so turned to Python to help me craft a 'brute force'
approach.

Keenan Vance Wilcox brought up the valid point that in its first
incarnation, this script assumed diameters would be submitted in
inches and log length in feet. As a result the code is being modified
to be unit independent. (Use of ft/inches is provided as an option.)

[1] What I really need is "center of gravity" but let's assume the
two are the same (although in the event of rot or other factors they
may well not be.)
"""


import sys
import math
import docopt
from code import helpers
import distance

TOLLERANCE = 1/12  # 1/12th of what ever unit is chosen
SCREEN_WIDTH = 80


def volume(length, d1, d2):
    """
    Returns the volume of a log of <length>
    and diameters at each of the two ends (<d1> & <d2>.)
    """
    radius = (d1 + d2)/4  # we want to work with radii
    return math.pi * radius**2 * length


def get_diameter_at_l(l, length, d1, d2):
    if d1 > d2:
        d1, d2 = d2, d1
    return d1 + l / length * (d2 - d1)


def volume_centre(length, d1, d2):
    half_volume = volume(length, d1, d2)/2
    len = length/2
    vol = 0
    while vol < half_volume:  # {Keep checking along length
        len += TOLLERANCE     # {until we get to half the volume.
        vol = volume(len, d1, get_diameter_at_l(len, length, d1, d2))
    return len


def main():
    """
    The 'probable' center of gravity is likely at
    (or near) the distance (from one end) returned.
    """
    fail = False
    for arg in ('--d1', '--d2', '--len'):
        if not args[arg]:
            fail = True
            print("Must provide a value for '{}'."
                    .format(arg))
    if fail:
        print("Aborting for lack of arguments!")
        sys.exit()
    use_feet_inches = args['-i']
    length = float(args['--len'])
#   print('len is {:.2f}'.format(length))
    d1 = float(args['--d1'])
#   print('d1 is {:.2f}'.format(d1))
    d2 = float(args['--d2'])
#   print('d2 is {:.2f}'.format(d2))
    if use_feet_inches:
        length = length * 12
#       print('len (in inches) is {:.2f}'.format(length))
    answer = length - volume_centre(length, d1, d2)
    if use_feet_inches:
        feet, fraction = divmod(answer, 12)
        inches, numerator = divmod(fraction*12, 16)
        feet = int(feet)
        inches = int(inches)
        numerator = int(numerator)
        denominator = 16
#       print("Types are.. feet: {}, inches: {}, num: {}, denom: {}"
#               .format(type(feet), type(inches),
#                   type(numerator), type(denominator)))
        while True:
            num1, rem1 = divmod(numerator, 2)
            num2, rem2 = divmod(denominator, 2)
            if rem1 or rem2:
                break
            else:
                numerator = num1//2
                denominator = num2//2
        if numerator:
            print(
            'Center of gravity is (>=) {}ft, {}-{}/{}"from larger end.'
                .format(feet, inches, numerator, denominator))
        else:
            print(
            'Center of gravity is (>=) {}ft, {}"from larger end.'
                .format(feet, inches))
    else:
        print(
            "Center of gravity is (>=) {:.2f} units from larger end."
                  .format(answer))


if __name__ == "__main__":
    args = docopt.docopt(__doc__, version='0.1.0')
    helpers.print_args(args, '-O')
    if args['-?']:
        helpers.print_usage_and_options(__doc__)
    main()
