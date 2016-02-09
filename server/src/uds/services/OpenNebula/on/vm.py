# -*- coding: utf-8 -*-

#
# Copyright (c) 2012 Virtual Cable S.L.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of Virtual Cable S.L. nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
.. moduleauthor:: Adolfo Gómez, dkmaster at dkmon dot com
'''

import logging
import six
import oca

from defusedxml import minidom
# Python bindings for OpenNebula
from .common import VmState

__updated__ = '2016-02-09'

logger = logging.getLogger(__name__)


def getMachineState(api, machineId):
    '''
    Returns the state of the machine
    This method do not uses cache at all (it always tries to get machine state from OpenNebula server)

    Args:
        machineId: Id of the machine to get state

    Returns:
        one of the on.VmState Values
    '''
    try:
        vm = oca.VirtualMachine.new_with_id(api, int(machineId))
        vm.info()
        return vm.state
    except Exception as e:
        logger.error('Error obtaining machine state for {} on opennebula: {}'.format(machineId, e))

    return VmState.UNKNOWN


def startMachine(api, machineId):
    '''
    Tries to start a machine. No check is done, it is simply requested to OpenNebula.

    This start also "resume" suspended/paused machines

    Args:
        machineId: Id of the machine

    Returns:
    '''
    try:
        vm = oca.VirtualMachine.new_with_id(api, int(machineId))
        vm.resume()
    except Exception as e:
        logger.error('Error obtaining machine state for {} on opennebula: {}'.format(machineId, e))

def stopMachine(api, machineId):
    '''
    Tries to start a machine. No check is done, it is simply requested to OpenNebula

    Args:
        machineId: Id of the machine

    Returns:
    '''
    try:
        vm = oca.VirtualMachine.new_with_id(api, int(machineId))
        vm.poweroff_hard()
    except Exception as e:
        logger.error('Error obtaining machine state for {} on opennebula: {}'.format(machineId, e))


def suspendMachine(api, machineId):
    '''
    Tries to start a machine. No check is done, it is simply requested to OpenNebula

    Args:
        machineId: Id of the machine

    Returns:
    '''
    startMachine(api, machineId)

def removeMachine(api, machineId):
    '''
    Tries to delete a machine. No check is done, it is simply requested to OpenNebula

    Args:
        machineId: Id of the machine

    Returns:
    '''
    try:
        vm = oca.VirtualMachine.new_with_id(api, int(machineId))
        vm.delete()
    except Exception as e:
        logger.error('Error obtaining machine state for {} on opennebula: {}'.format(machineId, e))


def enumerateMachines(self):
    '''
    Obtains the list of machines inside OpenNebula.
    Machines starting with UDS are filtered out

    Args:
        force: If true, force to update the cache, if false, tries to first
        get data from cache and, if valid, return this.

    Returns
        An array of dictionaries, containing:
            'name'
            'id'
            'cluster_id'
    '''
    vmpool = oca.VirtualMachinePool(self.api)
    vmpool.info()

    for vm in vmpool:
        yield (vm.id, vm.name)


def getNetInfo(api, machineId, networkId=None):
    '''
    Changes the mac address of first nic of the machine to the one specified
    '''
    md = minidom.parseString(api.call('vm.info', int(machineId)))
    node = md

    for nic in md.getElementsByTagName('NIC'):
        netId = nic.getElementsByTagName('NETWORK_ID')[0].childNodes[0].data
        if networkId is None or int(netId) == int(networkId):
            node = nic
            break

    # Default, returns first MAC found (or raise an exception if there is no MAC)
    return (node.getElementsByTagName('MAC')[0].childNodes[0].data, node.getElementsByTagName('IP')[0].childNodes[0].data)

# Sample NIC Content (there will be as much as nics)
#         <NIC>
#             <BRIDGE><![CDATA[br0]]></BRIDGE>
#             <CLUSTER_ID><![CDATA[100]]></CLUSTER_ID>
#             <IP><![CDATA[172.27.0.49]]></IP>
#             <IP6_LINK><![CDATA[fe80::400:acff:fe1b:31]]></IP6_LINK>
#             <MAC><![CDATA[02:00:ac:1b:00:31]]></MAC>
#             <NETWORK><![CDATA[private]]></NETWORK>
#             <NETWORK_ID><![CDATA[1]]></NETWORK_ID>
#             <NETWORK_UNAME><![CDATA[oneadmin]]></NETWORK_UNAME>
#             <NIC_ID><![CDATA[2]]></NIC_ID>
#             <VLAN><![CDATA[NO]]></VLAN>
#         </NIC>



