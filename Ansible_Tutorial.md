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
Ansible comes with a bunch of built-in modules that can be used once you set up an instance on a machine.
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