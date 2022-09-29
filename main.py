import asyncio
import configparser

import os
from ansible_sdk import AnsibleJobDef
import tempfile
import yaml
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
async def index():
    inventory_type = app.config['inventory_type']
    filename = os.path.join(app.instance_path, "inventory/%s.yml" % inventory_type)
    datadir_path = create_temp_dir()
    print("INFO: Gathering information about inventory from %s" % inventory_type)
    with open(filename, 'r') as fh:
        config = yaml.safe_load(fh.read())

    if inventory_type == 'gcp_compute':
        app.config['service_account_file'] = config.get('service_account_file')
        inventory_data = {
            'zone': config.get('zones')[0],
            'project': config.get('projects'),
            'service_account_file': config.get('service_account_file'),
        }
        create_gcp_inventory_playbook(
            datadir_path=datadir_path,
            **inventory_data
        )
    elif inventory_type == 'azure':
        inventory_data = {}
    else:
        print("ERR: Unable to parse inventory")
        return render_template(
            "index.html",
            message={
                "error": "Unable to parse inventory file provided"
            }
        )

    d = await run_playbook(datadir_path=datadir_path)
    print("Return from Ansible SDK %s" % d)

    return render_template(
        "index.html",
        hosts=d,
        zone=config.get('zones')[0],
        project=config.get('projects'),
        message={
            "success": "True"
        }
    )


@app.route("/powerstate_host", methods=["POST"])
async def manage_powerstate_host():
    data = request.get_json()
    datadir_path = create_temp_dir()
    create_inventory(datadir_path=datadir_path, host=data["ipAddress"])
    print("Performing %s operation on %s " % (data['powerstate'], data['ipAddress']))
    create_powerstate_playbook(
        datadir_path=datadir_path,
        **{
            'desired_powerstate': data['powerstate'],
            'machine_name': data['machine_name'],
            'machine_type': data['machine_type'],
            'zone': data['zone'],
            'project': data['project'],
            'service_file': app.config['service_account_file'],
        }
    )
    d = await run_playbook(datadir_path=datadir_path)
    print("Return from Ansible SDK %s" % d)
    return {"ipAddress": data["ipAddress"], "response": d, "success": True}


@app.route("/ping_host", methods=["POST"])
async def ping_host():
    data = request.get_json()
    datadir_path = create_temp_dir()
    create_inventory(datadir_path=datadir_path, host=data["ipAddress"])
    create_ping_playbook(datadir_path=datadir_path)
    d = await run_playbook(datadir_path=datadir_path)
    print("Return from Ansible SDK %s" % d)
    return {"ipAddress": data["ipAddress"], "response": d, "success": True}


def create_temp_dir():
    tmp_dir = tempfile.mkdtemp(suffix="ansible-sdk")
    datadir_path = os.path.join(tmp_dir, "datadir")
    for i in ["inventory", "project"]:
        os.makedirs(os.path.join(datadir_path, i), exist_ok=True)

    return datadir_path


def create_powerstate_playbook(datadir_path, **kwargs):
    if kwargs['desired_powerstate'] == 'poweredoff':
        tp_filename = 'gcp_powerstate_off.yml'
    else:
        tp_filename = 'gcp_powerstate_on.yml'
    powerstate_tp = render_template(
        tp_filename,
        machine_name=kwargs['machine_name'],
        machine_type=kwargs['machine_type'],
        zone=kwargs['zone'],
        project=kwargs['project'],
        service_file=kwargs['service_file'],
    )
    with open(os.path.join(datadir_path, "project", "pb.yml"), "w") as fh:
        fh.write(powerstate_tp)


def create_gcp_inventory_playbook(datadir_path, **kwargs):
    tp_filename = 'gcp_instance_info.yml'
    instance_info_tp = render_template(
        tp_filename,
        zone=kwargs['zone'],
        project=kwargs['project'],
        service_file=kwargs['service_account_file'],
    )
    with open(os.path.join(datadir_path, "project", "pb.yml"), "w") as f:
        f.write(instance_info_tp)


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
    # consume events as they arrive
    result = {"res": {}}
    async for ev in job_status.events:
        # print(ev)
        if isinstance(ev, RunnerOnOKEvent) and ev.event_data.task_action == 'debug':
            result = ev.event_data.res
    print("Result from Ansible SDK %s" % result)
    return result or {}
