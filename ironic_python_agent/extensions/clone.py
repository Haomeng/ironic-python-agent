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
        stdout, stderr = utils.execute(*cmd, **kwargs)
    except processutils.ProcessExecutionError as e:
        LOG.error(error_msg)
        raise errors.ISCSICommandError(error_msg, e.exit_code,
                                       e.stdout, e.stderr)
	return (stdout, stderr)

class CloneExtension(base.BaseAgentExtension):
    def __init__(self, agent=None):
        super(CloneExtension, self).__init__(agent=agent)     

   
    @base.async_command('clone_disk')
    def clone_disk(self, local_disk, remote_disk):
        LOG.debug('Clone disk, source=%s', local_disk)
	cmd = ['dd', 'if=', 'of=', 'bs=1M']
        _execute(cmd, "Error when executing os command:" % cmd)

    @base.async_command('prepare_iscsi_disk')
    def prepare_iscsi_disk(self, iscsi_ip):
        LOG.debug('Preparing prepare_iscsi_disk, iscsi target ip=%s', iscsi_ip)
	""""	    
        ls -l /dev/ | awk '{print $10}' > /tmp/fdisk-list-orig
        iscsiadm -m node -T $2 -p $1 -l
        ls -l /dev/ | awk '{print $10}' > /tmp/fdisk-list-orig-iscsi
        comm /tmp/fdisk-list-orig /tmp/fdisk-list-orig-iscsi -3 2>/dev/null | sed 's/^\t//'
    """
        LOG.debug('Preparing prepare_iscsi_disk, iscsi target ip=%s', iscsi_ip)		
		
	cmd = ['ls', '-l', '/dev/', '|', 'awk', '\'{print $10}\'',
            '>', '/tmp/dev-list-orig']
        _execute(cmd, "Error when executing os command:" % cmd)
		
	cmd = ['iscsiadm', '-m', 'iscsi', '--mode', 'target', '--op',
            'new', '--tid', '1', '--targetname', iqn]
        _execute(cmd, "Error when adding a new target for iqn %s" % iqn)
	
        cmd = ['ls', '-l', '/dev/', '|', 'awk', '\'{print $10}\'',
            '>', '/tmp/dev-list-iscsi']
        _execute(cmd, "Error when executing os command:" % cmd)

	cmd = ['comm', '/tmp/dev-list-orig', '/tmp/dev-list-iscsi',
       	    '-3', '2>/dev/null', '\'{print $10}\'',
           '>', '/tmp/dev-list-orig']
        _execute(cmd, "Error when executing os command:" % cmd)	
		
		
    @base.async_command('os_cmd')
    def os_cmd(self, *os_cmd_str):
        LOG.debug('os_cmd, cmd = %s',  os_cmd_str)	
