# vkcli

CLI for [VibeKit](https://vkcli.com) - Configure AI coding workflows in SaaS, execute locally with Claude Code.

## Installation

```bash
pip install vibekit-cli
```

## Quick Start

```bash
# Login to VibeKit
vk login

# Link to your project
vk link owner/project-name

# Pull configuration
vk pull

# Push updates
vk push
```

## Commands

| Command | Description |
|---------|-------------|
| `vk login` | Authenticate with VibeKit |
| `vk logout` | Clear credentials |
| `vk init` | Initialize new project |
| `vk link <slug>` | Link existing project |
| `vk pull` | Pull config from SaaS |
| `vk push` | Push updates to SaaS |
| `vk status` | Show sync status |

## How It Works

1. **Configure** your project at [vkcli.com](https://vkcli.com)
2. **Pull** configuration to your local `.vk/` folder
3. **Code** with Claude Code using your rules and context
4. **Push** metrics and status back to SaaS

## Documentation

Full documentation at [vkcli.com/docs](https://vkcli.com/docs)

## License

MIT
