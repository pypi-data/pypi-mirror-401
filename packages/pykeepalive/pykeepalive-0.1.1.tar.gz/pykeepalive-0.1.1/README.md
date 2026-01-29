# pykeepalive

A simple Python tool that keeps your system awake by making tiny periodic mouse movements.

## Description

`pykeepalive` prevents your computer from going to sleep by simulating user activity through small, random mouse movements. It's useful for:
- Preventing screensaver activation
- Avoiding system sleep during long-running tasks
- Keeping remote sessions active
- Testing scenarios that require system activity

## Installation

### Prerequisites
- Python 3.12 or higher

### Install from PyPI
```bash
pip install pykeepalive
```

### Install from source
```bash
git clone <repository-url>
cd pykeepalive
uv sync
```

## Usage

### Basic Usage
Run the tool to keep your system awake indefinitely:
```bash
uv run pykeepalive
```

The tool will start moving your mouse cursor slightly every 20-60 seconds. Press `Ctrl+C` to stop.

### Command Line Options

- `--min-interval INTEGER`: Minimum interval between movements in seconds (default: 20)
- `--max-interval INTEGER`: Maximum interval between movements in seconds (default: 60)
- `--duration INTEGER`: Run for this many seconds, then stop automatically (useful for testing)

### Examples

Run with custom intervals:
```bash
uv run pykeepalive --min-interval 10 --max-interval 30
```

Test for 10 seconds:
```bash
uv run pykeepalive --duration 10
```

## How It Works

The tool uses the `pynput` library to control the mouse cursor. Every random interval (between min and max seconds), it moves the cursor by a small random amount (-2 to +2 pixels in both x and y directions). This tiny movement is usually imperceptible but prevents the system from detecting inactivity.

## Testing

To verify the tool is working:

1. **Visual Test**: Run `uv run pykeepalive --duration 10` and watch your mouse cursor - it should move slightly every few seconds.

2. **Position Check**: Use this Python snippet to monitor mouse position:
   ```python
   from pynput.mouse import Controller
   import time

   mouse = Controller()
   print(f"Before: {mouse.position}")
   time.sleep(5)
   print(f"After: {mouse.position}")
   ```

3. **System Sleep Test**: Set your system to sleep after 1-2 minutes, run `pykeepalive`, and verify the system stays awake.

## Requirements

- `pynput>=1.8.1`: For mouse control
- `typer>=0.9.0`: For command-line interface

## License

MIT License

Copyright (c) 2026 vivek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.