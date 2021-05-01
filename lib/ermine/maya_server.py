# Copyright (C) 2020 craig

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from . import server
from maya.api.OpenMaya import MCommandMessage
import maya.utils, maya.mel

def _maya_exec(src, g, mel):

    log = [str()]

    def intercept(msg, msgType, data):
        if msgType > 0:
            data[0] += msg

    cb = MCommandMessage.addCommandOutputCallback(intercept, log)

    try:
        if mel:
            res = maya.mel.eval(src)
            if res != None:
                log[0] += str(res)
        else:
            exec(src, g)
    finally:
        MCommandMessage.removeCallback(cb)

    return log[0]


def _maya_mel(src):
    return maya.utils.executeInMainThreadWithResult(_maya_exec, src, None, True)

def _maya_python(src):
    g = maya.utils.executeInMainThreadWithResult('globals()')
    return maya.utils.executeInMainThreadWithResult(_maya_exec, src, g, False)

class MayaScriptServer(server.ScriptServer):
    def __init__(self, port=server.default_port):
        super(MayaScriptServer, self).__init__(
            port, {
                'mel': _maya_mel,
                'python': _maya_python
            })
