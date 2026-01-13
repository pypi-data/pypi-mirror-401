"""InterestPrint 库
作者:袁窦涵
邮箱:w111251@outlook.com"""
import sys
import ctypes
from ctypes import wintypes
from typing import Any
__version__ = "0.4.2"
print("""Thanks for using InterestPrint!
this project in pypi: https://pypi.org/project/InterestPrint/
now version: {}""".format(__version__), flush=True)
__import__("time").sleep(0.3)
__import__("os").system("cls") if sys.platform == "win32" else __import__("os").system("clear")
class COORD(ctypes.Structure):
    """手动定义控制台坐标结构体（替代 wintypes.COORD）"""
    _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

class SMALL_RECT(ctypes.Structure):
    """手动定义控制台矩形区域结构体（替代 wintypes.SMALL_RECT）"""
    _fields_ = [("Left", wintypes.SHORT), ("Top", wintypes.SHORT),
                ("Right", wintypes.SHORT), ("Bottom", wintypes.SHORT)]
_USE_ANSI = False
_CONSOLE_HANDLE = None
_DEFAULT_CONSOLE_ATTR = None
WIN_FG_COLORS = {
    'black': 0x00,    
    'red': 0x04,      
    'green': 0x02,    
    'yellow': 0x06,   
    'blue': 0x01,     
    'purple': 0x05,   
    'cyan': 0x03,     
    'white': 0x07,    
}
WIN_BG_COLORS = {
    'black': 0x00,    
    'red': 0x40,      
    'green': 0x20,    
    'yellow': 0x60,   
    'blue': 0x10,     
    'purple': 0x50,   
    'cyan': 0x30,     
    'white': 0x70,    
}
ANSI_FG_COLORS = {
    'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
    'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
}
ANSI_BG_COLORS = {
    'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
    'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
}
def _init():
    """
    库初始化方法：自动检测 Windows 版本，选择兼容方案
    - Win10+：启用 ANSI 转义码
    - WinXP-Win8.1：使用 kernel32.dll API 修改控制台样式
    """
    global _USE_ANSI, _CONSOLE_HANDLE, _DEFAULT_CONSOLE_ATTR
    if sys.platform != "win32":
        _USE_ANSI = True
        return
    win_ver = sys.getwindowsversion()
    nt_major, nt_minor, nt_build = win_ver.major, win_ver.minor, win_ver.build    
    if (nt_major, nt_minor) == (10, 0) and nt_build >= 15063:
        _USE_ANSI = True
        try:
            kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
            handle = kernel32.GetStdHandle(-11)  
            mode = wintypes.DWORD()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            mode.value |= 0x0004  
            kernel32.SetConsoleMode(handle, mode)
        except:
            _USE_ANSI = False
    else:
        _USE_ANSI = False    
    if not _USE_ANSI:
        try:
            kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
            
            _CONSOLE_HANDLE = kernel32.GetStdHandle(-11)
            if _CONSOLE_HANDLE == wintypes.HANDLE(-1):
                raise OSError("获取控制台句柄失败")            
            class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
                _fields_ = [
                    ("dwSize", COORD),
                    ("dwCursorPosition", COORD),
                    ("wAttributes", wintypes.WORD),
                    ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", wintypes.COORD)
                ]            
            csbi = CONSOLE_SCREEN_BUFFER_INFO()
            kernel32.GetConsoleScreenBufferInfo(_CONSOLE_HANDLE, ctypes.byref(csbi))
            _DEFAULT_CONSOLE_ATTR = csbi.wAttributes
        except:
            _CONSOLE_HANDLE = None
            _DEFAULT_CONSOLE_ATTR = None
def _set_console_color(fg_color: str, bg_color: str = None, bold: bool = False):
    """
    设置控制台文本颜色
    :param fg_color: 前景色名称
    :param bg_color: 背景色名称（可选）
    :param bold: 是否加粗（高亮度）
    """
    if not _CONSOLE_HANDLE or not _DEFAULT_CONSOLE_ATTR:
        return
    try:
        kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)        
        fg = WIN_FG_COLORS.get(fg_color.lower(), WIN_FG_COLORS['white'])
        if bold:
            fg |= 0x08  
        bg = WIN_BG_COLORS.get(bg_color.lower(), WIN_BG_COLORS['black']) if bg_color else 0x00
        color_attr = fg | bg
        kernel32.SetConsoleTextAttribute(_CONSOLE_HANDLE, color_attr)
    except:
        pass
def _restore_console_default():
    """恢复控制台默认样式"""
    if not _CONSOLE_HANDLE or not _DEFAULT_CONSOLE_ATTR:
        return
    try:
        kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
        kernel32.SetConsoleTextAttribute(_CONSOLE_HANDLE, _DEFAULT_CONSOLE_ATTR)
    except:
        pass
def ColorfulPrint(*objects: Any, color: str = 'white', bold: bool = False, end: str = '\n', sep: str = ' ') -> None:
    """
    带颜色打印
    :param objects: 要打印的内容（可变参数）
    :param color: 字体颜色,可选:black/red/green/yellow/blue/purple/cyan/white
    :param bold: 是否加粗,默认False
    :param end: 结尾字符，默认换行
    :param sep: 多个参数的分隔符，默认空格
    """
    if color.lower() not in WIN_FG_COLORS:
        raise ValueError(f"颜色必须是以下之一：{list(WIN_FG_COLORS.keys())}")
    content = sep.join(map(str, objects))
    if _USE_ANSI:
        fg_code = ANSI_FG_COLORS.get(color.lower(), ANSI_FG_COLORS['white'])
        style = 1 if bold else 0
        ansi_prefix = f'\033[{style};{fg_code}m'
        ansi_suffix = '\033[0m'
        print(f"{ansi_prefix}{content}{ansi_suffix}", end=end)
        return
    if not _USE_ANSI and _CONSOLE_HANDLE:
        
        _set_console_color(fg_color=color, bold=bold)
        
        print(content, end=end, sep=sep)
        
        _restore_console_default()
        return
    print(content, end=end, sep=sep)
def FrontBackPrint(*objects: Any, front: str = '^', back: str = '$', end: str = '\n', sep: str = ' '):
    """
    可设置前后缀的打印
    :param objects: 要打印的内容（可变参数）
    :param front: 前缀（默认^）
    :param back: 后缀（\EQUALTOFRONT的意思是前后缀相同）
    :param end: 结尾字符，默认换行
    :param sep: 多个参数的分隔符，默认空格
    """
    if back == r'\EQUALTOFRONT':
        back = front
    objects_str = sep.join(map(str, objects)) if objects else ''
    print(f"{front}{objects_str}{back}", end=end, sep=sep)
def MeowPrint(*objects: Any, meow_count: int = 1, end: str = '\n', sep: str = ' ', front: bool = True, back: bool = True) -> None:
    """
    喵喵喵打印
    :param objects: 要打印的内容（可变参数）
    :param meow_count: 猫咪表情数量,默认1
    :param end: 结尾字符,默认换行
    :param sep: 多个参数的分隔符,默认空格
    :param front: 是否在前面打印表情,默认True
    :param back: 是否打印后面打印表情,默认True
    """
    front_meow = '🐱' * meow_count if front else ''
    FrontBackPrint(*objects, front=front_meow, back='\EQUALTOFRONT' if back else '', end=end, sep=sep)
def BgColorfulPrint(*objects: Any, bg_color: str = 'black', end: str = '\n', sep: str = ' ', bold: bool = False) -> None:
    """
    带背景色的花式打印
    :param objects: 要打印的内容（可变参数）
    :param bg_color: 背景颜色,可选:black/red/green/yellow/blue/purple/cyan/white
    :param bold: 是否加粗,默认False
    :param end: 结尾字符，默认换行
    :param sep: 多个参数的分隔符，默认空格
    """
    if bg_color.lower() not in WIN_BG_COLORS:
        raise ValueError(f"背景颜色必须是以下之一：{list(WIN_BG_COLORS.keys())}")
    content = sep.join(map(str, objects))
    if _USE_ANSI:
        fg_code = ANSI_FG_COLORS['white']
        bg_code = ANSI_BG_COLORS.get(bg_color.lower(), ANSI_BG_COLORS['black'])
        style = 1 if bold else 0
        ansi_prefix = f'\033[{style};{fg_code};{bg_code}m'
        ansi_suffix = '\033[0m'
        print(f"{ansi_prefix}{content}{ansi_suffix}", end=end)
        return
    if not _USE_ANSI and _CONSOLE_HANDLE:
        _set_console_color(fg_color='white', bg_color=bg_color, bold=bold)
        print(content, end=end, sep=sep)
        _restore_console_default()
        return
    print(content, end=end, sep=sep)
def FgAndBgColorfulPrint(*objects: Any, fg_color: str = 'white', bg_color: str = 'black',
                        end: str = '\n', sep: str = ' ') -> None:
    """
    同时设置前景色和背景色
    :param objects: 要打印的内容（可变参数）
    :param fg_color: 前景色（字体色）
    :param bg_color: 背景色
    :param end: 结尾字符，默认换行
    :param sep: 多个参数的分隔符，默认空格
    """
    if fg_color.lower() not in WIN_FG_COLORS:
        raise ValueError(f"前景色必须是以下之一：{list(WIN_FG_COLORS.keys())}")
    if bg_color.lower() not in WIN_BG_COLORS:
        raise ValueError(f"背景色必须是以下之一：{list(WIN_BG_COLORS.keys())}")
    content = sep.join(map(str, objects))
    if _USE_ANSI:
        fg_code = ANSI_FG_COLORS.get(fg_color.lower(), ANSI_FG_COLORS['white'])
        bg_code = ANSI_BG_COLORS.get(bg_color.lower(), ANSI_BG_COLORS['black'])
        ansi_prefix = f'\033[{fg_code};{bg_code}m'
        ansi_suffix = '\033[0m'
        print(f"{ansi_prefix}{content}{ansi_suffix}", end=end)
        return
    if not _USE_ANSI and _CONSOLE_HANDLE:
        _set_console_color(fg_color=fg_color, bg_color=bg_color)
        print(content, end=end, sep=sep)
        _restore_console_default()
        return
    print(content, end=end, sep=sep)
def PrintThenClear(*objects: Any, show_time=1, color: str = 'white', bold: bool = False, end: str = '\n', sep: str = ' ') -> None:
    """
    打印后清屏
    :param objects: 要打印的内容（可变参数）
    :param color: 字体颜色,可选:black/red/green/yellow/blue/purple/cyan/white
    :param bold: 是否加粗,默认False
    :param end: 结尾字符，默认换行
    :param sep: 多个参数的分隔符，默认空格
    """
    ColorfulPrint(*objects, color=color, bold=bold, end=end, sep=sep)
    __import__("time").sleep(show_time)
    if sys.platform == "win32":
        __import__("os").system("cls")
    else:
        __import__("os").system("clear")

FgColorfulPrint = ColorfulPrint


__all__ = ['ColorfulPrint', 
           'MeowPrint', 
           'BgColorfulPrint', 
           'FgAndBgColorfulPrint', 
           'FgColorfulPrint', 
           'FrontBackPrint', 
           'PrintThenClear']
_init()
if __name__ == '__main__':
    ColorfulPrint("这是红色加粗", color='red', bold=True)
    ColorfulPrint("这是绿色常规", color='green')
    ColorfulPrint("多参数", "测试", color='blue', sep='|')
    ColorfulPrint("黄色结尾无换行", color='yellow', end='')
    print(" → 看，没换行～")
    MeowPrint("喵喵喵", meow_count=2, front=True, back=False)
    MeowPrint("喵喵喵", meow_count=3, front=False, back=True)
    MeowPrint("喵喵喵","wfe", meow_count=4, end="mmmmm\n",sep=" ")
    BgColorfulPrint("背景色测试（红色背景）", bg_color='red')
    FgAndBgColorfulPrint("前景红+背景绿测试", fg_color='red', bg_color='green')
    FgColorfulPrint("别名功能测试（白色常规）")
    FrontBackPrint("前后缀测试", front='*', back='\EQUALTOFRONT')
    PrintThenClear("打印后清屏测试", show_time=2, color='green', bold=True)