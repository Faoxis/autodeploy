from fabric.api import run

import autodeploy.fablib as fl
from autodeploy.fablib import init, clear


fl.before_init.append(lambda: run('echo "hello from before init" >> hello.txt'))
fl.before_deploy.append(lambda: run('echo "Hello from deploy" >> hello.txt'))
fl.before_rollback.append(lambda: run('echo "Hello from rollback" >> hello.txt'))

fl.after_init.append(lambda: run('echo "Bye from init" >> bye.txt'))
fl.after_deploy.append(lambda: run('echo "Bye from deploy" >> bye.txt'))
fl.after_rollback.append(lambda: run('echo "Bye from rollback" >> bye.txt'))

