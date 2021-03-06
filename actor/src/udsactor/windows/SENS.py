# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2019 Virtual Cable S.L.
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
@author: Adolfo Gómez, dkmaster at dkmon dot com
'''
import typing

import win32com.client  # @UnresolvedImport, pylint: disable=import-error
import win32com.server.policy  # @UnresolvedImport, pylint: disable=import-error

from ..log import logger

# based on python SENS example from
# http://timgolden.me.uk/python/win32_how_do_i/track-session-events.html

# from Sens.h
SENSGUID_PUBLISHER = "{5fee1bd6-5b9b-11d1-8dd2-00aa004abd5e}"
SENSGUID_EVENTCLASS_LOGON = "{d5978630-5b9f-11d1-8dd2-00aa004abd5e}"

# from EventSys.h
PROGID_EventSystem = "EventSystem.EventSystem"
PROGID_EventSubscription = "EventSystem.EventSubscription"

IID_ISensLogon = "{d597bab3-5b9f-11d1-8dd2-00aa004abd5e}"

# Not imported at runtime, just for type checking
if typing.TYPE_CHECKING:
    from ..service import CommonService

class SensLogon(win32com.server.policy.DesignatedWrapPolicy):
    _com_interfaces_ = [IID_ISensLogon]
    _public_methods_ = [
        'Logon',
        'Logoff',
        'StartShell',
        'DisplayLock',
        'DisplayUnlock',
        'StartScreenSaver',
        'StopScreenSaver'
    ]

    _service: 'CommonService'

    def __init__(self, service: 'CommonService'):  # pylint: disable=super-init-not-called
        self._wrap_(self)
        self._service = service

    def Logon(self, *args):
        self._service.login(args[0] or '')
        logger.debug('Logon event: {}'.format(args))

    def Logoff(self, *args):
        logger.debug('Logoff event: arguments: {}'.format(args))
        self._service.logout(args[0] or '')

    def StartShell(self, *args):
        # logevent('StartShell : %s' % [args])
        pass

    def DisplayLock(self, *args):
        # logevent('DisplayLock : %s' % [args])
        pass

    def DisplayUnlock(self, *args):
        # logevent('DisplayUnlock : %s' % [args])
        pass

    def StartScreenSaver(self, *args):
        # When finished basic actor, we will use this to provide a new parameter: logout on screensaver
        # This will allow to easily close sessions of idle users
        # logevent('StartScreenSaver : %s' % [args])
        pass

    def StopScreenSaver(self, *args):
        # logevent('StopScreenSaver : %s' % [args])
        pass


def logevent(msg):
    logger.info(msg)

# def register():
    # call the CoInitialize to allow the registration to run in an other
    # thread
    # pythoncom.CoInitialize()

    # logevent('Registring ISensLogon')

    # sl=SensLogon()
    # subscription_interface=pythoncom.WrapObject(sl)

    # event_system=win32com.client.Dispatch(PROGID_EventSystem)

    # event_subscription=win32com.client.Dispatch(PROGID_EventSubscription)
    # event_subscription.EventClassID=SENSGUID_EVENTCLASS_LOGON
    # event_subscription.PublisherID=SENSGUID_PUBLISHER
    # event_subscription.SubscriptionName='Python subscription'
    # event_subscription.SubscriberInterface=subscription_interface

    # event_system.Store(PROGID_EventSubscription, event_subscription)

    # pythoncom.PumpMessages()
    # #logevent('ISensLogon stopped')
