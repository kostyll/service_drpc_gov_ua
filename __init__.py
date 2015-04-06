#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import drpc_gov_ua
print (dir(drpc_gov_ua))
from drpc_gov_ua import register

registered_classes = register()

for registered_class in registered_classes:
    setattr(sys.modules[__name__],registered_class.represent(), registered_class)
