from cms import models
import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))

classes = map(lambda x:x[0], inspect.getmembers(models, inspect.isclass))

print(classes)
