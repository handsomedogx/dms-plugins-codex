<p align="center">
  <img src="./assets/icons/index.svg" width="92" alt="DMS Plugins Codex icon" />
</p>

# DMS Plugins Codex

> Independent DMS plugins. Shared standards. One public directory.

`DMS Plugins Codex` is the public landing page for my Dank Linux / DankMaterialShell plugin ecosystem.
This repository keeps the shared rules, plugin discovery links, demo references, and high-level compatibility notes.
Plugin source code does not live here. Each plugin is developed and released in its own repository.

## Start Here

- [Development rules](./AGENTS.md)
- [DMS docs](https://danklinux.com/docs/)
- [Plugin development guide](https://danklinux.com/docs/dankmaterialshell/plugin-development)
- [Official plugin registry](https://plugins.danklinux.com/)

## At A Glance

<table>
<tr>
<td width="25%" valign="top">
<img src="./assets/icons/repo.svg" width="20" alt="One Repo Per Plugin" />

<strong>One Repo Per Plugin</strong><br />
Every public plugin lives in its own source repository and release flow.
</td>
<td width="25%" valign="top">
<img src="./assets/icons/rules.svg" width="20" alt="Shared Standards" />

<strong>Shared Standards</strong><br />
This root repository stores the workflows, conventions, and publishing rules.
</td>
<td width="25%" valign="top">
<img src="./assets/icons/video.svg" width="20" alt="Video-First Showcase" />

<strong>Media Showcase</strong><br />
Each plugin entry can point to screenshots or a short demo video that shows the real workflow.
</td>
<td width="25%" valign="top">
<img src="./assets/icons/spark.svg" width="20" alt="Public Plugin Directory" />

<strong>Public Plugin Directory</strong><br />
Repository links, compatibility notes, and summaries stay in one public place.
</td>
</tr>
</table>

## Featured Plugins

Use this section for the plugins you want people to notice first. Keep it short and visual.

### Dank Translate

[<img src="https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/ui.png" alt="Dank Translate UI preview" height="420" />](https://github.com/handsomedogx/DankTranslate)
[<img src="https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/setting.png" alt="Dank Translate settings preview" height="420" />](https://github.com/handsomedogx/DankTranslate)

- Plugin: `dankTranslate`
- Type: `Widget`
- Repository: [GitHub](https://github.com/handsomedogx/DankTranslate)
- Preview: [UI](https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/ui.png) | [Settings](https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/setting.png)
- Demo: Pending
- Status: `Beta`
- Summary: Translate English and Chinese text from a popout or screenshot OCR workflow.

### Dank Focus Time

[<img src="https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/ui.png" alt="Dank Focus Time UI preview" height="420" />](https://github.com/handsomedogx/DankFocusTime)
[<img src="https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/setting.png" alt="Dank Focus Time settings preview" height="420" />](https://github.com/handsomedogx/DankFocusTime)

- Plugin: `dankFocusTime`
- Type: `Widget`
- Repository: [GitHub](https://github.com/handsomedogx/DankFocusTime)
- Preview: [UI](https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/ui.png) | [Settings](https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/setting.png)
- Demo: Pending
- Status: `Beta`
- Summary: Track focused-window time and browse per-app focus history from a bar popout.

**Template**

```md
### Plugin Name

- Plugin: `plugin-id`
- Type: `Widget / Launcher / Daemon / Desktop`
- Repository: [GitHub](https://github.com/<user>/<repo>)
- Preview: [UI](https://example.com/ui.png) | [Settings](https://example.com/settings.png)
- Demo: [Video](https://example.com/demo)
- Status: `Active`
- Summary: one-line explanation of what makes the plugin useful
```

## Plugin Directory

Add one row per public or released plugin.

| Plugin | Type | Repository | Preview | Demo | DMS | Status | Summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dank Translate | Widget | [GitHub](https://github.com/handsomedogx/DankTranslate) | [UI](https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/ui.png) / [Settings](https://raw.githubusercontent.com/handsomedogx/DankTranslate/main/assets/setting.png) | Pending | 1.4+ | Beta | Translate English and Chinese text from a popout or screenshot OCR workflow. |
| Dank Focus Time | Widget | [GitHub](https://github.com/handsomedogx/DankFocusTime) | [UI](https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/ui.png) / [Settings](https://raw.githubusercontent.com/handsomedogx/DankFocusTime/main/assets/setting.png) | Pending | 1.4+ | Beta | Track focused-window time and browse per-app focus history from a bar popout. |

**Template for a new row**

```md
| Plugin Name | Widget / Launcher / Daemon / Desktop | [GitHub](https://github.com/<user>/<repo>) | [UI](https://example.com/ui.png) / [Settings](https://example.com/settings.png) | [Video](https://example.com/demo) | 1.4+ | Active | Short one-line description |
```

**Recommended status labels**

- `Planned`
- `Active`
- `Beta`
- `Archived`

## Demo And Media

Each public plugin entry should eventually have:

- one repository link
- one screenshot preview or demo video link
- one concise summary
- one compatibility note if needed

Optional media can either stay in each plugin repository and be embedded here with raw GitHub links, or live under `assets/` in this index repository:

```text
assets/
└── <plugin-id>/
    ├── cover.png
    ├── thumb.png
    └── notes.txt
```

**Recommended media coverage:**

- show the widget or entry point immediately
- include both the primary UI and the settings view when using screenshots
- keep demo videos focused on one real interaction instead of only static screenshots

## Standards

Shared development standards for all plugins are maintained in [AGENTS.md](./AGENTS.md).

**Core rules**

- this root repository tracks standards and navigation only
- each plugin must have its own independent Git repository
- plugin repositories should follow the shared DMS workflow documented in `AGENTS.md`
- commit messages use the format `<type>: <summary>`

**Examples**

- `feat: add weather plugin entry`
- `docs: update plugin publishing rules`
- `fix: correct repository link for launcher plugin`

## Release Model

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
    ├── .gitkeep
    └── icons/
```

## Roadmap

- add more live plugin entries after repository migration
- add demo video links for published plugins
- add thumbnails or covers for each public plugin
- add compatibility notes across DMS versions
- add release and changelog links for each plugin
