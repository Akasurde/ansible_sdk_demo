Demo App for Ansible SDK
========================

# Overview

This is a sample Python web application using Flask that shows capabilities of [Ansible SDK](https://github.com/ansible/ansible-sdk).

# Requirements

- Python 3.8+
- Ansible SDK

# Installation

```bash
git clone https://github.com/Akasurde/ansible_sdk_demo
cd ansible_sdk_demo
pip install -r requirements.txt
```

This app uses GCP inventory configuration file.

Firstly, copy example configuration files like -

```console
cp -a instance_config instance
```

* Specifying GCP Service Account file in the GCP dynamic inventory file

Edit ``service_account_file:`` setting in ``instance/inventory/gcp_compute.yml`` to
specify your service account file.


# Run

```console
$ python main.py

...

* Serving Flask app 'main' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 461-665-892
```

# Demo

Navigate to `http://localhost:5000` 

# Configuration

TBD