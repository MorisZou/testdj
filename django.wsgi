

import os
    
from os.path import join,dirname,abspath
  
PROJECT_DIR = dirname(dirname(abspath(__file__)))

    
import sys
   
sys.path.insert(0,'/root/0712/testdj')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



