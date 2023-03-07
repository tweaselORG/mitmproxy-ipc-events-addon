"""
This is an addon for mitmproxy that sends events as nodejs-compatible IPC messages to a pipe.

The file descriptor of the pipe to send the messages to needs to be configured as an environment variable: IPC_PIPE_FD
If the variable is not set, the addon will do nothing.

To use the addon, start mitmproxy like this:

export IPC_PIPE_FD=42; mitmproxy -s ipc_events_addon.py
"""

import os
import json

class IpcEventRelay:
    pipe_fd = None

    def __init__(self):
        if ('IPC_PIPE_FD' in os.environ):
            self.pipe_fd = int(os.environ['IPC_PIPE_FD'])


    def _sendIpcMessage(self, message):
        """Takes a dict and sends it through a pipe as JSON."""
        if(self.pipe_fd is not None):
            os.write(self.pipe_fd, bytes(json.dumps(message) + '\n', 'utf8'))

    def running(self):
        self._sendIpcMessage({"status": "running"})

    def done(self):
        self._sendIpcMessage({"status": "done"})

    def client_connected(self, client):
        self._sendIpcMessage({"status": "client_connected", "context": {"address": client.peername} })

    def client_disconnected(self, client):
        self._sendIpcMessage({"status": "client_disconnected", "context": {"address": client.peername} })

    def tls_failed_client(self, data):
        self._sendIpcMessage({"status": "tls_failed", "context": {"client_address": data.context.client.peername, "server_address": data.context.server.address, "error": data.conn.error }})

    def tls_established_client(self, data):
        self._sendIpcMessage({"status": "tls_established", "context": {"client_address": data.context.client.peername, "server_address": data.context.server.address}})

addons = [IpcEventRelay()]
