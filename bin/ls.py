#!/usr/bin/env python3

import os
import sys

if __name__ == '__main__':
    for path in sys.stdin:
        path = path.rstrip()
        print(path, os.path.getsize(path))
