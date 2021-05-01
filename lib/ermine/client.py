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


import sys
if sys.version_info[0] >= 3:
    from xmlrpc.client import ServerProxy
    from xmlrpc.client import Fault as XMLFault
    raw_input = input
else:
    from xmlrpclib import ServerProxy
    from xmlrpclib import Fault as XMLFault

default_port = 8666


class ScriptClient(object):
    """Send a command to the ScriptServer"""

    def __init__(self, port=default_port):
        self.port = port

    def run(self):
        self.s = ServerProxy('http://localhost:{}'.format(self.port))
        prompt = '[{}] {} > '.format(self.s.pid(), self.langname())

        try:
            while True:
                x = raw_input(prompt)
                if x:
                    try:
                        log = self.evaluate(x)
                        if log:
                            sys.stdout.write(log)
                            if not log.endswith('\n'):
                                sys.stdout.write('\n')
                    except XMLFault as e:
                        print(e)
        except EOFError:
            print("")
            pass

