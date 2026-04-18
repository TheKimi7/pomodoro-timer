# customizable pomodoro timer

a python terminal user interface (TUI) application that implements a structured and customizable pomodoro timer with multiple themes, live countdowns, progress bars, and keyboard-driven controls. built with [textual](https://textual.textualize.io).

---

## features

* multiple theme modes:
  * classic
  * soft study
  * focus mode
  * late-night workflow
  * cozy desk
  * monochrome minimal

* predefined timer configurations:
  * 25 minutes work / 5 minutes break
  * 30 minutes work / 5 minutes break
  * 50 minutes work / 10 minutes break

* fully customizable timer:
  * user-defined hours, minutes, and seconds for both study and break durations

* session-based execution:
  * supports multiple consecutive study sessions in a single run

* live TUI experience:
  * large LCD-style clock, live progress bar, phase status, and persistent header/footer
  * keyboard controls: `space` to pause/resume, `s` to skip the current phase, `q` to return to the menu, `esc` to go back a screen

* strong input validation:
  * invalid numeric inputs are rejected in-line without crashing the app

---

## requirements

* python 3.8+
* see `requirements.txt` (textual + its dependencies)

---

## setup

create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

on windows, activate the venv with `venv\Scripts\activate` instead.

---

## how to run

with the venv activated:

```bash
python pomodoro_timer_tui.py
```

or invoke the venv's python directly without activating:

```bash
./venv/bin/python pomodoro_timer_tui.py
```

---

## keyboard controls

| key       | action                              |
|-----------|-------------------------------------|
| `space`   | pause / resume the running timer    |
| `s`       | skip the current phase              |
| `q`       | return to the theme menu            |
| `esc`     | go back one screen                  |
| `ctrl+c`  | quit the app                        |

---

## project structure

* `pomodoro_timer_tui.py` → main TUI application
* `requirements.txt` → pinned python dependencies
* `venv/` → local virtual environment (git-ignored)

---

## concepts demonstrated

* textual-based TUI with multiple `Screen` subclasses
* reactive UI updates driven by `set_interval` ticks
* modular programming using functions and classes
* control flow (loops, conditionals) and state machines (prep → focus → break)
* input validation with try-except blocks
* code reusability and abstraction

---

## future improvements

* persistent session tracking using file handling
* sound / desktop notification integration
* per-theme color palettes (textual CSS)
* statistics screen summarizing completed sessions

---
