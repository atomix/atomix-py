# Python client for interacting with Atomix clusters.
from primitives import Map, Set, Value, Counter, Lock

import requests
import requests.exceptions
import json

class AtomixClient(object):
    """Atomix client."""
    def __init__(self, host='127.0.0.1', port=5678):
        self.host = host
        self.port = port

    @property
    def address(self):
        return 'http://{}:{}'.format(self.host, self.port)

    def status(self):
        try:
            response = requests.get(self._format_url('/v1/status'))
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def map(self, name):
        return Map(self, name)

    def set(self, name):
        return Set(self, name)

    def value(self, name):
        return Value(self, name)

    def counter(self, name):
        return Counter(self, name)

    def lock(self, name):
        return Lock(self, name)

    def _format_url(self, *args, **kwargs):
        args = list(args)
        path = args.pop(0)
        return self.address + path.format(*args, **kwargs)

    def _sanitize(self, response):
        if response.status_code == 200 and response.text != '':
            try:
                return json.loads(response.text)
            except:
                return response.text
        elif response.status_code == 200:
            return response.text
        else:
            raise AtomixError("Error code: {}".format(response.status_code))

    def get(self, path, headers=None, *args, **kwargs):
        url = self._format_url(path, *args, **kwargs)
        return self._sanitize(requests.get(url, headers=headers))

    def post(self, path, data=None, headers=None, *args, **kwargs):
        url = self._format_url(path, *args, **kwargs)
        return self._sanitize(requests.post(url, data=data, headers=headers))

    def put(self, path, data=None, headers=None, *args, **kwargs):
        url = self._format_url(path, *args, **kwargs)
        return self._sanitize(requests.put(url, data=data, headers=headers))

    def delete(self, path, headers=None, *args, **kwargs):
        url = self._format_url(path, *args, **kwargs)
        return self._sanitize(requests.delete(url, headers=headers))

class AtomixError(Exception):
    pass
