# 📜 FTAI — Foundational Traceable AI Interface

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/FolkTechAI/ftai-spec/actions/workflows/ftai-ci.yml/badge.svg)](https://github.com/FolkTechAI/ftai-spec/actions/workflows/ftai-ci.yml)

---

FTAI is a hybrid format for human–AI collaboration, designed to improve on JSON, Markdown, and YAML for AI-native workflows with a structured, minimal, human-readable protocol.

Built for serious AI developers, researchers, and agent architects — but accessible enough for new builders learning to speak to machines.

---

## 🚀 Why FTAI?

- **Readable by humans. Parseable by models.**
- **Deterministic:** Always yields the same structure across systems.
- **Traceable:** Embeds rationale, constraints, and memory scopes directly.
- **Composable:** Bridges cleanly into JSON, YAML, text embeddings, or pipelines.
- **Minimal:** No noisy punctuation, no nested spaghetti.
- **Multimodal:** Native support for image references and vision-capable models.

FTAI is Markdown for agents. JSON for intelligence. YAML for reasoning.

---

## 🖼️ Multimodal Support

FTAI natively handles image references for vision-capable AI models:

```ftai
@image
  src: ./screenshot.png
  alt: Application dashboard
  context: User is asking about the error shown in the top-right

@task
  analyze the image and identify the error message
@end
```

Images can be:
- Local file paths
- Base64 encoded inline
- URLs (when online processing is available)

This makes FTAI ideal for workflows involving screenshots, documents, diagrams, and visual context.

---

## 📦 Install

### From PyPI (Recommended)

```bash
pip install ftai-py
```

### From Source

```bash
git clone https://github.com/FolkTechAI/ftai-spec.git
cd ftai-spec
pip install -e .
```

---

## ⚡ Quick Start

```bash
# Lint an FTAI file
ftai lint myfile.ftai

# Lint with strict mode
ftai lint myfile.ftai --strict

# Lint with lenient mode (unknown tags as warnings)
ftai lint myfile.ftai --lenient

# Convert JSON to FTAI
ftai convert data.json > output.ftai

# Check version
ftai --version
```

---

## 🛠 What's Inside

| File/Directory | Purpose |
|----------------|---------|
| `src/ftai_linter/` | Python package with CLI and linter |
| `grammar/ftai.ebnf` | Formal syntax definition (EBNF) |
| `grammar/FTAI_grammar_syntax_v1.6.md` | Human-readable grammar spec |
| `parsers/swift/` | Swift parser implementation |
| `tests/vectors/pass/` | Valid FTAI examples |
| `tests/vectors/fail/` | Invalid FTAI examples (for testing) |
| `tools/json_to_ftai.py` | JSON → FTAI converter |
| `spec/example/` | Real-world FTAI examples |

---

## 📝 Basic Syntax

```ftai
@ftai v2.0 lang:en

@document
  title: "My First FTAI Document"
  author: "Your Name"
  created: 2026-01-09

@section Introduction
  This is a simple FTAI document demonstrating the format.

@task priority:high
  description: Review the quarterly report
  due: 2026-01-15
@end

@note
  Remember to check the appendix for supporting data.
```

### Core Tags

| Tag | Purpose |
|-----|---------|
| `@ftai` | Document header (required) |
| `@document` | Document metadata (required) |
| `@section` | Content section |
| `@task` | Actionable task (requires `@end`) |
| `@note` | Informational note |
| `@warning` | Important warning |
| `@config` | Configuration block (requires `@end`) |
| `@memory` | Memory/context block (requires `@end`) |
| `@image` | Image reference (multimodal) |
| `@table` | Tabular data |

---

## 🤝 Contributing

We welcome thoughtful contributors! All Pull Requests require signing our Contributor License Agreement (CLA) first.

### Local Development

```bash
git clone https://github.com/FolkTechAI/ftai-spec.git
cd ftai-spec
pip install -e .
pip install pytest

# Run tests
pytest tests/ -v

# Test the CLI
ftai lint tests/vectors/pass/pass_minimal.ftai
```

---

## 🛡 License & Governance

- **License:** [Apache 2.0](LICENSE)
- **Governance:** [GOVERNANCE.md](GOVERNANCE.md)
- **Security Disclosure:** [SECURITY.md](SECURITY.md)

FTAI is stewarded with transparent, reviewable releases — designed for long-term stability, not churn.

---

## 🌱 Built in the Open

FTAI is designed for the future of machine interaction: clear enough for a person, structured enough for a model, powerful enough for autonomous systems.

Built openly by [FolkTech AI](https://folktechai.com) with contributions from the community.

---

© 2025-2026 FolkTech AI — Format maintained by Michael Folk and contributors.
