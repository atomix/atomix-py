class Primitive(object):
    """Atomix distributed primitive."""
    def __init__(self, client, name):
        self.client = client
        self.name = name


class Map(Primitive):
    """Map primitive."""
    def __init__(self, client, name):
        super(Map, self).__init__(client, name)

    def get(self, key):
        return self.client.get('/v1/atomic-map/{name}/{key}', name=self.name, key=key)

    def put(self, key, value):
        return self.client.put('/v1/atomic-map/{name}/{key}', name=self.name, key=key, data=value, headers={'content-type': 'text/plain'})

    def remove(self, key):
        return self.client.delete('/v1/atomic-map/{name}/{key}', name=self.name, key=key)

    def size(self):
        return self.client.get('/v1/atomic-map/{name}/size', name=self.name)

    def clear(self):
        return self.client.delete('/v1/atomic-map/{name}', name=self.name)


class Set(Primitive):
    """Set primitive."""
    def __init__(self, client, name):
        super(Set, self).__init__(client, name)

    def add(self, item):
        return self.client.put('/v1/set/{name}/{value}', name=self.name, value=item)

    def remove(self, item):
        return self.client.delete('/v1/set/{name}/{value}', name=self.name, value=item)

    def contains(self, item):
        return self.client.delete('/v1/set/{name}/{value}', name=self.name, value=item)

    def size(self):
        return self.client.get('/v1/set/{name}/size', name=self.name)

    def clear(self):
        return self.client.delete('/v1/set/{name}', name=self.name)


class Value(Primitive):
    """Value primitive."""
    def __init__(self, client, name):
        super(Value, self).__init__(client, name)

    def get(self):
        return self.client.get('/v1/atomic-value/{name}', name=self.name)

    def set(self, value):
        return self.client.put('/v1/atomic-value/{name}', name=self.name, data=value, headers={'content-type': 'text/plain'})

    def compare_and_set(self, expect, update):
        return self.client.post('/v1/atomic-value/{name}/cas', name=self.name, data={'expect': expect, 'update': update}, headers={'content-type': 'application/json'})


class Counter(Primitive):
    """Counter primitive."""
    def __init__(self, client, name):
        super(Counter, self).__init__(client, name)

    def get(self):
        return self.client.get('/v1/atomic-counter/{name}', name=self.name)

    def set(self, value):
        return self.client.put('/v1/atomic-counter/{name}', name=self.name, data=value, headers={'content-type': 'text/plain'})

    def increment(self):
        return self.client.post('/v1/atomic-counter/{name}/inc', name=self.name)


class Lock(Primitive):
    """Lock primitive."""
    def __init__(self, client, name):
        super(Lock, self).__init__(client, name)

    def lock(self):
        return self.client.post('/v1/atomic-lock/{name}', name=self.name)

    def unlock(self):
        return self.client.delete('/v1/atomic-lock/{name}', name=self.name)
