# RPI-HID — Raspberry Pi USB HID Automation Library

RPI-HID is a Python library that allows a **Raspberry Pi Zero / Zero 2 W** to act as a **USB Human Interface Device (HID)**, emulating a keyboard to automate keystrokes on a connected system.

It provides a **high-level keyboard API** and an **advanced Rubber Ducky–style interpreter**, abstracting low-level HID report handling into clean, reusable Python functions.

---

## Features

* USB HID **keyboard emulation** via Linux USB gadget mode
* High-level keyboard automation API
* Advanced **Rubber Ducky–style script interpreter**
* Configurable typing delays and pauses
* Fast “paste-like” input (burst typing)
* Optional auto-run support using `systemd`
* Modular, extensible architecture
* Published on **PyPI**

---

## Supported Hardware

* Raspberry Pi Zero
* Raspberry Pi Zero 2 W

> ⚠️ Raspberry Pi 3/4/5 **do not support USB gadget mode**.

---

## Requirements

* Raspberry Pi OS (Lite recommended)
* Python ≥ 3.7
* USB OTG enabled (`dwc2`, `libcomposite`)
* Root access (required for `/dev/hidg0`)

---

## Installation

```bash
pip install rpi-hid
```

---

## Quick Start

```python
from rpi_hid import Keyboard

kbd = Keyboard()
kbd.winRun("notepad")
kbd.type("Hello from RPI-HID")
kbd.enter()
kbd.close()
```

---

# Keyboard API

## `Keyboard(delay: float = 0.02)`

Creates a keyboard HID interface.

**Arguments**

* `delay` — default delay between key presses (seconds)

```python
kbd = Keyboard(delay=0.03)
```

---

## `type(text: str, pause_after: float = 0.05)`

Types text character-by-character using HID.

**Arguments**

* `text` — string to type
* `pause_after` — pause after typing completes (seconds)

```python
kbd.type("Hello World")
```

---

## `paste(text: str)`

Fast burst typing that appears as **instant paste** (no per-key delay).

**Arguments**

* `text` — text to inject instantly

```python
kbd.paste("echo Hello World > test.txt")
kbd.enter()
```

> ⚠️ This does not use clipboard. True clipboard paste is not possible via HID.

---

## `press(*keys: str)`

Presses a key or key combination.

**Arguments**

* One or more key names (modifiers first)

```python
kbd.press("ENTER")
kbd.press("CTRL", "c")
kbd.press("GUI", "r")
kbd.press("SHIFT", "ALT", "TAB")
```

---

## `hold(*keys: str)`

Holds modifier or regular keys (no release).

```python
kbd.hold("CTRL", "ALT")
```

---

## `release()`

Releases all currently held keys.

```python
kbd.release()
```

---

## `pause(seconds: float)`

Pauses script execution.

```python
kbd.pause(1.5)
```

---

## `enter()`

Presses ENTER.

```python
kbd.enter()
```

---

## `tab()`

Presses TAB.

```python
kbd.tab()
```

---

## `space()`

Presses SPACE.

```python
kbd.space()
```

---

## `esc()`

Presses ESC.

```python
kbd.esc()
```

---

## `winRun(command: str)`

Opens Windows Run dialog and executes a command.

**Arguments**

* `command` — command to execute

```python
kbd.winRun("cmd")
kbd.winRun("notepad")
```

---

## `spamText(text: str, n: int = 10)`

Types a string multiple times.

**Arguments**

* `text` — string to type
* `n` — number of repetitions (default: 10)

```python
kbd.spamText("TEST ", 5)
```

---

## `close()`

Closes the HID device and releases resources.

```python
kbd.close()
```

---

# Rubber Ducky Script Support

RPI-HID includes a **DuckyScript interpreter** with near **Rubber Ducky v1 compatibility**.

---

## `DuckyInterpreter(delay: float = 0.02)`

Creates a DuckyScript interpreter.

```python
from rpi_hid import DuckyInterpreter

duck = DuckyInterpreter()
```

---

## `run_file(path: str)`

Runs a `.ducky` script file.

```python
duck.run_file("payload.ducky")
```

---

## `run_script(text: str)`

Runs DuckyScript from a string.

```python
duck.run_script("""
GUI r
STRING notepad
ENTER
""")
```

---

## `close()`

Releases HID device.

```python
duck.close()
```

---

## Supported DuckyScript Commands

| Command                       | Description                    |
| ----------------------------- | ------------------------------ |
| `STRING <text>`               | Types text                     |
| `STRING_DELAY <ms> <text>`    | Types text with per-char delay |
| `DELAY <ms>`                  | Delay in milliseconds          |
| `DEFAULT_DELAY <ms>`          | Delay after each command       |
| `ENTER`                       | Press ENTER                    |
| `TAB`                         | Press TAB                      |
| `SPACE`                       | Press SPACE                    |
| `ESC`                         | Press ESC                      |
| `CTRL`, `ALT`, `SHIFT`, `GUI` | Modifier combinations          |
| `HOLD <keys>`                 | Hold keys                      |
| `RELEASE`                     | Release held keys              |
| `REPEAT <n>`                  | Repeat last action             |
| `REM <comment>`               | Comment                        |
| `PASTE <text>`                | Instant burst typing           |

---

## Example Ducky Script

```text
REM Demo payload
DEFAULT_DELAY 200
GUI r
STRING notepad
ENTER
PASTE Hello from RPI-HID
ENTER
```

---

## Permissions Note

HID device access requires root privileges.

When using a virtual environment:

```bash
sudo venv/bin/python script.py
```

---

## Ethical Use

This project is intended for:

* USB HID experimentation
* Automation on **owned or authorized systems**
* Educational and research purposes

Users are responsible for lawful and ethical use.

---

## License

MIT License

---

## Author

**Abhirup Rudra**

---

## Roadmap

* Mouse HID support
* Full Rubber Ducky v2 compatibility
* Conditional scripting logic
* GPIO-based payload selection
* udev-based non-root execution
