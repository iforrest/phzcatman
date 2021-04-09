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
    'github_repo_path': '/kelby-shelton/phantom_demo_assets',
    'github_tarball_path': '/tarball/default',
    'phantom_api_key': 'acIN3jQHYChKB1LEgL39EiawR74Qhf9xJM6RMcVIvMY=',
    'phantom_base_url': 'https://10.202.32.86/',
    'phantom_username': 'admin',
    'phantom_password': '5up3rn0va'
}

zcm.initialize()

zcm.base_url = 'https://10.202.32.86'

zcm.action_identifier = 'load_demo_data'

zcm.handle_action(
    {
        'object_types': 'assets'
    }
)