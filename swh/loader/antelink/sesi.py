# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Tryout module to check existence of file in s3 using ssh."""

import subprocess


def check_file_exists(path):
    cmd = ('ssh sesipvlc2 file %s' % path).split(' ')
    try:
        subprocess.check_call(cmd)
        return True
    except:
        return False
