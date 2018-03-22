#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import json
import os.path
import os
import re
import mmap

def findstr(fh, s, offset):
	f = mmap.mmap(fh.fileno(), length=1024*1024, access=mmap.ACCESS_READ)
	f.seek(offset)
	offset_str = f.find(s)
	if offset_str != -1:
		offset_null = f.find('\n', offset_str)
		return f[offset_str:offset_null]
	else:
		return False

def main():
	module = AnsibleModule(argument_spec=dict(
		filename	= dict(required=True),
		offset		= dict(required=True, type=int),
	))

	if not os.path.exists(module.params['filename']):
		module.fail_json(msg='file "{}" does not exist'.format(module.params['filename']))

	version = None
	with open(module.params['filename'], 'rb') as fh:
		version = findstr(fh, 'U-Boot SPL', module.params['offset'])
		if not version:
			module.fail_json(msg='Version string not found')
	
	facts = {}
	if version:
		r = re.compile('^(U-Boot (?:SPL)?) ((\d{4}\.\d{2})(?:-([^ ]+))?) \((.+)\)$')
		m = r.match(version)
		if m:
			facts['uboot_version_string'] = version
			facts['uboot_version_product'] = m.group(1)
			facts['uboot_version_full'] = m.group(2)
			facts['uboot_version_short'] = m.group(3)
			facts['uboot_version_git'] = m.group(4)
			facts['uboot_version_date'] = m.group(5)
		else:
			module.fail_json(msg='No parsable u-boot version found')
	else:
		module.fail_json(msg='No version string found at {}:{}'.format(module.params['filename'], module.params['offset']))
	print(json.dumps({'ansible_facts': facts}))

if __name__ == '__main__':
	main()
