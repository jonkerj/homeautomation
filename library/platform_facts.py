#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import json
import platform

def main():
	module = AnsibleModule(argument_spec={})
	facts = {}
	facts['platform_system'] = platform.system()
	facts['platform_machine'] = platform.machine()
	facts['platform_bits'] = int(platform.architecture()[0].replace('bit', ''))
	print(json.dumps({'ansible_facts': facts}))

if __name__ == '__main__':
	main()
