import requests, json

class LTM:
    """A basic class for interacting with F5's Local Traffic
    manager."""

    def __init__(self, hostname, username, password, partition='Common'):
        self.url_base = 'https://%s/mgmt/tm' % hostname
        self.bigip = requests.session()
        self.bigip.auth = (username, password)
        self.bigip.verify = False
        self.bigip.headers.update({'Content-Type': 'application/json'})
        self.partition = partition

    def get_pools(self):
        resp = self.bigip.get('%s/ltm/pool' % self.url_base)
        return resp.json()['items']

    def get_nodes(self):
        resp = self.bigip.get('%s/ltm/node' % self.url_base)
        return resp.json()['items']

    def disable_node(self, node):
        payload = { 'session': 'user-disabled' }
        resp = self.bigip.put('%s/ltm/node/%s' % (self.url_base, node), data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()
    
    def enable_node(self, node):
        payload = { 'session': 'user-enabled' }
        resp = self.bigip.put('%s/ltm/node/%s' % (self.url_base, node), data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    def sync_nodes(self, device_group):
        payload = { 'command': 'run', 'utilCmdArgs': 'confg-sync to-group %s' % device_group }
        resp = self.bigip.post('%s/cm', data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()
