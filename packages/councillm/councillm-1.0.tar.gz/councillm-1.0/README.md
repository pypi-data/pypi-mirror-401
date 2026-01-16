# councillm

**councillm** is a lightweight, transparent *LLM Council* framework built on **Ollama**. It orchestrates multiple local language models into a structured decision-making pipeline inspired by Andrej Karpathy’s *LLM Council* concept — but designed for **local-first**, **observable**, and **practical CLI usage**.

This project focuses on **correctness, transparency, and control**, not theatrics.
---
<a href="https://github.com/Rktim/ezyml/blob/main/LICENSE">
  <img alt="License" src="https://img.shields.io/github/license/Rktim/ezyml?color=blue">
</a>

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/councillm?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=BRIGHTGREEN&left_text=downloads)](https://pepy.tech/projects/councillm)
---
## ✨ Key Features

* 🔁 **Multi‑Model Reasoning** (Generator → Critic → Chairman)
* 🧠 **Fast / Lite / Full execution modes**
* 🔍 Optional **web‑search grounding**
* 👁️ **Transparent execution logs** — see each model work
* 🖥️ **Local‑only** (no OpenAI / no cloud)
* ⚡ **Fast install with `uv`**

---

## 🏗️ Council Architecture

The system follows a strict, inspectable pipeline:

```
User Question
   ↓
[Generators]  → produce independent drafts
   ↓
[Critics]     → review & rank drafts (optional)
   ↓
[Chairman]   → synthesize final answer
```

Each stage is logged in real time so users can verify that the council is *actually running*.

---

## 📦 Installation (Fast with uv)

### Prerequisites

* Python **3.10+**
* **Ollama** installed and running
* At least **2 local Ollama models** pulled

```bash
ollama pull mistral
ollama pull llama3
```

### Install with `uv`

```bash
uv pip install councillm
```

Or for development:

```bash
git clone https://github.com/yourname/councillm.git
cd councillm
uv pip install -e .
```

---

## 🚀 Quick Start

Run the CLI:

```bash
councillm
```

You will be prompted to configure the council **once per session**.

---

## ⚙️ Interactive Configuration

Instead of editing YAML files, **councillm asks you directly**:

```
Assign GENERATOR models (comma‑separated):
> mistral:latest, llama3:8b

Assign CRITIC models (comma‑separated):
> phi3:latest

Assign CHAIRMAN model:
> gemma3:1b
```

✔ No files are written
✔ No auto‑detection
✔ No hidden state

---

## 🧩 Execution Modes

After configuration, choose how the council runs:

### 1️⃣ Fast Mode

```
Chairman answers directly
```

* Fastest
* Lowest cost
* Least robust

### 2️⃣ Lite Mode (Default)

```
Generator → Chairman
```

* Balanced
* Good for daily use

### 3️⃣ Full Mode

```
Multiple Generators → Critics → Chairman
```

* Most reliable
* Slowest
* Maximum cross‑checking

---

## 🔍 Web Search Grounding

You can optionally enable web search:

```
Enable web search grounding? [y/N]: y
```

This uses DuckDuckGo search results to reduce hallucinations for factual queries.

---

## 🖥️ Example Session

```text
$ councillm

======================================================================
        LLM COUNCIL — OLLAMA CONSOLE MODE
======================================================================
Type your question and press Enter.
Type 'exit' to quit.

Council ready (mode=full, search=True).

You: who won the 2020 F1 drivers championship?

[Stage 1] Generating responses
  • mistral:latest ✓
  • llama3:8b ✓

[Stage 2] Peer review
  • phi3:latest ✓

[Stage 3] Chairman synthesis
  • gemma3:1b ✓

Final Answer:
Lewis Hamilton won the 2020 Formula 1 Drivers' Championship.
```

---

## 🧪 Hallucination Mitigation Strategy

councillm reduces hallucinations by:

* Multiple independent generations
* Cross‑model critique
* Chairman synthesis
* Optional web grounding

⚠️ **Still not perfect** — this is *risk reduction*, not elimination.

---


## ❌ What councillm Is NOT

* ❌ Not a chatbot UI
* ❌ Not a prompt playground
* ❌ Not a guarantee of truth
* ❌ Not cloud‑based

This is a **reasoning orchestrator**, not a demo app.

---

## 📜 License

MIT License

You are free to use, modify, and distribute this project.

---


## 🤝 Contributing

Contributions are welcome if they:

* Improve correctness
* Reduce hallucinations
* Increase transparency
* Keep the system simple

---

## 🧠 Philosophy

> "If you can’t observe it, you can’t trust it."

councillm exists to make **local LLM reasoning inspectable, not magical**.

---

Happy reasoning 🚀
