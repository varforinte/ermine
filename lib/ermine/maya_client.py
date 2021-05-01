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


from . import client


class MayaScriptClient(client.ScriptClient):
    def __init__(self, port=client.default_port, mel=False):
        super(MayaScriptClient, self).__init__(port)
        self.mel = mel

    def langname(self):
        return "MEL" if self.mel else "Python"

    def evaluate(self, src):
        if self.mel:
            return self.s.mel(src)
        return self.s.python(src)
