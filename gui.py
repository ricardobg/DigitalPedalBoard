# -*- coding: utf-8 -*-
"""
File to create windows and widgets

"""
import data
import wx

def sair(e):
    window.Close()
    
class main_window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()
        
    def InitUI(self):    

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()
def create_main_window():
    """
    Function that creates the main window of the Digital Pedalboard program
    """  
    app = wx.App()
    window = wx.Frame(None,title="Digital Pedalboard",name="main_window")
    menubar = wx.MenuBar()
    menu = wx.Menu()
    item1 = menu.Append(wx.ID_NEW, "Novo Preset", "Criar novo preset de filtros")
    item2 = menu.Append(wx.ID_OPEN, "Carregar Preset", "Carregar preset de filtros")
    item3 = menu.Append(wx.ID_EXIT, "Sair", "Sair do aplicativo")
    menubar.Append(menu,"Executar")
    window.SetMenuBar(menubar)
    window.Bind(wx.EVT_MENU, sair, item3)
    window.Maximize()   
    window.Show()
    app.MainLoop()
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

main_window()