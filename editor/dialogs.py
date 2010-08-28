"""
Open/save dialog functions that use the best option for each platform. While useful, this module will probably be discarded in favor of a thumbnail-based loading/saving system.
"""

__all__ = ["open_file", "save_file"]

class WxDialogs(object):
    def __init__(self):
        import wx
        self.app = wx.App(False)

    def open_file(self, type_list=[]):
        import wx
        wildcard = '|'.join(z for y in ((x,'*.'+x) for x in type_list) for z in y)
        dlg = wx.FileDialog(None,style=wx.FD_OPEN,wildcard=wildcard)
        dlg.ShowModal()
        return dlg.GetPath() if dlg.GetFilename() else None

    def save_file(self, default_name=""):
        import wx
        dlg = wx.FileDialog(None,style=wx.FD_SAVE)
        dlg.ShowModal()
        return dlg.GetPath() if dlg.GetFilename() else None

class ZenityDialogs(object):
    def __init__(self):
        import subprocess
        test = subprocess.Popen(["zenity"], stderr=subprocess.PIPE)
        test.wait()

    def open_file(self, type_list=[]):
        import subprocess
        cmd = ["zenity", "--file-selection"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        if p.wait():
            return None
        else:
            return p.stdout.next().strip()

    def save_file(self, default_name=""):
        import subprocess
        cmd = ["zenity", "--file-selection", "--save"]
        if default_name: cmd.append("--filename=" + default_name)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        if p.wait():
            return None
        else:
            return p.stdout.next().strip()

class EasyDialogsDialogs(object):
    def __init__(self):
        import EasyDialogs

    def open_file(self, type_list=[]):
        import EasyDialogs
        return EasyDialogs.AskFileForOpen()

    def save_file(self, default_name=""):
        import EasyDialogs
        return EasyDialogs.AskFileForSave(savedFileName = default_name)

class TkDialogs(object):
    def __init__(self):
        import Tkinter, tkFileDialog
        self.root = Tkinter.Tk()
        self.root.withdraw()

    def open_file(self, type_list=[]):
        import tkFileDialog
        name = tkFileDialog.askopenfilename(parent=self.root, filetypes=[(x,'*.'+x) for x in type_list])
        return name or None

    def save_file(self, default_name=""):
        import tkFileDialog
        name = tkFileDialog.asksaveasfilename(parent=self.root, initialfile=default_name)
        return name or None

class LackOfDialogs(object):
    def open_file(self, type_list=[]):
        return "My Picture.png"
    def save_file(self, default_name=""):
        return default_name or "My Picture.png"

things_to_try = [EasyDialogsDialogs,WxDialogs,ZenityDialogs,TkDialogs,LackOfDialogs]

for thing in things_to_try:
    try:
        handler = thing()
        open_file = handler.open_file
        save_file = handler.save_file
        break
    except:
        continue
else:
    raise ImportError, "Nothing worked!"
