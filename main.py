import os
import json
from unittest import removeHandler
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
app = Flask(
    __name__,
    static_folder="assets",
    template_folder="templates",
    instance_relative_config=True,
)


@app.route("/")
def index():
    filename = os.path.join(app.instance_path, "inventory/gcp_compute.yml")
    hosts = get_inventory(filename=filename)
    return render_template("index.html", hosts=hosts)


@app.route("/powerstate_host", methods=["POST"])
async def manage_powerstate_host():
    data = request.get_json()
    datadir_path = create_temp_dir()
    create_inventory(datadir_path=datadir_path, host=data["ipAddress"])
    print(data['powerstate'])
    create_powerstate_playbook(
        datadir_path=datadir_path,
        **{
            'desired_powerstate': data['powerstate'],
            'machine_name': data['machine_name'],
            'machine_type': data['machine_type'],
            'zone': data['zone'],
            'project': data['project'],
            'service_file': '/Users/akasurde/.gcp_auth',
        }
    )
    d = await run_playbook(datadir_path=datadir_path)
    return {"ipAddress": data["ipAddress"], "response": '', "success": True}

@app.route("/ping_host", methods=["POST"])
async def ping_host():
    data = request.get_json()
    datadir_path = create_temp_dir()
    create_inventory(datadir_path=datadir_path, host=data["ipAddress"])
    create_ping_playbook(datadir_path=datadir_path)
    d = await run_playbook(datadir_path=datadir_path)
    return {"ipAddress": data["ipAddress"], "response": d.res, "success": True}


def create_temp_dir():
    tmp_dir = tempfile.mkdtemp(suffix="ansible-sdk")
    datadir_path = os.path.join(tmp_dir, "datadir")
    for i in ["inventory", "project"]:
        os.makedirs(os.path.join(datadir_path, i), exist_ok=True)

    return datadir_path

def create_powerstate_playbook(datadir_path, **kwargs):

    if kwargs['desired_powerstate'] == 'poweredoff':
        tp_filename = 'powerstate_off.yml'
    else:
        tp_filename = 'powerstate_on.yml'
    powerstate_tp = render_template(
        tp_filename,
        machine_name=kwargs['machine_name'],
        machine_type=kwargs['machine_type'],
        zone=kwargs['zone'],
        project=kwargs['project'],
        service_file=kwargs['service_file'],
        )
    with open(os.path.join(datadir_path, "project", "pb.yml"), "w") as f:
        f.write(powerstate_tp)

def create_ping_playbook(datadir_path):
    ping_tp = render_template('ping.yml')
    with open(os.path.join(datadir_path, "project", "pb.yml"), "w") as f:
        f.write(ping_tp)

def create_inventory(datadir_path, host):
    inventory = configparser.ConfigParser(allow_no_value=True)
    section_name = "taskhosts"
    inventory.add_section(section_name)
    inventory.set(section_name, host)

    with open(os.path.join(datadir_path, "inventory", "hosts"), "w") as f:
        inventory.write(f)

async def run_playbook(datadir_path):
    executor = AnsibleSubprocessJobExecutor()

    jobdef = AnsibleJobDef(datadir_path, "pb.yml")

    job_status = await executor.submit_job(jobdef)

    # consume events and accumulate stdout replica
    stdout = ""

    # consume events as they arrive
    eventcount = 0
    result = {"res": {}}
    async for ev in job_status.events:
        eventcount += 1
        if isinstance(ev, RunnerOnOKEvent):
            result = ev
    return result.event_data or {}


def get_inventory(filename=None):
    if not filename:
        return {}

    r = ansible_runner.get_inventory(
        action="list",
        inventories=[filename],
    )
    return json.loads(r[0])["_meta"]["hostvars"]


if __name__ == "__main__":
    app.run(debug=True)
