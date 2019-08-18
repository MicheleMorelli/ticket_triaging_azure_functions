"""
Testing concurrency non-functional requirement
"""

import threading
import sys
import requests
sys.path.append('../')




def azure_uri() -> str:
    return os.getenv('AZURE_CLASSIFIER_URI')



