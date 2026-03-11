#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT_PATH = ROOT / "content" / "site.json"
README_EN_PATH = ROOT / "README.md"
README_ZH_PATH = ROOT / "README.zh-CN.md"

LANGS = {
    "en": README_EN_PATH,
    "zh-CN": README_ZH_PATH,
}

TYPE_LABELS = {
    "widget": "Widget",
    "launcher": "Launcher",
    "daemon": "Daemon",
    "desktop": "Desktop",
}

STATUS_LABELS = {
    "planned": "Planned",
    "active": "Active",
    "beta": "Beta",
    "archived": "Archived",
}

UI_SOURCE = {
    "generated_notice": "AUTO-GENERATED FILE. Edit `content/site.json` or `scripts/generate_readmes.py` instead.",
    "start_here": "Start Here",
    "at_a_glance": "At A Glance",
    "featured": "Featured Plugins",
    "featured_intro": "Use this section for the plugins you want people to notice first. Keep it short and visual.",
    "coming_soon": "Coming Soon",
    "plugin": "Plugin",
    "type": "Type",
    "repository": "Repository",
    "demo": "Demo",
    "status": "Status",
    "summary": "Summary",
    "add_repo": "Add GitHub link",
    "add_demo": "Add video link",
    "planned": "Planned",
    "placeholder_summary": "Short one-line value proposition",
    "featured_template": "Template",
    "featured_template_block": "### Plugin Name\n\n- Plugin: `plugin-id`\n- Type: `Widget / Launcher / Daemon / Desktop`\n- Repository: [GitHub](https://github.com/<user>/<repo>)\n- Demo: [Video](https://example.com/demo)\n- Status: `Active`\n- Summary: one-line explanation of what makes the plugin useful",
    "directory": "Plugin Directory",
    "directory_intro": "Add one row per public or released plugin.",
    "dms": "DMS",
    "directory_row_template": "| Plugin Name | Widget / Launcher / Daemon / Desktop | [GitHub](https://github.com/<user>/<repo>) | [Video](https://example.com/demo) | 1.4+ | Active | Short one-line description |",
    "template_for_row": "Template for a new row",
    "recommended_statuses": "Recommended status labels",
    "status_active": "Active",
    "status_beta": "Beta",
    "status_archived": "Archived",
    "demo_media": "Demo And Media",
    "demo_media_intro": "Each public plugin entry should eventually have:",
    "media_repo": "one repository link",
    "media_demo": "one demo video link",
    "media_summary": "one concise summary",
    "media_compat": "one compatibility note if needed",
    "media_local": "Optional local media can live under `assets/` using the plugin id or repository name:",
    "media_coverage": "Recommended demo coverage:",
    "coverage_entry": "show the widget or entry point in the first few seconds",
    "coverage_flow": "show the main workflow in under 30 to 60 seconds",
    "coverage_real": "show one real interaction instead of only static screenshots",
    "standards": "Standards",
    "standards_intro": "Shared development standards for all plugins are maintained in [AGENTS.md](./AGENTS.md).",
    "core_rules": "Core rules",
    "rule_root": "this root repository tracks standards and navigation only",
    "rule_repo": "each plugin must have its own independent Git repository",
    "rule_workflow": "plugin repositories should follow the shared DMS workflow documented in `AGENTS.md`",
    "rule_commit": "commit messages use the format `<type>: <summary>`",
    "examples": "Examples",
    "example_1": "`feat: add weather plugin entry`",
    "example_2": "`docs: update plugin publishing rules`",
    "example_3": "`fix: correct repository link for launcher plugin`",
    "release_model": "Release Model",
    "release_steps": [
        "build and maintain the plugin in its own repository",
        "document installation and usage in that plugin repository",
        "publish demo material",
        "link the repository and video back here",
        "update compatibility and status when the plugin changes"
    ],
    "repo_layout": "Repository Layout",
    "roadmap": "Roadmap",
    "language_en": "English",
    "language_zh": "Simplified Chinese",
}


class TranslationError(RuntimeError):
    pass


class Translator:
    def __init__(self) -> None:
        self.cache: dict[tuple[str, str, str], str] = {}

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text or source_lang == target_lang:
            return text

        key = (source_lang, target_lang, text)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        translated = self.translate_many([text], source_lang, target_lang)[0]
        self.cache[key] = translated
        return translated

    def translate_many(self, texts: list[str], source_lang: str, target_lang: str) -> list[str]:
        raise NotImplementedError


class AzureTranslator(Translator):
    def __init__(self, api_key: str, endpoint: str, region: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")
        self.region = region

    def translate_many(self, texts: list[str], source_lang: str, target_lang: str) -> list[str]:
        if not texts:
            return []

        azure_langs = {
            "en": "en",
            "zh-CN": "zh-Hans",
        }
        if source_lang not in azure_langs or target_lang not in azure_langs:
            raise TranslationError(f"Azure Translator does not support the configured language pair: {source_lang} -> {target_lang}")

        payload = [{"text": text} for text in texts]
        response = post_json(
            f"{self.endpoint}/translate?api-version=3.0&from={azure_langs[source_lang]}&to={azure_langs[target_lang]}",
            payload,
            {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Ocp-Apim-Subscription-Region": self.region,
                "Content-Type": "application/json",
            },
        )

        if not isinstance(response, list) or len(response) != len(texts):
            raise TranslationError("Azure translation result did not return the expected response list.")

        translations: list[str] = []
        for item in response:
            try:
                translations.append(str(item["translations"][0]["text"]))
            except (KeyError, IndexError, TypeError) as exc:
                raise TranslationError(f"Azure translation response was malformed: {response!r}") from exc
        return translations


def load_content() -> dict[str, Any]:
    return json.loads(CONTENT_PATH.read_text(encoding="utf-8"))


def post_json(url: str, payload: Any, headers: dict[str, str]) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def build_translator() -> AzureTranslator | None:
    api_key = os.getenv("README_TRANSLATOR_AZURE_API_KEY")
    region = os.getenv("README_TRANSLATOR_AZURE_REGION")
    endpoint = os.getenv("README_TRANSLATOR_AZURE_ENDPOINT", "https://api.cognitive.microsofttranslator.com")

    if not api_key and not region:
        return None
    if not api_key:
        raise TranslationError("README_TRANSLATOR_AZURE_API_KEY is required to generate translated readmes.")
    if not region:
        raise TranslationError("README_TRANSLATOR_AZURE_REGION is required to generate translated readmes.")
    return AzureTranslator(api_key=api_key, endpoint=endpoint, region=region)


class RenderContext:
    def __init__(self, lang: str, source_lang: str, translator: AzureTranslator | None) -> None:
        self.lang = lang
        self.source_lang = source_lang
        self.translator = translator

    def translate_text(self, text: str) -> str:
        if self.lang == self.source_lang or not text:
            return text
        if self.translator is None:
            raise TranslationError(
                f"Azure translation credentials are required for {self.source_lang} -> {self.lang}. "
                "Set README_TRANSLATOR_AZURE_API_KEY and README_TRANSLATOR_AZURE_REGION."
            )
        return self.translator.translate(text, self.source_lang, self.lang)

    def ui(self, key: str) -> str:
        source = UI_SOURCE[key]
        if isinstance(source, list):
            translated = [self.translate_text(item) for item in source]
            return "\n".join(translated)
        return self.translate_text(source)

    def localized_value(self, value: Any, *, translate_plain: bool = True) -> str:
        if isinstance(value, dict):
            if self.source_lang not in value:
                raise TranslationError(
                    f"Localized dictionaries must provide the source language key `{self.source_lang}`: {value!r}"
                )
            source_value = str(value[self.source_lang])
            return source_value if not translate_plain else self.translate_text(source_value)

        if isinstance(value, str):
            return value if not translate_plain else self.translate_text(value)

        raise TranslationError(f"Unsupported localized value: {value!r}")

    def localized_list(self, values: Any) -> list[str]:
        if isinstance(values, dict):
            if self.source_lang not in values:
                raise TranslationError(
                    f"Localized lists must provide the source language key `{self.source_lang}`: {values!r}"
                )
            selected = values[self.source_lang]
            return [self.localized_value(item) if isinstance(item, dict) else self.translate_text(str(item)) for item in selected]

        if isinstance(values, list):
            return [self.localized_value(item) if isinstance(item, dict) else self.translate_text(str(item)) for item in values]

        raise TranslationError(f"Unsupported localized list: {values!r}")


def icon(name: str, alt: str, width: int = 18) -> str:
    return f'<img src="./assets/icons/{name}" width="{width}" alt="{alt}" />'


def link(label: str, href: str) -> str:
    return f"[{label}]({href})"


def maybe_link(label: str, href: str, fallback: str) -> str:
    return link(label, href) if href else fallback


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def type_label(value: str, ctx: RenderContext) -> str:
    return ctx.translate_text(TYPE_LABELS.get(value, value.replace("-", " ").replace("_", " ").title()))


def status_label(value: str, ctx: RenderContext) -> str:
    return ctx.translate_text(STATUS_LABELS.get(value, value.replace("-", " ").replace("_", " ").title()))


def render_language_switch(ctx: RenderContext) -> str:
    if ctx.lang == "en":
        return f"**{ctx.ui('language_en')}** | [{ctx.ui('language_zh')}](./README.zh-CN.md)"
    return f"[{ctx.ui('language_en')}](./README.md) | **{ctx.ui('language_zh')}**"


def render_highlights(content: dict[str, Any], ctx: RenderContext) -> str:
    cells = []
    for item in content["highlights"]:
        title = ctx.localized_value(item["title"])
        text = ctx.localized_value(item["text"])
        cells.append(
            "\n".join(
                [
                    '<td width="25%" valign="top">',
                    f'{icon(item["icon"], title, 20)}',
                    "",
                    f"<strong>{title}</strong><br />",
                    text,
                    "</td>",
                ]
            )
        )
    return "\n".join(["<table>", "<tr>", *cells, "</tr>", "</table>"])


def render_featured(content: dict[str, Any], ctx: RenderContext) -> list[str]:
    lines = [f"## {ctx.ui('featured')}", "", ctx.ui("featured_intro"), ""]
    if not content["featured"]:
        lines.extend(
            [
                f"### {ctx.ui('coming_soon')}",
                "",
                f"- {ctx.ui('plugin')}: `TBD`",
                f"- {ctx.ui('type')}: `{type_label('widget', ctx)}`",
                f"- {ctx.ui('repository')}: {ctx.ui('add_repo')}",
                f"- {ctx.ui('demo')}: {ctx.ui('add_demo')}",
                f"- {ctx.ui('status')}: `{status_label('planned', ctx)}`",
                f"- {ctx.ui('summary')}: {ctx.ui('placeholder_summary')}",
                "",
            ]
        )
    else:
        for item in content["featured"]:
            item_name = ctx.localized_value(item["name"], translate_plain=False) if isinstance(item["name"], dict) else str(item["name"])
            lines.extend(
                [
                    f"### {item_name}",
                    "",
                    f"- {ctx.ui('plugin')}: `{item['plugin_id']}`",
                    f"- {ctx.ui('type')}: `{type_label(item['type'], ctx)}`",
                    f"- {ctx.ui('repository')}: {maybe_link('GitHub', item.get('repository_url', ''), ctx.ui('add_repo'))}",
                    f"- {ctx.ui('demo')}: {maybe_link('Video', item.get('demo_url', ''), ctx.ui('add_demo'))}",
                    f"- {ctx.ui('status')}: `{status_label(item.get('status', 'planned'), ctx)}`",
                    f"- {ctx.ui('summary')}: {ctx.localized_value(item['summary'])}",
                    "",
                ]
            )

    lines.extend([f"**{ctx.ui('featured_template')}**", "", "```md", ctx.ui("featured_template_block"), "```"])
    return lines


def render_plugin_rows(content: dict[str, Any], ctx: RenderContext) -> list[str]:
    lines = [
        f"## {ctx.ui('directory')}",
        "",
        ctx.ui("directory_intro"),
        "",
        f"| {ctx.ui('plugin')} | {ctx.ui('type')} | {ctx.ui('repository')} | {ctx.ui('demo')} | {ctx.ui('dms')} | {ctx.ui('status')} | {ctx.ui('summary')} |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    if not content["plugins"]:
        lines.append(
            f"| _{ctx.ui('coming_soon')}_ | {type_label('widget', ctx)} | {ctx.ui('add_repo')} | {ctx.ui('add_demo')} | 1.4+ | {status_label('planned', ctx)} | {ctx.ui('placeholder_summary')} |"
        )
    else:
        for item in content["plugins"]:
            item_name = ctx.localized_value(item["name"], translate_plain=False) if isinstance(item["name"], dict) else str(item["name"])
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_cell(item_name),
                        escape_cell(type_label(item["type"], ctx)),
                        escape_cell(maybe_link("GitHub", item.get("repository_url", ""), ctx.ui("add_repo"))),
                        escape_cell(maybe_link("Video", item.get("demo_url", ""), ctx.ui("add_demo"))),
                        escape_cell(item.get("dms", "1.4+")),
                        escape_cell(status_label(item.get("status", "planned"), ctx)),
                        escape_cell(ctx.localized_value(item["summary"])),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            f"**{ctx.ui('template_for_row')}**",
            "",
            "```md",
            ctx.ui("directory_row_template"),
            "```",
            "",
            f"**{ctx.ui('recommended_statuses')}**",
            "",
            f"- `{status_label('planned', ctx)}`",
            f"- `{ctx.ui('status_active')}`",
            f"- `{ctx.ui('status_beta')}`",
            f"- `{ctx.ui('status_archived')}`",
        ]
    )
    return lines


def render_readme(content: dict[str, Any], ctx: RenderContext) -> str:
    title = content["title"] if isinstance(content["title"], str) else ctx.localized_value(content["title"], translate_plain=False)
    lines = [
        f"<!-- {ctx.ui('generated_notice')} -->",
        "",
        '<p align="center">',
        f'  <img src="./assets/icons/index.svg" width="92" alt="{title} icon" />',
        "</p>",
        "",
        f"# {title}",
        "",
        f"> {ctx.localized_value(content['tagline'])}",
        "",
        render_language_switch(ctx),
        "",
    ]

    for paragraph in ctx.localized_list(content["intro"]):
        lines.append(paragraph)

    lines.extend(["", f"## {ctx.ui('start_here')}", ""])
    for item in content["quick_links"]:
        lines.append(f"- {link(ctx.localized_value(item['label']), item['href'])}")

    lines.extend(["", f"## {ctx.ui('at_a_glance')}", "", render_highlights(content, ctx), ""])
    lines.extend(render_featured(content, ctx))
    lines.extend([""])
    lines.extend(render_plugin_rows(content, ctx))
    lines.extend(
        [
            "",
            f"## {ctx.ui('demo_media')}",
            "",
            ctx.ui("demo_media_intro"),
            "",
            f"- {ctx.ui('media_repo')}",
            f"- {ctx.ui('media_demo')}",
            f"- {ctx.ui('media_summary')}",
            f"- {ctx.ui('media_compat')}",
            "",
            ctx.ui("media_local"),
            "",
            "```text",
            "assets/",
            "└── <plugin-id>/",
            "    ├── cover.png",
            "    ├── thumb.png",
            "    └── notes.txt",
            "```",
            "",
            f"**{ctx.ui('media_coverage')}**",
            "",
            f"- {ctx.ui('coverage_entry')}",
            f"- {ctx.ui('coverage_flow')}",
            f"- {ctx.ui('coverage_real')}",
            "",
            f"## {ctx.ui('standards')}",
            "",
            ctx.ui("standards_intro"),
            "",
            f"**{ctx.ui('core_rules')}**",
            "",
            f"- {ctx.ui('rule_root')}",
            f"- {ctx.ui('rule_repo')}",
            f"- {ctx.ui('rule_workflow')}",
            f"- {ctx.ui('rule_commit')}",
            "",
            f"**{ctx.ui('examples')}**",
            "",
            f"- {ctx.ui('example_1')}",
            f"- {ctx.ui('example_2')}",
            f"- {ctx.ui('example_3')}",
            "",
            f"## {ctx.ui('release_model')}",
            "",
        ]
    )

    release_steps = UI_SOURCE["release_steps"] if ctx.lang == ctx.source_lang else [ctx.translate_text(step) for step in UI_SOURCE["release_steps"]]
    for index, step in enumerate(release_steps, start=1):
        lines.append(f"{index}. {step}")

    lines.extend(
        [
            "",
            f"## {ctx.ui('repo_layout')}",
            "",
            "```text",
            ".",
            "├── AGENTS.md",
            "├── README.md",
            "├── README.zh-CN.md",
            "├── content/",
            "│   └── site.json",
            "├── scripts/",
            "│   └── generate_readmes.py",
            "└── assets/",
            "    ├── .gitkeep",
            "    └── icons/",
            "```",
            "",
            f"## {ctx.ui('roadmap')}",
            "",
        ]
    )

    for item in ctx.localized_list(content["roadmap"]):
        lines.append(f"- {item}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    content = load_content()
    source_lang = content.get("source_language", "en")
    translator = build_translator()
    target_langs = [lang for lang in LANGS if lang != source_lang]

    if target_langs and translator is None:
        raise TranslationError(
            "Azure translation credentials are required to render translated readmes. "
            "Set README_TRANSLATOR_AZURE_API_KEY and README_TRANSLATOR_AZURE_REGION."
        )

    for lang, path in LANGS.items():
        ctx = RenderContext(lang=lang, source_lang=source_lang, translator=translator)
        path.write_text(render_readme(content, ctx), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
