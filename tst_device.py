from PyQt5.QtCore import pyqtSignal, QThread

import subprocess

class Shell(QThread):
    trigger = pyqtSignal(str)
    def __init__(self):
        super(Shell, self).__init__()
        self.cmd = 'adb devices'
        self.ret_code = None
        self.ret_info = None
        self.err_info = None

    def run_background(self):
        self._process = subprocess.Popen(self.cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_status(self):
        retcode = self._process.poll()
        if retcode == None:
            status = "RUNNING"
        else:
            status = "FINISHED"
        return status

    def print_output(self):
        for _ in range(10):
            line = self._process.stdout.readline() # 这儿会阻塞
            if line:
                self.trigger.emit(str(line))
                print("output:", line)
            else: # 只有子进程结束后, 才会有readline返回""的情况
                print("no ouput yet")
                return

    def run(self):
        self.run_background()
        self.print_output()


if __name__ == '__main__':
    keepprinting = Shell() # keepprint will print out one line every 2 seconds
    keepprinting.run_background()
    keepprinting.print_output()