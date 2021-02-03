# 49er

A very minimal Python text editor, using curses, and weighing in at (for now) 49 lines. This is a recreation of the editor I wrote for the (now lost) 2008-era Raspberry Pi prototype, which booted directly to a CPython REPL on a BCM2727 development kit.

It supports:

- Navigation with cursor keys, home, end, page up, and page down
- Backspace, delete
- 3-space tabs
- Preservation of cursor x position while traversing short lines

## Usage

python 49er.py filename

A blank file is created if *filename* does not exist. Control+C exits the editor session and writes back to *filename*.
