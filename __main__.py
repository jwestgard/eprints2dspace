#!/usr/bin/env python3

import argparse
from eprints import Eprint
from dspace import SafPackage
import pyyaml



if __name__ == "__main__":
    
    e = Eprint(10)
    print(e, e.id)

    saf = SafPackage('foobar/')
    print(saf.packagedir)
