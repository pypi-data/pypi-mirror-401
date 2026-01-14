# PromptScope 🧠🔍

**Effortless Observability for LLM Prompts**

**Treat your prompts like code. Version, diff, replay, and debug them with ease.**

[![PyPI version](https://badge.fury.io/py/promptscope.svg)](https://badge.fury.io/py/promptscope)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/promptscope-dev/promptscope)](https://github.com/promptscope-dev/promptscope/issues)
[![GitHub stars](https://img.shields.io/github/stars/promptscope-dev/promptscope?style=social)](https://github.com/promptscope-dev/promptscope/stargazers)

---

## 🤔 The Problem

In most LLM-powered apps today:
- Prompts are unversioned strings scattered across the codebase.
- Small changes can silently break behavior in unexpected ways.
- No one knows *why* an output suddenly changed.
- Reproducing bugs is a painful, manual process.
- Upgrading to a new model is risky and hard to validate.

**PromptScope fixes this.** It brings the principles of Git-like version control and observability to your LLM prompts, so you can build more reliable and predictable AI applications.

---

## ✨ Key Features

- ** automático Automatic Versioning:** Every change to a prompt's content, model, or parameters creates a new, immutable version. No manual tracking required.
- **🔍 Intelligent Diffing:** See exactly what changed between any two versions of a prompt, from a single word to a temperature setting.
- **🛡️ Budget Guards:** Optional `max_cost` thresholds prevent runaway responses and surprise bills.
- **📦 One-Command Export:** Dump every tracked prompt/version to portable JSON for backup or migration.
- **⏳ Time-Travel Replay:** Re-run any historical prompt version to reproduce outputs, debug issues, or compare model performance. (Coming Soon)
- **📈 Performance Tracking:** Monitor cost, latency, and quality metrics for each prompt over time. (Coming Soon)
- **🚨 Drift Detection:** Get alerted when prompt outputs change unexpectedly or degrade in quality. (Coming Soon)
- **🔌 Seamless Integration:** Works with popular libraries like OpenAI, with more integrations planned.

---

## 🚀 Quick Start

Get up and running with PromptScope in less than a minute.

**1. Install PromptScope:**
```bash
pip install promptscope
```

**2. Set up your OpenAI API key:**
```bash
export OPENAI_API_KEY="your-api-key"
```

**3. Use the `PromptScopeOpenAI` client in your code:**

It's a drop-in replacement for the standard `openai.OpenAI` client, but with added powers.

```python
# your_app.py
from promptscope.openai import PromptScopeOpenAI

# Use it just like the regular OpenAI client
# Caching and retries are enabled by default!
# Optional: set max_cost (USD) to guard against expensive responses
client = PromptScopeOpenAI(retries=3, max_cost=0.01)

def generate_summary(text: str):
    # This prompt will be automatically tracked by PromptScope
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        # Track this prompt under the name "text_summarizer"
        # This is a custom parameter for PromptScope
        extra_body={"prompt_name": "text_summarizer"}
    )
    return response.choices[0].message.content

# Your prompt and its response are now saved and versioned in PromptScope!
summary = generate_summary("LLMs are transforming the way we build software...")
print(summary)
```

**4. Explore your prompt history with the CLI:**

Now you can use the `promptscope` CLI to inspect what happened — and even export everything.

```bash
# List all tracked prompts
promptscope list

# Show the history of your summarizer prompt
promptscope show text_summarizer

# Diff the latest version with the previous one
promptscope diff text_summarizer --from-version previous --to-version latest

# Export all prompts/versions to JSON
promptscope export --pretty --out promptscope_export.json
```

---

## ⚙️ Installation

You can install PromptScope using pip:

```bash
pip install promptscope
```

### Database Configuration

By default, PromptScope uses a local SQLite database (`promptscope.db`) in your current working directory.

To specify a different path, set the `PROMPTSCOPE_DB` environment variable:
```bash
export PROMPTSCOPE_DB=/path/to/your/promptscope.db
```

---

## 📚 Usage

### Python Library

The `PromptScopeOpenAI` and `PromptScopeAsyncOpenAI` clients are the easiest way to integrate PromptScope into your application. They are drop-in replacements for the standard OpenAI clients and automatically handle prompt tracking, versioning, caching, and retries.

To track a prompt, pass an `extra_body` with a `prompt_name` to the `create` method:

```python
from promptscope.openai import PromptScopeOpenAI

client = PromptScopeOpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    extra_body={"prompt_name": "my_awesome_prompt"}
)
```

Any changes to the `model`, `messages`, or other parameters will create a new version of `my_awesome_prompt`.

#### Optional: add a budget guard

You can cap per-request cost to prevent runaway responses. Set `max_cost` (USD) when constructing the client; a `BudgetExceededError` is raised if the model response would exceed it.

```python
from promptscope.openai import PromptScopeOpenAI, BudgetExceededError

client = PromptScopeOpenAI(max_cost=0.02)  # cap each call at ~$0.02

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[...],
        extra_body={"prompt_name": "guarded_prompt"}
    )
except BudgetExceededError as exc:
    # Decide whether to retry with a cheaper model or alert the user
    print(f"Too expensive: {exc}")
```

### CLI

The `promptscope` CLI is your command center for prompt observability.

- `promptscope list`: List all tracked prompts.
- `promptscope show <prompt_name>`: Show the history and versions of a prompt.
- `promptscope diff <prompt_name>`: Diff two versions of a prompt.
- `promptscope replay <prompt_name>`: Replay a past prompt version.
- `promptscope export`: Export all prompts and versions to JSON (for backup or migration).

For detailed options, run `promptscope --help`.

---

## 🤝 Contributing

We love contributions from the community! Whether it's a bug report, a new feature, or an improvement to the documentation, we welcome your help.

Please see our [CONTRIBUTING.md](https://github.com/promptscope-dev/promptscope/blob/main/CONTRIBUTING.md) for detailed instructions on how to get started.

---

## 💬 Community

- **GitHub Issues:** Have a bug or feature request? [Open an issue](https://github.com/promptscope-dev/promptscope/issues).
- **Discord:** Join our community on [Discord](https://discord.gg/your-invite-link) for help, discussion, and to share your projects. (Link coming soon!)

---
> **PromptScope** is an open-source project created by [PromptScope Dev](https://github.com/promptscope-dev).
