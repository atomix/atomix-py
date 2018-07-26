from threading import Thread
import time

class AtomixCluster(object):
    """Atomix cluster clinet."""
    def __init__(self, client):
        self.client = client
        self._listeners = {}

    def node(self):
        """Returns the node to which the client is connected."""
        node = self.client.get('/v1/cluster/node')
        return AtomixNode(node['id'], node['host'], node['port'])

    def nodes(self):
        """Returns the list of cluster members."""
        nodes = self.client.get('/v1/cluster/nodes')
        return [AtomixNode(node['id'], node['host'], node['port']) for node in nodes]

    def _poll_events(self, id, listener):
        """Polls for cluster events."""
        while listener in self._listeners:
            try:
                event = self.client.get('/v1/cluster/events/' + id)
                listener(AtomixClusterEvent(event['id'], event['type']))
            except KeyboardInterrupt:
                break
            except:
                time.sleep(1)

    def add_listener(self, listener):
        """Adds a node event listener callback."""
        id = self.client.post('/v1/cluster/events')
        thread = Thread(target=self._poll_events, args=(id, listener))
        self._listeners[listener] = (id, thread)
        thread.start()

    def remove_listener(self, listener):
        """Removes a node event listener callback."""
        if listener in self._listeners:
            id, thread = self._listeners[listener]
            del self._listeners[listener]
            self.client.delete('/v1/cluster/events/' + id)

class AtomixNode(object):
    """Atomix cluster node."""
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port

class AtomixClusterEvent(object):
    """Atomix node event."""
    class Type:
        MEMBER_ADDED = 'MEMBER_ADDED'
        MEMBER_REMOVED = 'MEMBER_REMOVED'
        METADATA_CHANGED = 'METADATA_CHANGED'
        REACHABILITY_CHANGED = 'REACHABILITY_CHANGED'

    def __init__(self, id, type):
        self.id = id
        self.type = type
