import sys

cmds = {}
args = {}

def ArrayIterator(arr):
    for i in arr:
        yield i

def Cmd(cmd):
    def CmdDecorator(func):
        cmds[cmd] = func
        return func
    return CmdDecorator

def run():
    cmds[next(args)]()

def getArg():
    return next(args)

args = ArrayIterator(sys.argv)
next(args)