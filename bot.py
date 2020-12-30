#!/usr/bin/env python3

import os
import sys
from gimkit import *

if __name__ == '__main__':
  if os.environ.get("CODE") != None:
    code = os.environ.get("CODE")
  else:
    code = sys.argv[1]
  if os.environ.get("NAME") != None:
    name = os.environ.get("NAME")
  else:
    name = sys.argv[2]
  join_game(code, name)
  play()
