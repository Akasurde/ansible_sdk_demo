Demo App for Ansible SDK
========================

# Overview

This is a sample Python web application using Flask that shows capabilities of [Ansible SDK](https://github.com/ansible/ansible-sdk).

The app will demonstrate the following use cases of the SDK as follows

- Upon app start the app will run a playbook using the localsubprocess function in the SDK to grab the inventory of your Google Cloud Platform account.
- The app parses the output of the playbook job execution and displays the result in the web ui as a list of vm’s, private IP and power status as action buttons
- You can press the stop or start action button to control the power status of the VM, this is dependent on your Google Cloud Platform service account having the correct permissions to do so.
- Clicking on an action button to stop or start a virtual machine will demonstrate the use of an Execution Environment image to run the playbook through.

![Demo Landing Page](https://github.com/Akasurde/ansible_sdk_demo/blob/main/LandingPage.jpg)


# Requirements

- Python 3.8+
- Ansible SDK
- Flask (with asgiref)
- google-api-python-client
- uwsgi
- receptorctl
- ansible-runner

# Installation
Recommended option is to use the Ansible playbook that will setup your VM with the dependencies and install the demo app for you.
The ansible installation for the SDK demo app is here (https://github.com/Akasurde/ansible_sdk_demo/tree/main/ansible_install)
 
Otherwise you can manually install the application  using the following developer style install.
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

You can create a Google Cloud Platform service account json export in the Google Cloud Platform WebUI, search for Service Accounts and either create a new service account with a key or add a key to an existing service account you wish to use, the key is automatically downloaded to your local filesystem, this file is the file you need to name GCP_Auth and copy to your vm that will run the demo app.

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

cd /home/sdkuser/ansible_sdk_demo && uwsgi --socket 127.0.0.1:5000  --protocol=http -w wsgi:app 


# Demo

Navigate to `http://<vm public IP` 

