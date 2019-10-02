#!/usr/bin/env python3.7

import binascii
import struct
import array
import sys
import subprocess
import cmd

def to_cstr(b):
    return ''.join('\\x' + format(x, '02x') for x in b[0])

def asm(s):
    try:
        subprocess.run("echo \'" + s + "\' | gcc -m32 -o asmrepl.o -c -xassembler -", shell=True, check=True)
        subprocess.run("objcopy -O binary -j .text asmrepl.o asmrepl.raw", shell=True, check=True)
        ret = subprocess.run('od -An -t x1 asmrepl.raw', shell=True, check=True, capture_output=True)
        return bytearray.fromhex(ret.stdout.decode('utf-8').strip()), s
    except Exception as e:
        return bytearray()

def to_cstrs(exp, pretty = True):
    cstrs = list(map(to_cstr, exp))
    
    if pretty:
        out = ""
        for i, s in enumerate(cstrs):
            if i != 0:
                out += "\n"
            out += "\"" + s + "\" \t/* " + exp[i][1] + " */"
        return out
    else:
        return "\"" + ''.join(cstrs) + "\""


class Repl(cmd.Cmd):
    prompt = '> '

    def default(self, line):
        b = asm(line)
        if len(b) != 0:
            print(to_cstrs([b]))
    
    def do_exit(self, line):
        return True
    
    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True

Repl().cmdloop()
