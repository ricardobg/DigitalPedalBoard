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
        super(main_window, self).__init__(*args, **kwargs) 
        self.InitUI()
        
    def InitUI(self):    
        #Cria o menu        
        menubar = wx.MenuBar()
        menu = wx.Menu()
        item1 = menu.Append(wx.ID_NEW, "Novo Preset", "Criar novo preset de filtros")
        item2 = menu.Append(wx.ID_OPEN, "Carregar Preset", "Carregar preset de filtros")
        item3 = menu.Append(wx.ID_EXIT, "Sair", "Sair do aplicativo")
        menubar.Append(menu, 'Arquivo')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnNewPreset, item1)
        self.Bind(wx.EVT_MENU, self.OnLoadPreset, item2)
        self.Bind(wx.EVT_MENU, self.OnQuit, item3)
        #Cria os panels que contem os filtros
        filter_list(self,"teste")



        self.Show(True)    
    
    def OnQuit(self, e):
        self.Close()
        
    def OnNewPreset(self, e):
        self.Close()
    
    def OnLoadPreset(self, e):
        self.Close()
def create_main_window():
    """
    Function that creates the main window of the Digital Pedalboard program
    """  
    app = wx.App()
    window = main_window(None,title="Digital Pedalboard",name="main_window")
    app.MainLoop()
    return window


    
def settings_window():
    pass

def filter_checkbox(check_list, name):
    """
    Create the checkbox    
    """
    pass

def filter_list(window, name):
    """
    Create a checkbox filter container.     
    """
    panel = wx.Panel(window, -1)
    wx.TextCtrl(panel,pos=(3,3), size=(250,150))

def filter_window():
    """
    Open a popup to show filter settings
    """
    pass

window = create_main_window()