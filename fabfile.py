"""
auto deployment code goes here
"""
from fabric.api import *
import os
import logging
from fabric.contrib.files import append
import util

logger = logging.getLogger(__name__)

env.hosts = ['xx.x.xx.xxx']
env.user = 'xxxx'
env.use_ssh_config = True


@task
def deploy(repo_name='', branch=''):
    logger.info("deploying %s:%s to %s" % (repo_name, branch, env.hosts))
    # your awesome deployment code goes here
    run("touch %s" % repo_name)
    # 1. disable nagios notification
    # 2. stop apache
    # 3. pull code on server
    # 3.1. git pull
    # 3.2. install requirements
    # 3.3. clear pyc
    # 4. run migration
    # 5. start apache
    # 6. post deployment: check app health
    # 7. enable nagios notification
    # 8. run automated selenium test
    # 9. deploy successful notification (Hip Chat notification?)
    pass


@task
def push_pub_key(key_file='~/.ssh/id_rsa.pub'):
    run("touch ~/.ssh/authorized_keys")
    run("chmod 640 ~/.ssh/authorized_keys")
    key_text = util.read_key_file(key_file)
    append('~/.ssh/authorized_keys', key_text)

