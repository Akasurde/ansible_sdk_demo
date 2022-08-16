import os
import json
import ansible_runner
import asyncio
import tempfile
import yaml
import configparser

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor
from ansible_sdk.model.job_event import RunnerOnOKEvent

from flask import Flask, render_template, request

loop = asyncio.get_event_loop()
app = Flask(__name__, static_folder='assets', template_folder='templates', instance_relative_config=True)


@app.route("/")
def index():
    filename = os.path.join(app.instance_path, "inventory/virtualbox.yml")
    # filename = os.path.join(app.instance_path, "inventory/gcp_compute.yml")
    hosts = get_inventory(filename=filename)
    return render_template('index.html', hosts=hosts)


@app.route('/ping_host', methods=['POST'])
async def ping_host():
    data = request.get_json()
    d = await run_playbook(data['ipAddress'])
    return {'ipAddress': data['ipAddress'], 'response': d.res, 'success': True}


def create_temp_dir(host):
    tmp_dir = tempfile.mkdtemp(suffix='ansible-sdk')
    datadir_path = os.path.join(tmp_dir, 'datadir')
    for i in ['inventory', 'project']:
        os.makedirs(os.path.join(datadir_path, i), exist_ok=True)

    with open(os.path.join(datadir_path, 'project', 'pb.yml'), 'w') as f:
        f.write(yaml.dump([{'hosts': 'all', 'tasks': [{ 'ping': {} }]}]))

    inventory = configparser.ConfigParser(allow_no_value=True)
    section_name = 'taskhosts'
    inventory.add_section(section_name)
    inventory.set(section_name, host)

    with open(os.path.join(datadir_path, 'inventory', 'hosts'), 'w') as f:
        inventory.write(f)
    
    return datadir_path


async def run_playbook(host):
    executor = AnsibleSubprocessJobExecutor()
    datadir_path = create_temp_dir(host)
    jobdef = AnsibleJobDef(datadir_path, 'pb.yml')

    job_status = await executor.submit_job(jobdef)

    # consume events and accumulate stdout replica
    stdout = ''

    # consume events as they arrive
    eventcount = 0
    result = {'res': {}}
    async for ev in job_status.events:
        eventcount += 1
        if isinstance(ev, RunnerOnOKEvent):
            result = ev
    return result.event_data or {}

def get_inventory(filename=None):
    if not filename:
        return {}

    r = ansible_runner.get_inventory(
            action='list',
            inventories=[filename],
        )
    return json.loads(r[0])["_meta"]["hostvars"]




if __name__ == "__main__":
    app.run(debug=True)
