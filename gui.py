# -*- coding: utf-8 -*-
"""
File to create windows and widgets

"""
import data
import wx
main_window()
def main_window():
    """
    Function that creates the main window of the Digital Pedalboard program
    """  
    app = wx.App()
    window = wx.Frame(None,title="Digital Pedalboard",name="main_window")
    window.Maximize()
    window.Show()
    return window

def settings_window():
    pass

def filter_checkbox(check_list, name):
    """
    Create the checkbox    
    """
    pass

def filter_list(name):
    """
    Create a checkbox filter container.  
    """
    pass

def filter_window():
    """
    Open a popup to show filter settings
    """
    pass