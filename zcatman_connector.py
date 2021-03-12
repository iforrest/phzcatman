# File: zcatman_connector.py
# Copyright (c) 2020-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------
# Phantom sample App Connector python file
# -----------------------------------------

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault

# Usage of the consts file is recommended
# from zcatman_consts import *
import requests
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import tarfile
import glob
import os
import json
from base64 import b64encode
import uuid
import time

class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class ZcatmanConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(ZcatmanConnector, self).__init__()

    def _rest_call(self, base_url, endpoint, method="get", headers=None, params=None, data=None, json=None, github_download=False, use_auth=False):
        try:
            request_method = getattr(requests, method)
        except AttributeError:
            return False, 'invalid method: {}'.format(method)

        url = '{base_url}{endpoint}'.format(base_url=base_url, endpoint=endpoint)

        response_data = None

        self.debug_print('URLY', url)

        auth=None
        if use_auth:
            config = self.get_config()
            auth = (config['phantom_username'], config['phantom_password'])
            headers = None
        
        try:
            r = request_method(
                url,
                headers=headers,
                verify=False,
                params=params,
                data=data,
                auth=auth,
                json=json,
            )
            r.raise_for_status()
            if not(github_download):
                response_data = r.json()
            else:
                response_data = r.content

        except requests.exceptions.HTTPError as http_error:
            return False, 'http error: {}'.format(http_error)
        except requests.exceptions.RequestException as err:
            return False, 'error: {}'.format(err)

        return True, response_data

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("C\'mon man. Roll the dice, and don\'t EVER doubt me again!!!!")
        self.save_progress(r'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\\\//////\\\\\\\\\\\\\\\\\///\\\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\//\\\\\\/\\\\\\\\\\\\\///\\///\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\/\\\\\\\//\\\\\\\\\\\//\\\\\\//\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\/\\\\\/\\\/\\\\\\\\\\\/\\\//\\\//\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\\/\\\\\/\\\/\\\\\\\\\\\/\\\//\\\\/\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\//\\\\\\/\\\/\\\\\\\\\\\/\\\//\\\\/\/\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\/\\\\\\/\\\/\\\\\\\\\\/\\\\//\\\\//\\\/\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\/\\\\\//\\\/\\\\\\\\\\//\\\//\\\\/\\\\/\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\\/\\\\\\\\//\\\\\\\\\\//\\\/\\\\\/\\\\/\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\\//\\\\\\///\\\\\\\\\///\\\\\\\\/\\\\\/\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\\\//\\\\/\\\\\\\\\\\\\\\//\\\\\/\\\\\//\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\//\\\\\\\////\\\\\\\\\\\\\\\\\\/////\\\\\\//\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\//\\\\\\\\\\\\\\\\////////\\\\\\\\\\\\\\\\\/\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\//\\\\\\\\\\\\\\\\\//\/\\\\\\\\\\\\\\\\\//\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\//\\\\\\\\\\\\\\\\\\//\\\\\\\\\\\\\\\\\\//\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\//\\\\\\\\\\\\\\\\\\//\\\\\\\\\\\\\\\\///\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\//\/\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\///\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\///\\\\/\\\\\\\\/////\\\\\\\\\\\\\\///\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\//\\/\\\\//////\\\\\////\\//\\\\/\//\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\//\/\/\\\\\/\/\\/\\/\/\\\\\\/\\///\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\/////\//\\/\//\/\\/\/\\/\\\/\\//\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\\\//\///\\///\/\////\\/\/////\\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\\\\\\/\//\/\/\/\/\/\\\/\///\\\\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\\\\\\\\\/\/\/\\\/\///\/\\\\\\\\\\\\\\\\\\\\\ ')
        self.save_progress(r'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ')
        return action_result.set_status(phantom.APP_SUCCESS, "C\'mon man. Roll the dice, and don\'t EVER doubt me again!!!!")

    def get_phantom_base_url_formatted(self):
        config = self.get_config()
        phantom_base_url = config['phantom_base_url']
        if phantom_base_url.endswith('/'):
            phantom_base_url = phantom_base_url[:-1]
        return phantom_base_url

    def _handle_update_object(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(dict(param)))
        
        status, response = self._get_github_data()
        if not(status):
            return action_result.set_status(phantom.APP_ERROR, response)

        status, untar_response = self._save_github_data(response)
        if not(status):
            return action_result.set_status(phantom.APP_ERROR, response)

        github_path = param['github_path']

        if 'assets/' in  github_path.lower():
            status, response = self.update_an_asset(untar_response, github_path)
        elif 'playbooks/' in github_path.lower():
            status, response = self.update_a_playbook(untar_response, github_path)
        elif 'demo_config__containers/' in github_path.lower():
            status, response = self.update_containers(untar_response, github_path=github_path, single=True)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, 'Whoops. That didn\'t work. If you\'re trying to update a demo_configuration container, you\'ll need to delete it first. Hopefully that won\'t be a requirement forever, but it is for now. Deal with it. Details - {}'.format((str(response) if response else 'None')))
        elif 'compiled_apps/' in github_path.lower():
            status, response = self.update_an_app(untar_response, github_path)

        if not(status):
            return action_result.set_status(phantom.APP_ERROR, 'Unable to load object. Details - {}'.format((str(response) if response else 'None')))

        return action_result.set_status(phantom.APP_ERROR, 'Successfully loaded object.')

    def update_an_asset(self, file_directory, github_path):
        self.save_progress('Loading asset')
        asset_file = glob.glob('{}/*{}'.format(file_directory, github_path))
        if len(asset_file) < 1:
            return False, 'Unable to get asset from github data'

        asset_file_data = None
        with open(asset_file[0], 'r') as asset_file_stream:
            asset_file_data = asset_file_stream.read()

        status, response = self.seek_and_destroy('asset', json.loads(asset_file_data))
        if not(status):
            return status, 'Unable to determine existence of asset. Details - {}'.format(str(response) if response else 'None')

        asset_status, asset_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/asset', data=asset_file_data, headers=self.phantom_header, method='post')
        if not(asset_status):
            return asset_status, 'Unable to load assets. File - {}. Details - {}'.format(file_, (str(asset_response) if asset_response else 'None'))

        return True, 'Asset successfully loaded'

    def update_a_playbook(self, file_directory, github_path):
        self.save_progress('Loading playbook')
        playbook_file = glob.glob('{}/*{}'.format(file_directory, github_path))
        if len(playbook_file) < 1:
            return False, 'Unable to get playbok from github data'

        playbook_file_data = None
        with open(playbook_file[0], 'rb') as playbook_file_stream:
            playbook_file_data = playbook_file_stream.read()

        playbook_file_data = b64encode(playbook_file_data)
        payload = {'playbook': playbook_file_data.decode('utf-8'), 'scm': 'local', 'force': True}
        status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/import_playbook', json=payload, headers=self.phantom_header, method='post')
        if not(status):
            return status, 'Unable to load playbook. Details - {}'.format((str(response) if response else 'None'))

        return True, 'Successfully loaded playbook'

    def update_an_app(self, file_directory, github_path):
        self.save_progress('Loading app')
        app_file = glob.glob('{}/*{}'.format(file_directory, github_path))
        if len(app_file) < 1:
            return False, 'Unable to get app from github data'

        app_file_data = None
        with open(app_file[0], 'rb') as app_file_stream:
            app_file_data = app_file_stream.read()

        app_file_data = b64encode(app_file_data)
        payload = {'app': app_file_data.decode('utf-8')}
        try:
            status, app_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/app', method='post', json=payload, headers=self.phantom_header)
        except Exception as err:
            return False, 'Unable to install app. File - {}. Details - {}'.format(file_, (str(app_response) if app_response else 'None'))

        return True, 'Successfully updated app.'

    def _get_github_data(self):
        self.save_progress('Retrieving github demo data')
        config = self.get_config()

        github_header = {}

        if config.get('github_personal_access_token'):
            github_header = {
                'Authorization':
                'token {}'.format(config['github_personal_access_token'])
            }

        github_base_url = config['github_base_url']
        if github_base_url.endswith('/'):
            github_base_url = github_base_url[:-1]
        
        github_repo_path = config['github_repo_path']
        if not(github_repo_path.startswith('/')):
            github_repo_path = '/{}'.format(github_repo_path)
        if github_repo_path.endswith('/'):
            github_repo_path = github_repo_path[:-1]

        github_tarball_path = config['github_tarball_path']
        if not(github_tarball_path.startswith('/')):
            github_tarball_path = '/{}'.format(github_tarball_path)
        if github_tarball_path.endswith('/'):
            github_tarball_path = github_tarball_path[:-1]
        
        github_endpoint = '/repos{}{}'.format(github_repo_path, github_tarball_path)

        status, response = self._rest_call(
            github_base_url,
            github_endpoint,
            headers=github_header,
            github_download=True
        )

        return status, response

    def _save_github_data(self, content):
        self.save_progress('Unpacking github demo data')
        tmp_vault_directory = Vault.get_vault_tmp_dir()
        unique_id = uuid.uuid4()

        file_path = '{}/{}'.format(tmp_vault_directory, unique_id)
        print(file_path)
        try:
            with open('{}.tar'.format(file_path), 'wb') as tarball:
                tarball.write(content)
            tf = tarfile.open('{}.tar'.format(file_path), mode="r")
            tf.extractall(path='{}'.format(file_path))
            tf.close()
        except Exception as err:
            return False, 'Error occurred unpacking tarball. Details - {}'.format(err.message)
        
        return True, file_path

    def update_containers(self, file_directory, github_path='demo_config__containers', single=False, do_not_destroy=False):
        demo_container_dir = glob.glob('{}/*/{}'.format(file_directory, github_path))
        if len(demo_container_dir) < 1:
            return False, 'Unable to get demo_config__conatiners from github data'

        if 'demo_config' in github_path:
            parameters = {
                '_filter_label__iexact': '"demo_configuration"',
                'page_size': 0
            }
            if not(single) and not(do_not_destroy): 
                status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/container', headers=self.phantom_header, params=parameters)
                if not(status):
                    return False, 'Unable to retrieve demo_configuration containers. Details - {}'.format(str(response) if response else 'None')

                for container in response['data']:
                    status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/container/{}'.format(container['id']), headers=self.phantom_header, method='delete')
                    if not(status):
                        return False, 'Unable to delete demo_configuration containers. Details - {}'.format(str(response) if response else 'None')

        last_file = None
        for root, dirs, files in os.walk(demo_container_dir[0]):
            for file_ in files:
                if root.endswith('vault'):
                    vault_contents = None
                    with open(os.path.join(root, file_), 'rb') as vault_file:
                        vault_contents = vault_file.read()
                    serialized_contents = b64encode(vault_contents)
                    attachment_json = {
                        'container_id': last_file,
                        'file_content': serialized_contents.decode('utf-8'),
                        'file_name': file_
                    }
                    status, vault_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/container_attachment', method='post', json=attachment_json, headers=self.phantom_header)
                    if not(status):
                        return False, 'Unable to upload vault data. File - {}. Details - {}'.format(file_, (str(vault_response) if vault_response else 'None'))
                elif '.json' in file_ and not(root.endswith('vault')):
                    container_data = None
                    with open(os.path.join(root, file_), 'r') as container_file:
                        container_data = container_file.read()

                    json_container_data = json.loads(container_data)

                    if 'demo_config' not in github_path and not(do_not_destroy):
                        self.seek_and_destroy('seed_containers', json_container_data)

                    json_container_artifacts = json_container_data.get('artifacts', [])
                    json_container_data = json_container_data['container']
                    if 'id' in json_container_data:
                        json_container_data.pop('id')
                    if 'ingest_app_id' in json_container_data:
                        json_container_data.pop('ingest_app_id')
                    if 'asset_id' in json_container_data:
                        json_container_data.pop('asset_id')
                    if 'current_phase_id' in json_container_data:
                        json_container_data.pop('current_phase_id')
                    for artifact in json_container_artifacts:
                        if 'id' in artifact:
                            artifact.pop('id')
                        if 'ingest_app_id' in artifact:
                            artifact.pop('ingest_app_id')
                    json_container_data['artifacts'] = json_container_artifacts
                    
                    status, container_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/container', method='post', headers=self.phantom_header, json=json_container_data)
                    if not(status):
                        return False, 'Unable to upload container data. File - {}. Details - {}/{}'.format(root,file_, (str(container_response) if container_response else 'None'))
                    last_file = container_response['id']

        return True, 'Successfully loaded demo_configuration container data'

    def update_apps(self, file_directory):
        apps_dir = glob.glob('{}/*/compiled_apps'.format(file_directory))
        if len(apps_dir) < 1:
            return False, 'Unable to get compiled_apps from github data'

        for root, dirs, files in os.walk(apps_dir[0]):
            for file_ in files:
                app_file_data = None
                with open(os.path.join(root, file_), 'rb') as app_file:
                    app_file_data = app_file.read()
                app_file_data = b64encode(app_file_data)
                payload = {'app': app_file_data.decode('utf-8')}
                
                status, app_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/app', method='post', json=payload, headers=self.phantom_header)
                if not(status):
                    return False, 'Unable to install app. File - {}. Details - {}'.format(file_, (str(app_response) if app_response else 'None'))
        
        return True, 'Successfully loaded apps'

    def update_roles(self, file_directory):
        roles_dir = glob.glob('{}/*/roles'.format(file_directory))
        if len(roles_dir) < 1:
            return True, 'Roles not found in github'
        for root, dirs, files in os.walk(roles_dir[0]):
            for file_ in files:
                role_file_data = None
                with open(os.path.join(root, file_), 'rb') as role_file:
                    role_file_data = role_file.read()
                self.seek_and_destroy('roles', json.loads(role_file_data))
                
                status, role_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/role', method='post', json=json.loads(role_file_data), use_auth=True)
                if not(status):
                    return False, 'Unable to load role. File - {}. Details - {}'.format(file_, (str(role_response) if role_response else 'None'))
        
        return True, 'Successfully loaded roles'

    def update_users(self, file_directory):
        users_dir = glob.glob('{}/*/users'.format(file_directory))
        if len(users_dir) < 1:
            return True, 'Users not found in github data'

        for root, dirs, files in os.walk(users_dir[0]):
            for file_ in files:
                user_file_data = None
                with open(os.path.join(root, file_), 'rb') as user_file:
                    user_file_data = user_file.read()
                self.seek_and_destroy('users', json.loads(user_file_data))
                try:
                    status, user_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/ph_user', method='post', data=user_file_data, use_auth=True)
                except Exception as err:
                    return False, 'Unable to load user. File - {}. Details - {}'.format(file_, (str(user_response) if user_response else 'None'))
        
        return True, 'Successfully loaded users'

    # def live_replace(self, object_data_as_string):
    #     regex = r"\|\|([A-z\_0-9\:]+)\|\|"
    #     matches = re.finditer(regex, object_data_as_string, re.MULTILINE)
    #     for match in matches:
    #         if len(match.groups()) == 1:
    #             placeholder = match.group(0)
    #             placeholder_parts = placeholder.split('__')
    #             endpoint = placeholder[0]
    #             field = placeholder[1].split(':')
    #             value = field[1]
    #             field = field[0]
    #             filter_params = {
    #                 '_filter_{}__iexact'.format().field: '"{}"'.format(value)
    #             }
    #             status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/{}'.format(endpoint), method='get', params=filter_params, use_auth=True)
    #             if not(status):
    #                 return status, 'Unable to live replace values - {} {} {}'.format(endpoint, field, value)
    #             replacement_value = response['data'][0][placeholder[1]]
    #             object_data_as_string.replace(match.group(0), replacement_value)



    def seek_and_destroy(self, object_type, object_data, do_not_destroy=False):
        filter_params = None
        endpoint = None 
        use_auth=False
        
        if object_type == 'asset':
            filter_params = {
                '_filter_name__iexact': '"{}"'.format(object_data['name'])
            }
            endpoint= '/rest/asset'

        if object_type == 'response_template':
            filter_params = {
                '_filter_name__iexact': '"{}"'.format(object_data['name'])
            }
            endpoint = '/rest/workflow_template'
        elif object_type == 'demo_config__containers':
            filter_params = {
                '_filter_id': '{}'.format(object_data['container_id'])
            }
            endpoint = '/rest/container'

        if object_type == 'seed_containers':
            filter_params = {
                '_filter_name__iexact': '"{}"'.format(object_data['container']['name'])
            }
            endpoint = '/rest/container'

        if object_type == 'roles':
            filter_params = {
                '_filter_name__iexact': '"{}"'.format(object_data['name'])
            }
            endpoint = '/rest/role'
            use_auth=True

        if object_type == 'users':
            filter_params = {
                '_filter_username__iexact': '"{}"'.format(object_data['username'])
            }
            endpoint = '/rest/ph_user'
            use_auth=True

        status, response = self._rest_call(self.get_phantom_base_url_formatted(), endpoint, params=filter_params, headers=self.phantom_header, use_auth=True)
        if not(status):
            return status, 'Unable to search for existance of object. Details - {}'.format((str(response) if response else 'None'))

        if do_not_destroy:
            return status, response['data']

        if len(response['data']) == 1:
            status, response = self._rest_call(self.get_phantom_base_url_formatted(), '{}/{}'.format(endpoint, response['data'][0]['id']), headers=self.phantom_header, method='delete', use_auth=True)
            if not(status):
                return status, 'Unable to delete existing object. Details - {}'.format((str(response) if response else 'None'))

        return True, 'Successfully sought and destroyed'

    def update_assets(self, file_directory):
        config = self.get_config()
        assets_dir = glob.glob('{}/*/assets'.format(file_directory))
        if len(assets_dir) < 1:
            return False, 'Unable to get assets from github data'

        for root, dirs, files in os.walk(assets_dir[0]):
            for file_ in files:
                with open(os.path.join(root, file_), 'r') as asset_file:
                    asset_file_data = asset_file.read()
                status, response = self.seek_and_destroy('asset', json.loads(asset_file_data))
                if not(status):
                    return status, 'Unable to check existance asset data. File - {}. Details - {}'.format(file_, response)
                asset_file_data = asset_file_data.replace('$$$PH_AUTH_TOKEN$$$', config['phantom_api_key']).replace('$$$PH_SERVER_NAME$$$', self.get_phantom_base_url_formatted().replace('https://', '').replace('http://', ''))
                asset_status, asset_response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/asset', data=asset_file_data, headers=self.phantom_header, method='post')
                if not(asset_status):
                    return asset_status, 'Unable to load assets. File - {}. Details - {}'.format(file_, (str(asset_response) if asset_response else 'None'))

        return True, 'Successfully loaded assets'


    def update_custom_functions(self, file_directory):
        custom_function_dir = glob.glob('{}/*/custom_functions'.format(file_directory))
        if len(custom_function_dir) < 1:
            return False, 'Unable to get custom_functions from github data'

        for root, dirs, files in os.walk(custom_function_dir[0]):
            for file_ in files:
                with open(os.path.join(root, file_), 'rb') as custom_function_file:
                    custom_function_file_data = custom_function_file.read()
                custom_function_file_data = b64encode(custom_function_file_data)
                payload = {'custom_function': custom_function_file_data.decode('utf-8'), 'scm': 'local', 'force': True}
                status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/import_custom_function', json=payload, headers=self.phantom_header, method='post')
                if not(status):
                    return status, 'Unable to load custom_function. File - {}. Details - {}'.format(file_, (str(response) if response else 'None'))

        return True, 'Successfully loaded custom_functions'

    def update_playbooks(self, file_directory):
        playbooks_dir = glob.glob('{}/*/playbooks'.format(file_directory))
        if len(playbooks_dir) < 1:
            return False, 'Unable to get playbooks from github data'

        for root, dirs, files in os.walk(playbooks_dir[0]):
            for file_ in files:
                with open(os.path.join(root, file_), 'rb') as playbook_file:
                    playbook_file_data = playbook_file.read()
                playbook_file_data = b64encode(playbook_file_data)
                payload = {'playbook': playbook_file_data.decode('utf-8'), 'scm': 'local', 'force': True}
                status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/import_playbook', json=payload, headers=self.phantom_header, method='post')
                if not(status):
                    return status, 'Unable to load playbooks. File - {}. Details - {}'.format(file_, (str(response) if response else 'None'))

        return True, 'Successfully loaded playbooks'

    def update_response_templates(self, file_directory):
        response_templates_dir = glob.glob('{}/*/response_templates'.format(file_directory))
        if len(response_templates_dir) < 1:
            return True, 'No response templates to get'

        for root, dirs, files in os.walk(response_templates_dir[0]):
            for file_ in files:
                with open(os.path.join(root, file_), 'r') as response_template_file:
                    response_template_data = response_template_file.read()
                status, response = self.seek_and_destroy('response_template', json.loads(response_template_data), do_not_destroy=True)
                if not(status):
                    return status, 'Unable to check existence of response template. File - {}. Details - {}'.format(file_, (str(response) if response else 'None'))
                workflow_template_id = ''
                if len(response) > 0:
                    workflow_template_id = '/{}'.format(response[0]['id'])
                status, response = self._rest_call(self.get_phantom_base_url_formatted(), '/rest/workflow_template{}'.format(workflow_template_id), data=response_template_data, headers=self.phantom_header, method='post')
                if not(status):
                    return status, 'Unable to load response templates. File - {}. Details - {}'.format(file_, (str(response) if response else 'None'))

        return True, 'Successfully loaded response templates'

    def _handle_load_demo_data(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(dict(param)))
        
        status, response = self._get_github_data()
        if not(status):
            return action_result.set_status(phantom.APP_ERROR, response)

        status, untar_response = self._save_github_data(response)
        if not(status):
            return action_result.set_status(phantom.APP_ERROR, response)
        
        object_list = ['roles', 'users', 'assets', 'compiled_apps', 'demo_config__containers', 'playbooks', 'response_templates', 'seed_containers', 'custom_functions']
        object_types = param.get('object_types', '').split(',')
        exclude_object_list = param.get('excluded_object_types', '').split(',')

        if len([type_ for type_ in object_types if type_]) > 0:
            object_list = [type_.strip().lower() for type_ in object_types if type_]
        
        object_list = [type_ for type_ in object_list if type_ not in [item.strip().lower() for item in exclude_object_list]]

        summary = {}

        if 'roles' in object_list:
            self.save_progress('Loading role data')
            status, message = self.update_roles(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['roles_message'] = message

        if 'users' in object_list:
            self.save_progress('Loading user data')
            status, message = self.update_users(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['users_message'] = message

        if 'demo_config__containers' in object_list:
            self.save_progress('Loading demo configuration container data')
            status, message = self.update_containers(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['demo_config__containers_message'] = message

        if 'compiled_apps' in object_list:
            self.save_progress('Loading demo app data')
            status, message = self.update_apps(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['compiled_apps_message'] = message

        if 'assets' in object_list:
            self.save_progress('Loading demo asset data')
            status, message = self.update_assets(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['assets_message'] = message

        if 'playbooks' in object_list:
            self.save_progress('Loading demo playbook data')
            status, message = self.update_playbooks(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['playbooks_message'] = message

        if 'custom_functions' in object_list:
            self.save_progress('Loading demo custom function data')
            status, message = self.update_custom_functions(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['custom_functions_message'] = message

        if 'response_templates' in object_list:
            self.save_progress('Loading response templates')
            status, message = self.update_response_templates(untar_response)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['response_templates_message'] = message

        if 'seed_containers' in object_list:
            self.save_progress('Loading seed container data')
            status, message = self.update_containers(untar_response, github_path='seed_containers', do_not_destroy=False)
            if not(status):
                return action_result.set_status(phantom.APP_ERROR, message)
            summary['seed_containers_message'] = message

        action_result.update_summary(summary)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully loaded phantom demo data")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_vms':
            ret_val = self._handle_list_vms(param)

        elif action_id == 'update_object':
            ret_val = self._handle_update_object(param)

        elif action_id == 'load_demo_data':
            ret_val = self._handle_load_demo_data(param)

        return ret_val

    def initialize(self):
        config = self.get_config()
        self.phantom_header = {
            'ph-auth-token': config['phantom_api_key']
        }

        return phantom.APP_SUCCESS

    def finalize(self):
        return phantom.APP_SUCCESS


def main():
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = ZcatmanConnector._get_phantom_base_url_formatted() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = ZcatmanConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
