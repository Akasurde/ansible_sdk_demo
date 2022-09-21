Demo App for Ansible SDK
========================

# Overview

This is a sample Python web application using Flask that shows capabilities of [Ansible SDK](https://github.com/ansible/ansible-sdk).

# Requirements

- Python 3.8+
- Ansible SDK
- Flask (with asgiref)

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

Edit ``service_account_file:`` setting in ``instance/inventory/gcp_compute.yml`` to specify your GCP service account file.

A sample GCP Service Account file looks -

```json
{
  "type": "service_account",
  "project_id": "project_name",
  "private_key_id": "oenx7d5k954bjmnwftuksqej24jdez2p6l4etvxj",
  "private_key": "-----BEGIN PRIVATE KEY-----<SOME_DATA>\n-----END PRIVATE KEY-----\n",
  "client_email": "username@project_name.iam.gserviceaccount.com",
  "client_id": "12345678910",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/username%40project_name.iam.gserviceaccount.com"
}
```


# Run

You can specify which Cloud platform you want to work with. Currently, ``gcp_compute`` is supported.

```console
$ python main.py gcp_compute

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
