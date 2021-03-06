#!/usr/bin/env python3

# File: gradations.py

"""
Provides a function <heights>
=============================
Given two locations d units apart, each of specified height h0 & h1
and given the need to segment the intervening distance into n parts
we want to know the height of each of the n - 1 locations.
<d> must be an integer.  <h0> and <h1> can be integer or float.

In the following example we have d = 7, h2 = 4, h1 = 11:

     #
     #     |     
     #     |     |     
     #     |     |     |     
     #     |     |     |     |     
     #     |     |     |     |     |     
     #     |     |     |     |     |     |     
     #     |     |     |     |     |     |     #
     #     |     |     |     |     |     |     #
     #     |     |     |     |     |     |     #
     #     |     |     |     |     |     |     #
     
     ^                                         ^   -- Known heights
           ^     ^     ^     ^     ^     ^   -- Unkown heights
Our function "heights(d, h0, h1)" yields an array of d+1 heights
(included are the first and last (h1 & h2) heights we already know):
    	For 7 intervals and heights 4.0 & 11.0
	---------------------------------------
	[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]

"""

problem_d = {'first':
              {'d': 8,
               'h0': 36.5,
               'h1': 50.5,
               },
             'second':
              {'d': 5,
               'h0': 36.5,
               'h1': 21.5,
               },
              } 
            
def heights(d, h0, h1):
    dh = (h1 - h0) / d
    return [(h0 + dh * n) for n in range(d+1)]


def main():
    res = ['',]
    for key in problem_d.keys():
        res.append("    For {d} intervals and heights {h0} & {h1}:"
                .format(**problem_d[key]))
        res.append("      " + repr(heights(problem_d[key]['d'],
                                  problem_d[key]['h0'],
                                  problem_d[key]['h1'])))
        res.append('')
    print('\n'.join(res))


if __name__ == "__main__":
    main()

