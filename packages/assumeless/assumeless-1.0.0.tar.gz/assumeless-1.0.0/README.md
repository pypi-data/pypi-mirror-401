# Assumeless

### An Assumptions-First Diagnostic Tool For Python

---

<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=008080&height=200&section=header&text=Assumeless&fontSize=80&animation=fadeIn&fontAlignY=35&" width="100%" alt="Assumeless Banner" />

  <br />

  <img src="https://img.shields.io/badge/Status-Stable-00C853?style=for-the-badge&logo=check&logoColor=white" />
  <img src="https://img.shields.io/badge/Version-1.1.0-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Maintained-Yes-1DE9B6?style=for-the-badge&logo=github&logoColor=white" />
  <br/>
  <img src="https://img.shields.io/badge/Tech-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Tech-AST-success?style=for-the-badge&logo=code&logoColor=white" />
  <img src="https://img.shields.io/badge/Tech-CLI-F7DF1E?style=for-the-badge&logo=terminal&logoColor=black" />
  <br/>
  <img src="https://img.shields.io/badge/License-Apache--2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" />

  <br /><br />

  <h2>Stop Guessing. Start Assuming Less.</h2>

  <br/><br/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&pause=1000&color=008080&center=true&vCenter=true&width=435&lines=Detect+Risky+Assumptions;Prevent+Silent+Faliures;Audit+Documentation+Drift)](https://git.io/typing-svg)
</div>


---

## Project Overview

> **Assumeless** is a specialized static analysis tool designed to surface **dangerous hidden assumptions** in your code.

Unlike traditional linters that focus on style or syntax errors, Assumeless audits your codebase for semantic fragility—places where the code "assumes" success without ensuring it.

**Key Goals:**
* **Reliability:** Detect undefined behavior like silent exception swallowing.
* **Security:** Identify hardcoded paths, secrets, and environment dependencies.
* **Integrity:** Ensure documentation matches the reality of your implementation.

---

## Tech Stack

<div align="center">

| Core | Analysis | Interface | Formatting |
| :---: | :---: | :---: | :---: |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="50" alt="Python" /> | <img src="https://img.shields.io/badge/AST-Parser-green?style=flat-square&logo=python&logoColor=white" height="50" alt="AST" /> | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bash/bash-original.svg" height="50" alt="CLI" /> | <img src="https://img.shields.io/badge/Rich-Text-red?style=flat-square&logo=markdown&logoColor=white" height="50" alt="Rich" /> |
| **Python 3.9+** | **AST Visitor** | **Click CLI** | **Rich** |

</div>

---

## CLI Showcase

*Assumeless provides a suite of 10+ standardized commands for every workflow.*

<div align="center">

| Scan Mode | Doctor Mode | Docs Check |
|:----------:|:-----------:|:------------:|
| `assumeless scan` | `assumeless doctor` | `assumeless docs` |
| Fast, minimal CI output | Human-readable diagnosis | Detect documentation drift |

</div>

### Key Commands

```bash
# Quick diagnostics for CI/CD
$ assumeless scan . --json

# Detailed human-readable report
$ assumeless doctor

# Check if README.md matches code reality
$ assumeless docs

# List all active rules
$ assumeless rules
```

---

## Active Rules

Assumeless enforces a strict catalog of assumption checks:

| ID | Name | Description |
| :--- | :--- | :--- |
| `AL-ERR-01` | **Silent Exception** | `except:` blocks that swallow errors silently. |
| `AL-ERR-02` | **Broad Catch** | `except Exception:` without logging re-raise. |
| `AL-ENV-01` | **Direct Env Var** | `os.environ["KEY"]` which crashes if missing. |
| `AL-PATH-01` | **Hardcoded Path** | Absolute file paths that break portability. |
| `AL-PATH-08` | **Unclosed File** | `open()` calls without context managers. |
| `AL-GLOB-07` | **Mutable Default** | Function arguments like `def foo(x=[]):`. |
| `AL-DOC-XX` | **Docs Drift** | Mismatches between docs and code. |

---

## License & Credits

<div align="center">

This Project is licensed under the **Apache-2.0 License**.


<img src="https://img.shields.io/badge/License-Apache--2.0-red.svg" alt="Apache License" />

---

### Developed by **Huntwter**

<a href="https://github.com/huntwter">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

<br />

*Built with a focus on reliability, maintainability, and truth.*

<img src="https://capsule-render.vercel.app/api?type=waving&color=00B4D8&height=100&section=footer" width="100%" />

</div>
