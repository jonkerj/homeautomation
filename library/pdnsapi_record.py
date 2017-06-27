#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import requests
import json

# Low level interface
class PDNSAPI(object):
	def __init__(self, endpoint, token, version):
		self._token = token
		self._uri = endpoint + '/api/{0}'.format(version)
#		print('Initializing {0} with URI {1}'.format(self.__class__.__name__, self._uri))
	
	def request(self, method, uri, data):
		assert method in ('GET', 'PATCH')
		m = getattr(requests, method.lower())
		u = self._uri + uri
#		print('Going for {0}'.format(u))
		return m(
			self._uri + uri,
			json = data,
			headers = {'X-API-Key': self._token}
		)
	
	def server(self, name):
		return Server(self, '/servers/{0}'.format(name), name)

class PDNSObject(object):
	def __init__(self, api, uri, name):
		self._api = api
		self._uri = uri
		self.name = name
#		print('Initializing {0} with URI {1}'.format(self.__class__.__name__, self._uri))
		self._load()

	def _load(self):
		pass
	
	def _api_patch(self, uri, data):
		return self._api.request('PATCH', self._uri + uri, data)
	
	def _api_get(self, uri, data):
		return self._api.request('GET', self._uri + uri, data).json()

class Server(PDNSObject):
	def zones(self):
		for zone in self._api_get('/zones', {}):
			yield self.zone(zone['id'])
	
	def zone(self, name):
		return Zone(self._api, self._uri + '/zones/{0}'.format(name), name)

class Zone(PDNSObject):
	def records(self):
		for rrset in self._api_get('', {})['rrsets']:
			yield rrset['name']
	
	def record(self, relname):
		fqdn = '{0}.{1}'.format(relname, self.name)
		return Record(self._api, self._uri, fqdn)
	
	def set_record(self, relname, typ, ttl, content):
		d = {'rrsets': [{
			'name': '{0}.{1}'.format(relname, self.name),
			'type': typ,
			'ttl': ttl,
			'changetype': 'REPLACE',
			'records': [{
				'content': content,
				'disabled': False,
				'set-ptr': False,
			}],
			'comments': [],
		}]}
		r = self._api_patch('', d)
		return r

	def del_record(self, relname, typ):
		d = {'rrsets': [{
			'name': '{0}.{1}'.format(relname, self.name),
			'type': typ,
			'changetype': 'DELETE',
#			'records': [],
#			'comments': [],
		}]}
		r = self._api_patch('', d)
		return r
	
class Record(PDNSObject):
	def _load(self):
		d = self._api_get('', {})
		for rrset in d['rrsets']:
			if rrset['name'] == self.name:
				self._data = rrset
				return
		raise RuntimeError('Record not present in zone')

def main():
	module = AnsibleModule(argument_spec=dict(
		api		= dict(required=True),
		token		= dict(required=True),
		state		= dict(default='present', choices=['present', 'absent']),
		name		= dict(required=True),
		zone		= dict(required=True),
		ttl		= dict(default=3600, type='int'),
		type		= dict(required=True),
		content		= dict(),
		server		= dict(default='localhost'),
	))

	if module.params['state'] == 'present' and not module.params['content']:
		module.fail_json(msg='Missing field "content"')

	a = PDNSAPI(module.params['api'], module.params['token'], 'v1')
	s = a.server(module.params['server'])
	z = s.zone(module.params['zone'])

	if module.params['state'] == 'present':
		r = z.set_record(module.params['name'], module.params['type'], module.params['ttl'], module.params['content'])
	elif module.params['state'] == 'absent':
		r = z.del_record(module.params['name'], module.params['type'])
	if r.status_code in range(200,300):
		module.exit_json(changed=True, meta={
			'http_status': r.status_code,
		})
	else:
		j = json.loads(r.text)
		module.fail_json(msg='API status {0}, message={1}'.format(r.status_code, j['error']))

if __name__ == '__main__':
	main()
