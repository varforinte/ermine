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


import maya.cmds, maya.utils

def ErmineStart():
    """Start the server in a background thread"""

    from ermine.maya_server import MayaScriptServer
    global g_ermine_server
    g_ermine_server = MayaScriptServer()

if not maya.cmds.about(b=True):
    maya.utils.executeDeferred(ErmineStart)
