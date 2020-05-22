# -*- coding: utf-8 -*-
import sys
from application import EDLManagerApp

if __name__ == '__main__':

    application = EDLManagerApp(sys.argv)
    sys.exit(application.run())
