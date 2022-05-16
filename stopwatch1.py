#!/usr/bin/env python3

# File: stopwatch1.py

import time
import sys

when = 0
while True:
    minutes, seconds = divmod(when, 60)
    hours, minutes = divmod(minutes, 60)
    print(f'  {hours:02d}:{minutes:02d}:{seconds:02d}', end='\r')
    sys.stdout.flush()
    when += 1
    time.sleep(1)

