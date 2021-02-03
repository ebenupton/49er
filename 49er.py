#!/usr/bin/env python
import curses, sys

def main(stdscr):
   try:
      with open(sys.argv[1], "r") as file: 
         lines = [line.strip("\r\n")+"\n" for line in file.readlines()]
   except:
      lines = ["\n"]

   x, y, h, v = 0, 0, 0, 0

   clampx = lambda : min(x, len(lines[y])-1)

   FUN = {curses.KEY_HOME:  (lambda : x, lambda x : (lines, 0, y)),
          curses.KEY_END:   (lambda : x, lambda x : (lines, len(lines[y])-1, y)),
          curses.KEY_LEFT:  (clampx,     lambda x : (lines, ) + ((x-1, y) if x > 0 else (len(lines[y-1])-1, y-1) if y > 0 else (x, y))),
          curses.KEY_RIGHT: (clampx,     lambda x : (lines, ) + ((x+1, y) if x < len(lines[y])-1 else (0, y+1) if y < len(lines)-1 else (x, y))),
          curses.KEY_UP:    (lambda : x, lambda x : (lines, x, max(y-1, 0))),
          curses.KEY_DOWN:  (lambda : x, lambda x : (lines, x, min(y+1, len(lines)-1))),
          curses.KEY_PPAGE: (lambda : x, lambda x : (lines, x, max(y-rows, 0))),
          curses.KEY_NPAGE: (lambda : x, lambda x : (lines, x, min(y+rows, len(lines)-1))),
          10:               (clampx,     lambda x : (lines[:y]+[lines[y][:x]+"\n", lines[y][x:]]+lines[y+1:], 0, y+1)),
          127:              (clampx,     lambda x : (lines[:y]+[lines[y][:x-1]+lines[y][x:]]+lines[y+1:], x-1, y) if x > 0 else (lines[:y-1]+[lines[y-1][:-1]+lines[y]]+lines[y+1:], len(lines[y-1])-1, y-1) if y > 0 else (lines, x, y)),
          curses.KEY_DC:    (clampx,     lambda x : (lines[:y]+[lines[y][:x]+lines[y][x+1:]]+lines[y+1:], x, y) if x < len(lines[y])-1 else (lines[:y]+[lines[y][:-1]+lines[y+1]]+lines[y+2:], x, y) if y < len(lines)-1 else (lines, x, y))}

   try:
      while True:
         stdscr.clear()
         rows, cols = stdscr.getmaxyx()

         h, v = max(min(h, clampx()), clampx()-cols+1), max(min(v, y), y-rows+1)

         for i in range(min(rows, len(lines)-v)):
            stdscr.addstr(i, 0, lines[v+i][h:h+cols][:-1])
         stdscr.move(y-v, clampx()-h)
         stdscr.refresh()

         key = stdscr.getch()
         
         if FUN.has_key(key):
            lines, x, y = FUN[key][1](FUN[key][0]())
         elif key == 9 or key >= 32 and key < 127:
            lines[y], x = lines[y][:clampx()]+(" "*(3-x%3) if key == 9 else chr(key))+lines[y][clampx():], clampx()+(3-x%3 if key == 9 else 1)
   except KeyboardInterrupt:
      with open(sys.argv[1], "w") as file: 
         file.writelines(lines)

curses.wrapper(main)
