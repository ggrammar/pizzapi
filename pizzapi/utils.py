import requests
import xmltodict

# TODO: Find out why this occasionally hangs
def request_json(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    return r.json()


def request_xml(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    return xmltodict.parse(r.text)
