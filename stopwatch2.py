#!/usr/bin/env python3

# File: stopwatch2.py

"""
Student Jamie reminded me about the flush option to print(). So we
don't need to invoke sys.stdout.flush(), like I did in the original.
Thanks, Jamie!)
Now, this version has several user-interface problems; you cannot
pause it, the only way to quit is to kill the process (and generate
a stack trace), etc.
I'll ignore those, for something more fundamental...
It does not actually count time well. At all:
1) time.sleep() is not that accurate, first of all; it frequently
goes over the requested time, depending on the OS and other factors.
2) Even if it was, the while-loop takes up (a) the sleep time, PLUS
(b) the time it takes to execute the other lines in the while loop.
Distorting the wait time even further.
3) And there's the process start-up time, which is not zero, and the
time it takes Python to even execute its way to the while loop. This
will distort the first second even more.
How do we make this better?
First of all, I am going for "better", not "perfect". Which would
require a real-time operating system and heroic effort.
Let's go for "pretty good". Like so:
"""

import time
import os

import psutil

def process_start_time():
    return psutil.Process(os.getpid()).create_time()

when = 0
now = process_start_time()

while True:
    minutes, seconds = divmod(when, 60)
    hours, minutes = divmod(minutes, 60)
    print(f'  {hours:02d}:{minutes:02d}:{seconds:02d}',
          end='\r', flush=True)
    when += 1
    time.sleep(1 - (time.time() - now))
    now = time.time()

comments = """
What's happening:
1) I'm using psutil (https://pypi.org/project/psutil/) to check when
the process started, in a cross-platform way. We'll use this to wait
on the first second more correctly.
2) I measure the current timestamp each iteration through the loop,
and use that to calculate a time to wait (rather than naively waiting
one second every time). On any given loop, this may be a bit off, but
if so it will correct itself on the next iteration.
Is this perfect?...  Nope.  There are still imprecisions and small
delays, hiding in the spaces between bytecodes.
But it is absolutely good enough for its intended purpose. Which is
often the right target to aim for when writing code.
"""
