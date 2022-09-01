import requests


def mac(bssid):
    return requests.get(f'http://macvendors.co/api/{bssid}')
