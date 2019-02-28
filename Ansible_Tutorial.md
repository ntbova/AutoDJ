# ANSIBLE 

### Ansible is an IT automation tool to automate things like cloud provisioning, configuration management, application deployment, and intra-service orchestration

### **Language Used:** YAML, shell commands

## **How it works**
Ansible works by putting "modules" as they're called on any machine and executing the modules over SSH so no additional programs are required. This is useful because it means there are no servers, daemons, or databases required to automate what you want.

Another cool thing Ansible has is "playbooks". Playbooks are descriptions of the desired state of your system, which Ansible does all the heavy lifting of getting your system into that state no matter their current state. This makes tasks very repeatable and reliable.

## **What it's useful for**
Very popular use cases for ansible include:
* Provisioning - Dealing with infrastructure; databases, networks, cloud products
* Configuration Management
* App Deployment
* Continuous Delivery
* Security & Compliance
* Orchestration - Doing all of these things in the correct order at the correct times

## **Out of the box**
Ansible comes with a bunch of built-in modules that are essentially programs that can be used once you set up an instance on a machine.
Some modules include:
* Various database functions (MySQL, Postgres, etc.)
* Various file functions
* A variety of cloud functions (AWS s3, ec2, etc)
* Ability to execute commands and scripts
* Source Control
  
[Here's a more expansive list of modules](https://docs.ansible.com/ansible/latest/modules/modules_by_category.html)

## **Get Started**
To get started, all you need to do is install ansible on any machine. From that machine you will be able to manage a whole fleet of remote machines.

### **Installation**
1. To install, make sure your control machine is **not windows** and has Python 2 (2.7+) or Python 3 (3.5+)
2. Install Ansible on your designated control machine using your OS's package manager or pip

```
sudo apt-get install ansible
```
or
```
sudo easy_install pip
sudo pip install ansible
```

### **Adding Remote Machines**
Now that you have ansible installed on your machine, it is time to add remote machines to your "*inventory*" as Ansible calls it. This allows ansible to run modules on groups of machines.

To do this, simply add the hostnames of your servers to Ansible's `hosts` file, which is located in:
```
/etc/ansible/hosts
```
Here's an example of what that could like like when you're done:
```
foo.example.com
bar.example.com
173.02.12.201
```
This hosts file has 3 hosts in it. You can also group hosts together so you can run Ansible modules for groups of hosts in your inventory.
```
[webservers]
foo.example.com
bar.example.com

[dbservers]
db1.example.com
db2.example.com
```

#### Setting up connectivity to your remote machines
The easiest way to ensure connectivity to your remote machines is through SSH keys. Ansible uses SSH to connect to the computer and setting up SSH keys on your remote machines allow you to connect without the use of a password. 

To do this, first generate an SSH key on your controlling machine:
```
ssh-keygen -t rsa -C "name@example.org"
```
Then copy your key to the remote machines using:
```
ssh-copy-id user@foo.example.com
```
Where *user* is the user to be logged on to on the server. This step may ask for a password for the user on the server when copying over the SSH key.

## **Running commands on remote machines**
### Now that you have remote machines set up to be managed, you can run ansible modules and playbooks on them. With playbooks, you don't need to run commands Ad-Hoc in the command line and can specify multiple commands to be run in a sequence.

We will begin with modules, which can be run Ad-Hoc in the command line.

### **Modules**
Modules 

### **Playbooks**
