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


from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from threading import Thread
import os

default_port = 8666

def _python(src):
    exec(src, globals())
    return True

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ScriptServer(object):
    def __init__(self, port=default_port, methods={}):
        self.server = SimpleXMLRPCServer(
            ('localhost', port),
            requestHandler=RequestHandler,
            logRequests=False,
            allow_none=True)

        for name,func in methods.items():
            self.server.register_function(func, name)
        if 'python' not in methods:
            self.server.register_function(_python, 'python')

        self.server.register_function(lambda: os.getpid(), 'pid')

        server = self.server
        self.t = Thread(target=lambda: server.serve_forever())
        self.t.start()

    def __del__(self):
        print("Shutting down ScriptServer")
        self.server.shutdown()

