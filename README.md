# DMS Plugin Index

> Independent DMS plugins. Shared standards. One public directory.

`DMS Plugin Index` is the public landing page for my Dank Linux / DankMaterialShell plugin ecosystem.
This repository is where I keep the shared rules, plugin discovery links, demo references, and high-level compatibility notes.

Plugin source code does not live here.
Each plugin is developed and released in its own repository.

## Start Here

- Development rules: [AGENTS.md](./AGENTS.md)
- DMS docs: <https://danklinux.com/docs/>
- Plugin development guide: <https://danklinux.com/docs/dankmaterialshell/plugin-development>
- Official plugin registry: <https://plugins.danklinux.com/>

## At A Glance

- one root repository for standards and discovery
- one repository per plugin for source code and releases
- one public directory for repository links and demo videos
- optional local media under `assets/` for covers and thumbnails

## Featured Plugins

Use this section for the plugins you want people to notice first.
Keep it short and visual.

### Coming Soon

- Plugin: `TBD`
- Type: `Widget`
- Repository: add GitHub link
- Demo: add video link
- Status: `Planned`
- Summary: short one-line value proposition

Template:

```md
### Plugin Name

- Plugin: `plugin-id`
- Type: `Widget / Launcher / Daemon / Desktop`
- Repository: [GitHub](https://github.com/<user>/<repo>)
- Demo: [Video](https://example.com/demo)
- Status: `Active`
- Summary: one-line explanation of what makes the plugin useful
```

## Plugin Directory

Add one row per public or released plugin.

| Plugin | Type | Repository | Demo | DMS | Status | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| _Coming soon_ | Widget | Add repo link | Add video link | 1.4+ | Planned | Public plugin repositories will appear here after migration |

Template for a new row:

```md
| Plugin Name | Widget / Launcher / Daemon / Desktop | [GitHub](https://github.com/<user>/<repo>) | [Video](https://example.com/demo) | 1.4+ | Active | Short one-line description |
```

Recommended status labels:

- `Planned`
- `Active`
- `Beta`
- `Archived`

## Demo And Media

Each public plugin entry should eventually have:

- one repository link
- one demo video link
- one concise summary
- one compatibility note if needed

Optional local media can live under `assets/` using the plugin id or repository name:

```text
assets/
└── <plugin-id>/
    ├── cover.png
    ├── thumb.png
    └── notes.txt
```

Recommended demo coverage:

- show the widget or entry point in the first few seconds
- show the main workflow in under 30 to 60 seconds
- show one real interaction instead of only static screenshots

## Standards

Shared development standards for all plugins are maintained in [AGENTS.md](./AGENTS.md).

Core rules:

- this root repository tracks standards and navigation only
- each plugin must have its own independent Git repository
- plugin repositories should follow the shared DMS workflow documented in `AGENTS.md`
- commit messages use the format `<type>: <summary>`

Examples:

- `feat: add weather plugin entry`
- `docs: update plugin publishing rules`
- `fix: correct repository link for launcher plugin`

## Release Model

For each plugin:

1. build and maintain the plugin in its own repository
2. document installation and usage in that plugin repository
3. publish demo material
4. link the repository and video back here
5. update compatibility and status when the plugin changes

## Repository Layout

```text
.
├── AGENTS.md
├── README.md
└── assets/
    └── .gitkeep
```

## Roadmap

- add live plugin entries after repository migration
- add a proper featured section with real repositories
- add thumbnails or covers for each public plugin
- add compatibility notes across DMS versions
- add release and changelog links for each plugin
