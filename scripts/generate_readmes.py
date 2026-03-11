#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import urllib.parse
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

LANGUAGE_NAMES = {
    "en": "English",
    "zh-CN": "Simplified Chinese",
}

TYPE_LABELS = {
    "widget": {"en": "Widget", "zh-CN": "Widget"},
    "launcher": {"en": "Launcher", "zh-CN": "Launcher"},
    "daemon": {"en": "Daemon", "zh-CN": "Daemon"},
    "desktop": {"en": "Desktop", "zh-CN": "Desktop"},
}

STATUS_LABELS = {
    "planned": {"en": "Planned", "zh-CN": "计划中"},
    "active": {"en": "Active", "zh-CN": "活跃"},
    "beta": {"en": "Beta", "zh-CN": "测试中"},
    "archived": {"en": "Archived", "zh-CN": "已归档"},
}

UI_SOURCE = {
    "generated_notice": "此文件为自动生成，请修改 `content/site.json` 或 `scripts/generate_readmes.py`。",
    "start_here": "快速入口",
    "at_a_glance": "仓库结构总览",
    "featured": "精选插件",
    "featured_intro": "这里用于展示你最希望访客优先看到的插件，尽量保持简洁和可视化。",
    "coming_soon": "即将加入",
    "plugin": "插件",
    "type": "类型",
    "repository": "仓库",
    "demo": "演示",
    "status": "状态",
    "summary": "简介",
    "add_repo": "补充 GitHub 链接",
    "add_demo": "补充视频链接",
    "planned": "计划中",
    "placeholder_summary": "一句话说明这个插件的价值",
    "featured_template": "模板",
    "featured_template_block": "### 插件名称\n\n- 插件: `plugin-id`\n- 类型: `Widget / Launcher / Daemon / Desktop`\n- 仓库: [GitHub](https://github.com/<user>/<repo>)\n- 演示: [Video](https://example.com/demo)\n- 状态: `活跃`\n- 简介: 用一句话说明这个插件为什么有用",
    "directory": "插件目录",
    "directory_intro": "每个公开或已发布的插件都在这里保留一行条目。",
    "dms": "DMS",
    "directory_row_template": "| 插件名称 | Widget / Launcher / Daemon / Desktop | [GitHub](https://github.com/<user>/<repo>) | [Video](https://example.com/demo) | 1.4+ | 活跃 | 一句话描述 |",
    "template_for_row": "新增条目模板",
    "recommended_statuses": "推荐状态标签",
    "status_active": "活跃",
    "status_beta": "测试中",
    "status_archived": "已归档",
    "demo_media": "演示与素材",
    "demo_media_intro": "每个公开插件条目最终最好都包含：",
    "media_repo": "一个仓库链接",
    "media_demo": "一个演示视频链接",
    "media_summary": "一条简洁摘要",
    "media_compat": "必要时补一条兼容性说明",
    "media_local": "可选的本地素材可以按插件 id 或仓库名放在 `assets/` 下：",
    "media_coverage": "推荐的演示内容：",
    "coverage_entry": "前几秒先展示组件或入口位置",
    "coverage_flow": "30 到 60 秒内完整展示一条主流程",
    "coverage_real": "尽量展示真实交互，而不是只放静态截图",
    "standards": "统一规范",
    "standards_intro": "所有插件共享的开发规范都维护在 [AGENTS.md](./AGENTS.md) 中。",
    "core_rules": "核心规则",
    "rule_root": "根仓库只跟踪规范、导航和展示信息",
    "rule_repo": "每个插件都必须拥有独立 Git 仓库",
    "rule_workflow": "插件仓库应遵循 `AGENTS.md` 中的共享 DMS 工作流",
    "rule_commit": "提交信息统一使用 `<type>: <summary>` 格式",
    "examples": "示例",
    "example_1": "`feat: add weather plugin entry`",
    "example_2": "`docs: update plugin publishing rules`",
    "example_3": "`fix: correct repository link for launcher plugin`",
    "release_model": "发布模型",
    "release_steps": [
        "在各自独立仓库中开发和维护插件",
        "在插件仓库中记录安装方式和使用说明",
        "发布演示素材",
        "将仓库链接和视频链接回填到这里",
        "在插件变化时同步更新兼容性和状态"
    ],
    "repo_layout": "仓库结构",
    "roadmap": "后续计划",
    "language_en": "English",
    "language_zh": "简体中文",
}

UI_FALLBACKS = {
    "en": {
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
        "language_zh": "简体中文",
    }
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


class OpenAITranslator(Translator):
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def translate_many(self, texts: list[str], source_lang: str, target_lang: str) -> list[str]:
        if not texts:
            return []

        payload = {
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a translation engine. "
                        f"Translate each input from {LANGUAGE_NAMES[source_lang]} to {LANGUAGE_NAMES[target_lang]}. "
                        "Preserve Markdown, inline code, fenced code blocks, URLs, file paths, plugin ids, repo names, "
                        "and link targets. Return strict JSON in the form "
                        "{\"translations\": [\"...\"]}. Do not add commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps({"texts": texts}, ensure_ascii=False),
                },
            ],
        }
        response = post_json(
            f"{self.base_url}/chat/completions",
            payload,
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise TranslationError(f"OpenAI translation response was malformed: {response!r}") from exc

        parsed = parse_json_text(content)
        translations = parsed.get("translations")
        if not isinstance(translations, list) or len(translations) != len(texts):
            raise TranslationError("OpenAI translation result did not return the expected translations array.")
        return [str(item) for item in translations]


class DeepLTranslator(Translator):
    def __init__(self, api_key: str, api_url: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_url = api_url

    def translate_many(self, texts: list[str], source_lang: str, target_lang: str) -> list[str]:
        if not texts:
            return []

        deepl_langs = {
            "en": "EN",
            "zh-CN": "ZH",
        }
        if source_lang not in deepl_langs or target_lang not in deepl_langs:
            raise TranslationError(f"DeepL does not support the configured language pair: {source_lang} -> {target_lang}")

        form_parts = [("source_lang", deepl_langs[source_lang]), ("target_lang", deepl_langs[target_lang])]
        for text in texts:
            form_parts.append(("text", text))

        response = post_form(
            self.api_url,
            form_parts,
            {
                "Authorization": f"DeepL-Auth-Key {self.api_key}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        translations = response.get("translations")
        if not isinstance(translations, list) or len(translations) != len(texts):
            raise TranslationError("DeepL translation result did not return the expected translations array.")
        return [str(item["text"]) for item in translations]


def load_content() -> dict[str, Any]:
    return json.loads(CONTENT_PATH.read_text(encoding="utf-8"))


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def post_form(url: str, pairs: list[tuple[str, str]], headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(pairs).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_json_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if "\n" in stripped:
            stripped = stripped.split("\n", 1)[1]
        if stripped.endswith("```"):
            stripped = stripped[:-3]
        stripped = stripped.strip()
    return json.loads(stripped)


def build_translator() -> Translator | None:
    provider = os.getenv("README_TRANSLATOR_PROVIDER", "").strip().lower()
    if not provider:
        if os.getenv("README_TRANSLATOR_OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("README_TRANSLATOR_DEEPL_API_KEY"):
            provider = "deepl"
        else:
            return None

    if provider == "openai":
        api_key = os.getenv("README_TRANSLATOR_OPENAI_API_KEY")
        if not api_key:
            raise TranslationError("README_TRANSLATOR_OPENAI_API_KEY is required when README_TRANSLATOR_PROVIDER=openai.")
        base_url = os.getenv("README_TRANSLATOR_OPENAI_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("README_TRANSLATOR_OPENAI_MODEL", "gpt-4.1-mini")
        return OpenAITranslator(api_key=api_key, base_url=base_url, model=model)

    if provider == "deepl":
        api_key = os.getenv("README_TRANSLATOR_DEEPL_API_KEY")
        if not api_key:
            raise TranslationError("README_TRANSLATOR_DEEPL_API_KEY is required when README_TRANSLATOR_PROVIDER=deepl.")
        api_url = os.getenv("README_TRANSLATOR_DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")
        return DeepLTranslator(api_key=api_key, api_url=api_url)

    raise TranslationError(f"Unsupported translator provider: {provider}")


class RenderContext:
    def __init__(self, lang: str, source_lang: str, translator: Translator | None) -> None:
        self.lang = lang
        self.source_lang = source_lang
        self.translator = translator

    def translate_or_fallback(self, text: str, fallback: str | None = None) -> str:
        if self.lang == self.source_lang:
            return text
        if self.translator is not None:
            return self.translator.translate(text, self.source_lang, self.lang)
        if fallback is not None:
            return fallback
        raise TranslationError(
            f"No translator is configured for {self.source_lang} -> {self.lang}. "
            "Set README_TRANSLATOR_OPENAI_API_KEY or README_TRANSLATOR_DEEPL_API_KEY."
        )

    def ui(self, key: str) -> str:
        source = UI_SOURCE[key]
        fallback = UI_FALLBACKS.get(self.lang, {}).get(key)
        if isinstance(source, list):
            translated = [self.translate_or_fallback(item, (fallback or [None] * len(source))[index] if isinstance(fallback, list) else None)
                for index, item in enumerate(source)]
            return "\n".join(translated)
        return self.translate_or_fallback(source, fallback if isinstance(fallback, str) else None)

    def localized_value(self, value: Any, *, translate_plain: bool = True) -> str:
        if isinstance(value, dict):
            if self.lang in value:
                return str(value[self.lang])
            if self.source_lang in value:
                source_value = str(value[self.source_lang])
                fallback = None
                if self.lang in value:
                    fallback = str(value[self.lang])
                return self.translate_or_fallback(source_value, fallback)
            if "en" in value and self.lang == "en":
                return str(value["en"])
            raise TranslationError(f"Unable to localize value for {self.lang}: {value!r}")

        if isinstance(value, str):
            if not translate_plain:
                return value
            return self.translate_or_fallback(value)

        raise TranslationError(f"Unsupported localized value: {value!r}")

    def localized_list(self, values: Any) -> list[str]:
        if isinstance(values, dict):
            if self.lang in values:
                selected = values[self.lang]
                should_translate = False
            elif self.source_lang in values:
                selected = values[self.source_lang]
                should_translate = self.lang != self.source_lang
            else:
                raise TranslationError(f"Unsupported localized list: {values!r}")

            result = []
            for item in selected:
                if isinstance(item, dict):
                    result.append(self.localized_value(item))
                else:
                    text = str(item)
                    result.append(self.translate_or_fallback(text) if should_translate else text)
            return result
        if isinstance(values, list):
            return [self.localized_value(item) if isinstance(item, dict) else self.translate_or_fallback(str(item)) for item in values]
        raise TranslationError(f"Unsupported localized list: {values!r}")


def icon(name: str, alt: str, width: int = 18) -> str:
    return f'<img src="./assets/icons/{name}" width="{width}" alt="{alt}" />'


def link(label: str, href: str) -> str:
    return f"[{label}]({href})"


def maybe_link(label: str, href: str, fallback: str) -> str:
    return link(label, href) if href else fallback


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def type_label(value: str, lang: str) -> str:
    return TYPE_LABELS.get(value, {}).get(lang, value)


def status_label(value: str, lang: str) -> str:
    return STATUS_LABELS.get(value, {}).get(lang, value)


def render_language_switch(ctx: RenderContext) -> str:
    if ctx.lang == "en":
        return f"**{ctx.ui('language_en')}** | [简体中文](./README.zh-CN.md)"
    return f"[English](./README.md) | **{ctx.ui('language_zh')}**"


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
                f"- {ctx.ui('type')}: `{type_label('widget', ctx.lang)}`",
                f"- {ctx.ui('repository')}: {ctx.ui('add_repo')}",
                f"- {ctx.ui('demo')}: {ctx.ui('add_demo')}",
                f"- {ctx.ui('status')}: `{ctx.ui('planned')}`",
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
                    f"- {ctx.ui('type')}: `{type_label(item['type'], ctx.lang)}`",
                    f"- {ctx.ui('repository')}: {maybe_link('GitHub', item.get('repository_url', ''), ctx.ui('add_repo'))}",
                    f"- {ctx.ui('demo')}: {maybe_link('Video', item.get('demo_url', ''), ctx.ui('add_demo'))}",
                    f"- {ctx.ui('status')}: `{status_label(item.get('status', 'planned'), ctx.lang)}`",
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
            f"| _{ctx.ui('coming_soon')}_ | {type_label('widget', ctx.lang)} | {ctx.ui('add_repo')} | {ctx.ui('add_demo')} | 1.4+ | {ctx.ui('planned')} | {ctx.ui('placeholder_summary')} |"
        )
    else:
        for item in content["plugins"]:
            item_name = ctx.localized_value(item["name"], translate_plain=False) if isinstance(item["name"], dict) else str(item["name"])
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_cell(item_name),
                        escape_cell(type_label(item["type"], ctx.lang)),
                        escape_cell(maybe_link("GitHub", item.get("repository_url", ""), ctx.ui("add_repo"))),
                        escape_cell(maybe_link("Video", item.get("demo_url", ""), ctx.ui("add_demo"))),
                        escape_cell(item.get("dms", "1.4+")),
                        escape_cell(status_label(item.get("status", "planned"), ctx.lang)),
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
            f"- `{ctx.ui('planned')}`",
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

    release_steps = UI_SOURCE["release_steps"] if ctx.lang == ctx.source_lang else UI_FALLBACKS.get(ctx.lang, {}).get("release_steps")
    if release_steps is None:
        release_steps = [ctx.translate_or_fallback(step) for step in UI_SOURCE["release_steps"]]
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
    source_lang = content.get("source_language", "zh-CN")
    translator = build_translator()

    for lang, path in LANGS.items():
        ctx = RenderContext(lang=lang, source_lang=source_lang, translator=translator)
        path.write_text(render_readme(content, ctx), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
