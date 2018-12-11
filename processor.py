from collector import initalizeCollector
from collector import GetFrame
import collector # for using APP_* strings
import cmd

print("==============================================================")

status, window_info = initalizeCollector()

if status:
    shape = window_info[collector.APP_O]
    cmd.initalizeCmd(shape)
    cmd.Go()
    cmd.StartMouseListener()