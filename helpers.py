import json
import os
from urllib.parse import urlsplit, urlunsplit

import requests
from config import SLACK_ERROR_URL, SLACK_URL


def print_to_slack(txt, error=False):
    if os.environ.get('NO_SLACK_POST'):
        print(txt)
        return
    data = {'text': txt}
    if not error:
        requests.post(url=SLACK_URL, json=data)
    else:
        requests.post(url=SLACK_ERROR_URL, json=data)
