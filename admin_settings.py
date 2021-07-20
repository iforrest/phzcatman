# File: admin_settings.py
# Copyright (c) 2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.import os
import sys
import encryption_helper
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phantom_ui.settings')

import django
django.setup()
from phantom_ui.ui.models import SystemSettings, PhUser, SCM
from phantom_ui.phplaybooks import git_helper

phantom_key=sys.argv[1]
phantom_ip=sys.argv[2]
git_user=sys.argv[3]
git_pass=sys.argv[4]

ss = SystemSettings.get_settings()
ss.environment_variables = {
    'PHANTOM_API_KEY': {'type': 'password', 'value': encryption_helper.encrypt(phantom_key, 'PHANTOM_API_KEY')},
    'NO_PROXY': {'type': 'text', 'value': '127.0.0.1,localhost'}
}
ss.administrator_contact = 'newadmin@localhost'
ss.company_name = 'Splunk'
ss.system_name = 'SOS_Demo'
ss.eula_accepted = True
ss.fqdn = phantom_ip
ss.save(ignore_rabbit_error=True)

admin_user = PhUser.objects.get(username='admin')
admin_user.profile.onboarding_state = {'redirect_onboarding': False}
admin_user.profile.save()
admin_user.save()

scm = SCM()
scm.name = 'internal-oar-content'
scm.uri = 'https://github.com/splunk/internal-oar-content'
scm.branch = 'sos_demo'
scm.read_only = True
scm.repo_user = git_user
scm.repo_pass = encryption_helper.encrypt(git_pass, scm.uri)
scm.save()
git_helper.pull(scm, None, True)
