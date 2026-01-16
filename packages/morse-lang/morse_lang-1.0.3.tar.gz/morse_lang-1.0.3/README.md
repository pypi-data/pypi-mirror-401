<div id="top" align="center">

  <h1>Morse Lang</h1>
  <p><em>A tiny programming language written entirely in Morse code.</em></p>

  <p>
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/morse-lang?style=flat&color=0080ff" />
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/morse-lang?style=flat&color=0080ff" />
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/sharky-3/morse-programming-language?style=flat&logo=git&logoColor=white&color=0080ff" />
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/sharky-3/morse-programming-language?style=flat&color=0080ff" />
    <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/sharky-3/morse-programming-language?style=flat&color=0080ff" />
  </p>

  <p><em>Built with:</em></p>
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white" />
    <img alt="Flask" src="https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white" />
  </p>

</div>

<br />
<hr />

## Table of Contents

- **[Overview](#overview)**
- **[How It Works](#how-it-works)**
- **[Quick Demo](#quick-demo)**
- **[Getting Started](#getting-started)**
  - **[Prerequisites](#prerequisites)**
  - **[Installation (from PyPI)](#installation-from-pypi)**
  - **[Installation (from source)](#installation-from-source)**
  - **[Running Your First Morse Program](#running-your-first-morse-program)**
- **[Language Basics](#language-basics)**
- **[Web Frontend (Text ⇄ Morse Translator)](#web-frontend-text--morse-translator)**
- **[Development](#development)**

<hr />

## Overview

**Morse Lang** lets you write Python code, but the source itself is Morse code.

You write a `.mc` file using dots (`.`) and dashes (`-`), the `morse` CLI decodes it into Python, and then executes it.  
It works the same way on **macOS**, **Windows**, and **Linux** as long as you have Python installed.

**Use cases**

- **Learning / teaching Morse code** with a fun programming twist
- **Code golf / esolangs** and experimentation
- **Novel demos** where the source file looks like radio traffic but runs like Python

<hr />

## How It Works

- **Step 1 – Morse source (`.mc`):**  
  You create a file filled with Morse symbols (e.g. `.-`, `--..--`) separated by spaces.

- **Step 2 – Decode to Python:**  
  The CLI uses `morse_lang.morse_to_text` and `MORSE_MAP` to translate each Morse token into a character, building a normal Python source file line by line.

- **Step 3 – Execute:**  
  The decoded Python string is executed with `exec(...)` in a fresh namespace, just like running a regular `.py` script.

Because of this, **Morse Lang programs can do anything Python can**. Only run `.mc` files you trust, just as you would with untrusted Python code.

<hr />

## Quick Demo

If you have cloned this repo, you can immediately run the included `hello.mc`:

```bash
morse examples/hello.mc
```

This is equivalent to running the following Python:

```python
print('hello, world')
```

But the actual file only contains Morse:

```text
.--. .-. .. -. - -.--. .----. .... . .-.. .-.. --- --..--  .-- --- .-. .-.. -.. .----. -.--.-
```

<hr />

## Getting Started

### Prerequisites

- **Python:** 3.8 or newer (3.10+ recommended)
- Works on:
  - **macOS** (tested on recent versions)
  - **Windows 10/11**
  - **Linux** (any modern distro)

You can check your Python version with:

```bash
python --version
```

On Windows, you may need:

```powershell
py --version
```

### Installation (from PyPI)

The simplest way is to install the package directly from PyPI.

- **macOS / Linux (bash, zsh, etc.):**

```bash
python -m pip install --upgrade pip
python -m pip install morse-lang
```

- **Windows (PowerShell or Command Prompt):**

```powershell
py -m pip install --upgrade pip
py -m pip install morse-lang
```

After installation, the `morse` command should be available on your PATH.

### Installation (from source)

If you are working directly with this repository:

```bash
git clone https://github.com/sharky-3/morse-programming-language.git
cd morse-programming-language

# (Optional but recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -e .
```

This installs `morse-lang` in editable mode so changes to the source are reflected immediately.

### Running Your First Morse Program

#### 1. Using the included example

If you installed from PyPI and want to run your own `.mc` file:

1. Create a file, for example `hello.mc`, containing:

   ```text
   .--. .-. .. -. - -.--. .----. .... . .-.. .-.. --- --..--  .-- --- .-. .-.. -.. .----. -.--.-
   ```

2. Run it:

   - **macOS / Linux:**

     ```bash
     morse hello.mc
     ```

   - **Windows:**

     ```powershell
     morse hello.mc
     ```

You should see:

```text
hello, world
```

#### 2. If `morse` is not found on Windows

Sometimes PATH setup can be tricky. You can always fall back to:

```powershell
py -m morse_lang.cli path\to\file.mc
```

On macOS / Linux:

```bash
python -m morse_lang.cli path/to/file.mc
```

<hr />

## Language Basics

At its core, **Morse Lang is “Python in Morse”**. Each Morse token is mapped to a character:

- Single space (`" "`) between Morse codes → separates letters
- Triple space (`"   "`) between sequences → separates words
- Each line in your `.mc` file → one line of decoded Python

The mapping is defined in `MORSE_MAP` (letters, digits, operators, punctuation). Example:

- **Letters:** `.-` → `a`, `-...` → `b`, `....` → `h`, etc.
- **Digits:** `.....` → `5`, `--...` → `7`, etc.
- **Operators:**  
  - `.-.-.` → `+`  
  - `-...-` → `=`  
  - `-....-` → `-`  
  - `-..-.` → `/`  
  - `-.-.-` → `*`
- **Punctuation / grouping:**  
  - `--..--` → `,`  
  - `.----.` → `'`  
  - `-.--.` → `(`, `-.--.-` → `)`

### Example: variables and arithmetic

Python:

```python
let x = 5
print(x)
```

In Morse (spaces between letters, triple spaces between words):

```text
.-.. . -   -..-   -...-   .....      # let x = 5
.--. .-. .. -. - -.--. -..- -.--.-   # print(x)
```

When passed through `morse`, this decodes to the Python code and executes it.

You can combine any valid Morse characters into full Python programs (loops, functions, imports, etc.), as long as the decoded text is valid Python.

<hr />

## Web Frontend (Text ⇄ Morse Translator)

This repository also includes a small **Flask** web app that lets you convert between text and Morse interactively.

### Run the web UI (macOS & Windows)

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python app.py
```

Then open `http://localhost:5000` in your browser.

The page lets you:

- **Type text → get Morse code**
- **Paste Morse → get decoded text**

The web app uses the same `MORSE_MAP` as the CLI, so behavior is consistent.

<hr />

## Development

If you want to hack on Morse Lang itself:

- **Clone and install in editable mode:**

```bash
git clone https://github.com/sharky-3/morse-programming-language.git
cd morse-programming-language

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r requirements.txt
```

- **Run tests:**

```bash
python -m pip install pytest
pytest
```

- **Play with the internals:**
  - `morse_lang/lexer.py` – Morse → text decoding
  - `morse_lang/morse_map.py` – core Morse symbol map
  - `morse_lang/cli.py` – `morse` command-line entrypoint

You can now iterate on the language, extend the Morse mapping, or experiment with new features.

---

Enjoy writing code in dots and dashes!  
If you build something cool with Morse Lang, feel free to share it or open an issue/PR on the GitHub repo.
