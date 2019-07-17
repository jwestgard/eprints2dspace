import os
import sys
#from ..load import DublinCoreXML

print(sys.path)
sys.path.append(os.path.join(sys.path[0], '..'))
print(sys.path)

from load import DublinCoreXML

print(DublinCoreXML)
