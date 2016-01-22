# Copyright 2016 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from oslo_concurrency import processutils
from oslo_log import log

from ironic_python_agent import errors
from ironic_python_agent.extensions import base
from ironic_python_agent import hardware
from ironic_python_agent import utils

LOG = log.getLogger(__name__)

def _execute(cmd, error_msg, **kwargs):
    try:
        LOG.info("cmd=%s",*cmd)
        stdout, stderr = utils.execute(*cmd, **kwargs)
    except processutils.ProcessExecutionError as e:
        LOG.error(error_msg)
        raise errors.CommandExecutionError(e)
    return (stdout, stderr)

class CloneExtension(base.BaseAgentExtension):
    def __init__(self, agent=None):
        super(CloneExtension, self).__init__(agent=agent)     

 
    @base.async_command('clone_disk')
    def clone_disk(self, local_disk, remote_disk):
        LOG.debug('Clone disk, source=%s', local_disk)
        cmd = ['dd', 'if='+local_disk,  'of='+remote_disk, 'bs=1M']
        _execute(cmd, "clone disk error")

    @base.async_command('prepare_iscsi_disk')
    def prepare_iscsi_disk(self, iscsi_ip, iqn):
        LOG.debug('Preparing prepare_iscsi_disk, iscsi target ip=%s', iscsi_ip)
        cmd = ['iscsiadm', '-m', 'node', '-T', iqn, '-p', iscsi_ip, '-l']
        _execute(cmd, "prepare_iscsi_disk failed")


    @base.async_command('run_os_cmd')
    def run_os_cmd(self, os_cmd_str):
        LOG.debug('run_os_cmd, cmd = %s',  os_cmd_str)
        utils.execute(os_cmd_str)
