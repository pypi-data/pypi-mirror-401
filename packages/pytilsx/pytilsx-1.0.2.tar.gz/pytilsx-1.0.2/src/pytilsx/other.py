import time as _tm
import sys as _ss
import subprocess as _sb

class Timer:
    """
        Create timer

        Example:
            import time

            timer = Timer()
            timer.start()
            time.sleep(5.11)
            timer.end()

            print(timer.get())"""
    def __init__(self, decimals:int=2):
        """
        Create timer

        Example:
            import time

            timer = Timer()
            timer.start()
            time.sleep(5.11)
            timer.end()

            print(timer.get())"""
        self.starttime = 0.0
        self.endtime = 0.0
        self.decimals = decimals
    
    def start(self):
        """Start timer"""
        self.starttime = _tm.time()
    
    def end(self):
        """Stop timer"""
        self.endtime = _tm.time() - self.starttime
    
    def get(self):
        """Get the time timer value"""
        return round(self.endtime, self.decimals)

    def reset(self):
        """Reset timer"""
        self.endtime = 0.0
        self.starttime = 0.0

class logging:
    """Record all actions."""
    def __init__(self, *, time:bool=True, lighting:bool=False, timestyle:str="%H:%M:%S"):
        """Record all actions."""
        self.log = []
        self.time = time
        self.lighting = lighting
        self.timestyle = timestyle

    def AddAction(self, text:str, state:int = 1):
        """States:
            1 - Info;
            2 - Waring;
            3 - Error;
            other - Unknow;"""
        if self.time:current_time = f"({_tm.strftime(self.timestyle, _tm.localtime())})"
        else:current_time = ""
        if state == 1:
            status = "INFO"
            if self.lighting:color = "\033[34m"
            else:color = ""
        elif state == 2:
            status = "WARING"
            if self.lighting:color = "\033[33m"
            else:color = ""
        elif state == 3:
            status = "ERROR"
            if self.lighting:color = "\033[31m"
            else:color = ""
        else:
            status = "UNKNOWN"
            if self.lighting:color = "\033[90m"
            else:color = ""
        if self.lighting:reset = "\033[0m"
        else:reset = ""

        self.log.append(f"[{color}{status}{reset}] {current_time} {text}")

    def GetLog(self):
        """You get all the actions you"ve done."""
        result = ""
        for line in self.log:
            result += f"{line}\n"
        return result

    def SaveLog(self, path:str, *, write_type:str="w+", encoding:str="utf-8"):
        """Saving the entire log.
        Write types:
            w;
            w+;"""
        with open(path, write_type, encoding=encoding) as f:
            f.write(self.GetLog())
    
    def SaveToClipboard(self):
        platform: str = _ss.platform

        if platform == "win32":
            _sb.run("clip", text=True, input=self.GetLog())
        elif platform == "darwin":
            _sb.run("pbcopy", text=True, input=self.GetLog())
        elif platform.startswith("linux"):
            _sb.run("xclip -selection clipboard", text=True, input=self.GetLog())