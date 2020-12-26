#!/usr/bin/env python3

import sys
from gimkit import *

if __name__ == '__main__':
  join_game(sys.argv[1], sys.argv[2])
  play()
