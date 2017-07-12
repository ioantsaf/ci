from __future__ import absolute_import

import os
import sys

from flask import Flask, render_template, jsonify, url_for, request
from mkcelery import make_celery

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ansible'))
from ansible_manager import run_playbook

app = Flask(__name__)
rabbitmq = 'amqp://guest:guest@localhost:5672' # TODO
app.config.update(
    CELERY_BROKER_URL=rabbitmq,
    CELERY_RESULT_BACKEND=rabbitmq
)
celery = make_celery(app)


@celery.task(bind=True)  # https://blog.miguelgrinberg.com/post/using-celery-with-flask
def deploy_ci_task(self, host_list, vars):
    playbook_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ansible'))
    playbook = os.path.join(playbook_dir, "deploy-ci.yml")
    deploy_ci_stages = ['ci', 'docker', 'jenkins', 'mysql', 'sonarqube', 'apache']
    deploy_ci_messages = ['Initializing CI VM', 'Setting up docker', 'Setting up jenkins',
                          'Setting up mysql', 'Setting up sonarqube',
                          'Setting up apache reverse proxy']
    result = 0
    ci_pubkey = None
    for i, (stage, message) in enumerate(zip(deploy_ci_stages, deploy_ci_messages)):
        vars['deploy_ci_stage'] = stage
        self.update_state(state='STARTED',
                          meta={'current': i, 'total': len(deploy_ci_stages),
                                'message': message, 'ci_pubkey': ci_pubkey})
        result, tmp_pubkey = run_playbook(playbook, host_list, vars)
        if result != 0:
            if result == 2:
                error = 'Task failed'
            elif result == 4:
                error = 'Unreachable host'
            else:
                error = 'Unknown'
            raise Exception('Failed at: ' + message + '. Reason: ' + error +
                            '. For more info, consult Celery log.')
        if tmp_pubkey is not None:
            ci_pubkey = tmp_pubkey
    return result


@app.route('/')
def index():
    return render_template('index.html', pubkey=get_pub_key())


def get_pub_key():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'id_rsa.pub')
    if os.path.isfile(path):
        with open(path) as pub_key:
            res = pub_key.readline()
    else:
        res = "No private-public keypair exists on this host, on the current user. " \
              "Please use ssh-keygen, to generate a keypair."
    return res


@app.route('/deploy-ci', methods=['POST'])
def deploy_ci():
    host_list = {'ci': request.form['ci_host']}
    vars = {'app_name': request.form['app_name'], 'app_type': request.form['app_type'],
            'ci_user': request.form['ci_user'], 'mysql_root_pass': request.form['mysql_root_pass'],
            'mysql_sonar_pass': request.form['mysql_sonar_pass'],
            'staging_host': request.form['staging_host'],
            'staging_user': request.form['staging_user'],
            'production_host': request.form['production_host'],
            'production_user': request.form['production_user']}
    task = deploy_ci_task.apply_async(args=[host_list, vars])
    return jsonify({}), 202, {'status_url': url_for('taskstatus', task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = deploy_ci_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'message': 'Pending...'
        }
    elif task.state == 'STARTED':
        response = {
            'state': task.state,
            'current': task.info['current'],
            'total': task.info['total'],
            'message': task.info['message'],
            'ci_pubkey': task.info['ci_pubkey']
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'message': 'Complete',
        }
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'message': str(task.info).replace('()', '')
        }
    return jsonify(response)
