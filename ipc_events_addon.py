"""
This is an addon for mitmproxy that sends events as nodejs-compatible IPC messages to a pipe.

The file descriptor of the pipe to send the messages to needs to be configured as a mitmproxy option: ipcPipeFd
If the option is not set, the addon will do nothing.

To use the addon, start mitmproxy like this:

mitmproxy -s ipc_events_addon.py --set ipcPipeFd=42
"""

import os
import json
from mitmproxy import ctx

class IpcEventRelay:
    def load(self, loader):
        loader.add_option(
            name="ipcPipeFd",
            typespec=int,
            default=False,
            help="The file descriptor to write the IPC messages to",
        )


    def _sendIpcMessage(self, message):
        """Takes a dict and sends it through a pipe as JSON."""
        if(ctx.options.ipcPipeFd is not None):
            os.write(ctx.options.ipcPipeFd, bytes(json.dumps(message) + '\n', 'utf8'))

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
