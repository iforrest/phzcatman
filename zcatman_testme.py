# File: zcatman_testme.py
# Copyright (c) 2020-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED. 
# 
# 
# 

from zcatman_connector import ZcatmanConnector

zcm = ZcatmanConnector()

zcm.config = {
    'github_base_url': 'https://api.github.com',
    'github_repo_path': '/iforrest/phantom_demo',
    'github_tarball_path': '/tarball/master',
    'github_personal_access_token': 'a3efc7e9bc35c4ea3439743c41218583673d9a85',
    'phantom_api_key': '89pOLtazM881Be+4NqPTvcQMjBiWwMYYR/p6hzDCAas=',
    'phantom_base_url': 'https://54.89.181.150/',
    'phantom_username': 'admin',
    'phantom_password': 'password1!'
}

zcm.initialize()

zcm.base_url = 'https://172.16.22.138'

zcm.action_identifier = 'load_demo_data'

zcm.handle_action(
    {
        'object_types': 'playbooks,custom_functions'
    }
)