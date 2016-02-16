#!/usr/bin/env python3

# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
import sys


def strcount(count):
    if count < 10:
        return '0'+str(count)
    return str(count)


if __name__ == '__main__':
    prefix_name = sys.argv[1]
    if len(sys.argv) > 2:
        count = int(sys.argv[2])
    else:
        count = 1

    for path in sys.stdin:
        path = path.rstrip()

        if os.path.exists(path):
            new_path = prefix_name + '.' + strcount(count) + '.csv'
            os.rename(path, new_path)
            count += 1
