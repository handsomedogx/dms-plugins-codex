# AGENTS.md

## Scope

This repository is the umbrella repo for Dank Linux / DankMaterialShell (DMS) plugin standards and discovery.
Use it to maintain shared development rules, plugin index links, and demo references.
Plugin source code should live in separate plugin repositories, not in this root repository.

## Repository Role

Treat this root repository as documentation and navigation only.

Track here:

- `AGENTS.md`
- `README.md`
- shared documentation, templates, and index assets
- links to plugin repositories and demo videos

Do not track here:

- local plugin working trees
- plugin-specific source code that belongs in its own repository
- temporary local `Dank*` directories that will be migrated elsewhere

Root documentation rule:

- maintain `README.md` manually in English
- do not add generated multilingual README outputs to this repository unless the user explicitly asks
- keep links, showcase content, and navigation current in `README.md`

## Source Of Truth

- Primary docs site: `https://danklinux.com/docs/`
- Plugin overview: `https://danklinux.com/docs/dankmaterialshell/plugins-overview`
- Plugin development guide: `https://danklinux.com/docs/dankmaterialshell/plugin-development`
- Registry contribution guide: `https://danklinux.com/docs/contributing-registry`
- Plugin registry: `https://plugins.danklinux.com/`

As of `2026-03-10`, the docs indicate:

- `1.4` is the latest stable documentation for plugin development.
- `1.5` is marked `unreleased`.

Unless the user explicitly asks for unreleased behavior, prefer the `1.4` plugin-development docs and verify current docs before citing version-sensitive details.

## DMS Plugin Development Workflow

When helping with a new plugin, default to this workflow:

1. Clone the upstream shell repo for QML tooling context.
2. Create the plugin under the repo's `quickshell/dms-plugins/`.
3. Symlink that plugin into the user's DMS config plugin directory.
4. Use DMS IPC commands for reload and status checks.
5. Keep the plugin compatible with the stable docs unless the user asks otherwise.

Recommended setup:

```bash
mkdir -p ~/repos && cd ~/repos
git clone https://github.com/AvengeMedia/DankMaterialShell.git
cd DankMaterialShell/quickshell
touch .qmlls.ini
qs -p .

mkdir -p dms-plugins/MyPlugin
ln -sf ~/repos/DankMaterialShell/quickshell/dms-plugins/MyPlugin \
  ~/.config/DankMaterialShell/plugins/MyPlugin
```

After `qs -p .`, the user can stop the process if they only need the generated QML language server config.

## Plugin Location And Minimum Structure

Default plugin location:

- `~/.config/DankMaterialShell/plugins/<PluginName>/`

Every plugin should start with at least:

- `plugin.json`
- one or more QML files for UI or logic
- optional settings QML

Minimal `plugin.json` starter:

```json
{
  "id": "myPlugin",
  "name": "My Plugin",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": "Your Name",
  "type": "widget",
  "component": "./MyWidget.qml",
  "settings": "./MySettings.qml",
  "permissions": ["settings_read", "settings_write"]
}
```

## Plugin Types

Choose the implementation pattern based on plugin type:

- `widget`: status bar or panel widget; usually rooted in `PluginComponent`
- `widget` with Control Center integration: still `PluginComponent`, plus Control Center properties and handlers
- `launcher`: search/launcher integration; root object is `QtObject`, typically implements `getItems(query)` and `executeItem(item)`
- `daemon`: background plugin without visible UI
- `desktop`: desktop widget; root in `DesktopPluginComponent`

If the user has not chosen a type yet, ask what the plugin should do and map it to one of the types above.

## Common Runtime APIs And Conventions

Remember these common concepts from the docs:

- `pluginData` is for persisted plugin settings
- `pluginService.savePluginData(...)` writes settings
- runtime state should be stored separately from settings
- runtime state path is under `~/.local/state/DankMaterialShell/plugins/`
- runtime state APIs include `savePluginState` and `loadPluginState`
- permission-sensitive features must be declared in `plugin.json`
- use `process` permission to run commands
- use `network` permission for network access

## Development Loop

For local development, prefer this loop:

```bash
dms ipc call plugins list
dms ipc call plugins reload myPlugin
dms ipc call plugins status myPlugin
```

Useful checks:

- In DMS settings, scan or enable plugins from `Settings -> Plugins`
- Validate manifest syntax with `jq . plugin.json`
- Restart and inspect logs with `dms kill && dms run`

When the user reports that a plugin is not appearing, check in this order:

1. plugin path and symlink target
2. `plugin.json` syntax
3. plugin `id`
4. declared `type`
5. runtime logs
6. IPC status output

## Publishing Workflow

If the user wants to publish a plugin to the official registry:

1. Create a public GitHub repository for the plugin.
2. Include `plugin.json`, a README, and screenshots.
3. Create a release tag.
4. Submit the plugin to the registry repository following the registry docs.

Important registry rule:

- the registry entry `id` and `name` must match the plugin's own `plugin.json`

## Git Workflow

This workspace uses one plugin per repository only.
Do not create multi-plugin plugin-source repositories in this workspace.
Each plugin must be maintained and published as its own independent Git repository.

For every new plugin created in this workspace:

1. create the plugin directory in its own location
2. run `git init -b main` inside that plugin directory immediately
3. set repository-local Git identity immediately after init:
   - `git config user.name "Codex"`
   - `git config user.email "codex@local"`
4. add a `.gitignore` before the first commit
5. add an MIT `LICENSE` file before the first commit
6. use `handsomedogx` as the copyright holder in that MIT license
7. create an initial commit once the scaffold is runnable
8. publish that plugin to its own remote repository

For the workspace root:

- treat it as a coordination directory for shared docs such as `AGENTS.md`
- do not treat it as the canonical source repository for plugins

Default ignore rules should cover at least:

- `__pycache__/`
- `*.pyc`
- editor or OS junk such as `.DS_Store`, `.idea/`, `.vscode/`
- temporary logs or screenshots produced during development

Every new plugin repository should include a standard MIT license with this header:

```text
MIT License

Copyright (c) <year> handsomedogx
```

Commit discipline:

- make one commit per completed logical change
- do not leave finished code edits uncommitted at the end of a task when the repo is in a valid state
- do not mix unrelated changes into the same commit
- do not amend, rebase, or rewrite history unless the user explicitly asks
- for new local repositories in this workspace, use repository-local Git identity `Codex <codex@local>`
- do not change the global Git config for workspace plugin repositories
- in a single-plugin repository, do not use the plugin name as `scope` by default because it duplicates repository context
- only use `scope` when it adds real information such as `ui`, `ocr`, `settings`, `ipc`, or `docs`

Before committing, run the smallest relevant validation for the files touched. Prefer:

- `jq . plugin.json`
- `python3 -m py_compile` for changed Python helpers
- `dms ipc call plugins reload <pluginId>` when the plugin is installed in the active DMS session

Default commit format:

```text
<type>: <summary>
```

Optional commit format when `scope` adds useful information:

```text
<type>(<scope>): <summary>
```

Rules:

- `type` must be one of `feat`, `fix`, `refactor`, `docs`, `chore`, `test`
- `scope` is optional
- if `scope` is used, prefer subsystem names instead of the plugin name in a single-plugin repository
- `summary` should be short, imperative, and describe the user-visible or engineering change

Examples:

- `feat: bootstrap translation plugin`
- `fix(ui): constrain translator panel height`
- `docs: document niri keybind setup`
- `fix(ocr): silence screenshot cancel errors`

## How To Help In Future Turns

When asked to build a DMS plugin, do not stop at high-level advice if code changes are feasible.
Default to scaffolding a working plugin skeleton in the current workspace, then iterate on:

- manifest
- main QML component
- settings UI
- permissions
- hot reload
- validation/debugging

If the user asks for "the latest" plugin guidance, verify the docs site again before answering because DMS versioning may change.
