#!/usr/bin/env python
from collections import namedtuple

from ansible import constants as constants
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.inventory.group import Group
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager


def run_playbook(playbook, host_list, vars):
    # https://github.com/celery/billiard/issues/189
    # https://github.com/Mirantis/kostyor-openstack-ansible/commit/407ec033514600cd62f4931f199efd13405b0aae
    import multiprocessing
    import billiard
    multiprocessing.Process = billiard.Process

    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
                                     'module_path', 'forks', 'remote_user', 'private_key_file',
                                     'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                     'scp_extra_args', 'become', 'become_method', 'become_user',
                                     'verbosity', 'check', 'diff'])
    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)

    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False,
                      connection='ssh', module_path=None, forks=100, remote_user=None,
                      private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                      sftp_extra_args=None, scp_extra_args=None, become=False, become_method='sudo',
                      become_user='root', verbosity=None, check=False, diff=False)
    passwords = {}

    inventory = InventoryManager(loader=loader)
    inventory.add_group('ci')
    inventory.add_host(host_list.values()[0], 'ci')
    inventory.reconcile_inventory()

    variable_manager.set_inventory(inventory)
    variable_manager.extra_vars = vars
    playbook_path = playbook

    constants.HOST_KEY_CHECKING = False

    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory,
                            variable_manager=variable_manager, loader=loader, options=options,
                            passwords=passwords)

    results = pbex.run()
    pubkey = None
    try:
        pubkey = variable_manager._nonpersistent_fact_cache[host_list['ci']]['pubkey']['stdout']
    except KeyError:
        pass
    return results, pubkey


if __name__ == "__main__":
    host_list = {'ci': 'cihost'}
    vars = {'app_name': 'testapp', 'app_type': 'nodejs', 'ci_user': 'dummyuser0',
            'mysql_pass': 'changeme',
            'staging_host': 'dummyhost1', 'staging_user': 'dummyuser1',
            'production_host': 'dummyhost2', 'production_user': 'dummyuser2'}
    vars['deploy_ci_stage'] = 'ci'

    run_playbook("deploy-ci.yml", host_list, vars)
