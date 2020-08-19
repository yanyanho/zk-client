import threading

from django.shortcuts import render

# Create your views here.
from commands.event_sync import event_sync


def event_sync_start() -> None :{
    print("********* django start")

}

class TaskThread(threading.Thread):
    def run(self):
        event_sync()

def EventSyncTask():
    taskThread = TaskThread()
    taskThread.start()
    # testThread.join() # 如果加上就会等线程执行完才响应，在我们这个场景下不加

event_sync_start()

# EventSyncTask()