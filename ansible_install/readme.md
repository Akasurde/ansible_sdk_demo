# Install instructions

We have supplied an easy way to run the demo app using Ansible to install and set it up.

We recommend a Red Hat Enterprise Linux 8 or higher virtual machine. We have been using VMs in *Google Compute Cloud*, though this is not mandatory.
Remember you need to provide your OWN *gcp_auth* file. This is a json output of the service account in *Google Cloud Platform* you wish to use for inventory and actions.

### Instructions 
1. Create a user called "sdkuser"
2. Copy **’gcp_auth', 'install.yml', 'nginx.conf’** to /home/sdkuser
3. sudo dnf install -y ansible-core
4. ansible-playbook install.yml
5. cd /home/sdkuser/ansible_sdk_demo 
6. Run /usr/local/bin/uwsgi --socket 127.0.0.1:5000  --protocol=http -w wsgi:app 
