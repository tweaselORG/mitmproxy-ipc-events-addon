# mitmproxy IPC Events Addon

> Addon for mitmproxy to send IPC messages for lifecycle and other events.

This addon was developed for <https://github.com/tweaselORG/cyanoacrylate> to spawn mitmproxy from a parent process and receive the events as IPC messages to a pipe. It is compatible with the IPC interface nodejs uses to communicate with other node child processes, even though this interface is not offically supported for this purpose (see <https://nodejs.org/api/child_process.html#optionsstdio>). The addon was inspired by [this stackoverflow answer](https://stackoverflow.com/a/23854353).

This addon is only supported on POSIX environments and **does not work on Windows**.

## Usage

To use the addon, you need to start mitmproxy with the addon. Also, the addon expects an environment variable `IPC_PIPE_FD` set to the number of a file descriptor that belongs to the pipe the addons is supposed to write the IPC messages to. Make sure the addon has the permissions to write to this file descriptor. It could look like this:

```zsh
export IPC_PIPE_FD=42; mitmproxy -s ipc_events_addon.py
```

If you want to use the addon with nodejs as intended, here is an example of how it comes together:

```js
const { spawn } = require('child_process');

const proc = spawn('mitmproxy', ['-s ./ipc_events_addon.py'], {
    stdio: ['pipe', 'pipe', 'pipe', 'ipc'],
    env: { PATH: process.env.PATH, IPC_PIPE_FD: 3 },
});

proc.on('message', (msg) => console.log(msg));
```

## License

This code is licensed under the MIT license, see the [`LICENSE`](LICENSE) file for details.

Issues and pull requests are welcome! Please be aware that by contributing, you agree for your work to be licensed under an MIT license.
