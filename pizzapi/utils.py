import requests
import xmltodict
from time import sleep

# TODO: Find out why this occasionally hangs
def request_json(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    #Testing a sleeper to see if this function is being to aggressive
    sleep(2)
    return r.json()


def request_xml(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    return xmltodict.parse(r.text)
