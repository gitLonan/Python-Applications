import json, urllib.request, time

class Network_communication:

    def url_access(url):
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
            status_code = response.getcode()
            if status_code == 200:
                return body