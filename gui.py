# -*- coding: utf-8 -*-
# This file is part of DigitalPedalBoard python program.
# Copyright (C) 2013 Copyright (C) 2013 Daniel Ken Fujimori Killner,
# Gabriel Moura Vieira Martinez, Rafael Alves de Araujo Sena,
# Ricardo Boccoli Gallego, Danilo de Jesus da Silva Bellini.
#
# DigitalPedalBoard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
File to create windows and widgets

"""
import data
import filters
import player
import serialcom as sc
from lib import FloatSlider, DataGen, MyThread
from audiolazy import ControlStream


import wx
import copy
import sys     
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab


sys.tracebacklimit = 0

   
class main_window(wx.Frame):
    """
    Main Window
    Modes: (Regular Mode, Preset Editing Mode, Preset Mode)
    """
    def __init__(self, *args, **kwargs):
        super(main_window, self).__init__(*args, **kwargs) 
        self.InitUI()
        
    def InitUI(self):    
        """
        Initialize the main screen on Regular Mode.
        """

        # Creates the menu with two items: File and Preset
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.menubar = wx.MenuBar()
        self.menu = wx.Menu()
        item_novo = self.menu.Append(wx.ID_NEW, "New Preset", "Create new preset")
        item_carregar = self.menu.Append(wx.ID_OPEN, "Load Preset", "Load preset")
        item_salvar = self.menu.Append(wx.ID_SAVE, "Save Preset", "Save preset")
        item_sair = self.menu.Append(wx.ID_EXIT, "Quit", "Quit")
        self.menubar.Append(self.menu , 'File')
        self.menu_preset = wx.Menu()
        item_voltar = self.menu_preset.Append(wx.ID_BACKWARD, "Back", "Back")   
        item_editar = self.menu_preset.Append(wx.ID_EDIT, "Edit Preset", "Edit Preset")
        item_start = self.menu_preset.Append(wx.ID_SETUP, "Play Preset", "Play Preset")
        self.menubar.Append(self.menu_preset , 'Preset')
        self.SetMenuBar(self.menubar) 
        self.menubar.EnableTop(1, False)
        
        self.Bind(wx.EVT_MENU, self.OnNewPreset, item_novo)
        self.Bind(wx.EVT_MENU, self.OnLoadPreset, item_carregar)
        self.Bind(wx.EVT_MENU, self.OnQuit, item_sair)
        self.Bind(wx.EVT_MENU, self.OnEditPreset, item_editar)
        self.Bind(wx.EVT_MENU, self.OnSavePreset, item_salvar)
        self.Bind(wx.EVT_MENU, self.OnStartPreset, item_start)
        self.Bind(wx.EVT_MENU, self.OnVoltar, item_voltar)
        
        
        # --------------------- #
        #   STATUS VARIABLES    #
        # --------------------  #
        
        # Player status: 0-Stopped, 1-Playing, 2-Paused
        self.status = 0      
        # Preset use status: 0-not using, 1-Playing preset, 2-Editing preset
        self.preset_mode = 0
      
      
        
        # Graph refresh time in ms
        self.graph_refresh_time = 100
        self.pausa_grafico = False
        
        # Creates the panel and the main sizer
        self.panel_principal = wx.ScrolledWindow(self,-1)
        self.panel_principal.SetScrollbars(1,1,1,1) 
        self.panel_principal.SetBackgroundColour("#444444")
        self.sizer_principal = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_principal.SetSizer(self.sizer_principal)
        
        
        # Left Panel/Sizer (filters/playing preset)        
        self.panel_esquerda = wx.Panel(self.panel_principal)
        self.panel_esquerda.SetBackgroundColour('#444444')
        self.sizer_esquerda = wx.BoxSizer(wx.VERTICAL)
        self.panel_esquerda.SetSizer(self.sizer_esquerda)
        self.sizer_principal.Add(self.panel_esquerda, 1, wx.EXPAND | wx.ALL, 25)  
        
        
        # ------------------ #
        #     RIGHT PANEL    #
        # -----------------  #
        
        # Right Panel/Sizer (graph/buttons/preset editing)
        self.panel_direita = wx.Panel(self.panel_principal,size=(320,0))    
        self.panel_direita.SetBackgroundColour('#333333')
        self.sizer_direita = wx.BoxSizer(wx.VERTICAL)
        self.panel_direita.SetSizer(self.sizer_direita)
        self.sizer_principal.Add(self.panel_direita, 0, wx.EXPAND | wx.ALL, 0)  

        # Creates the buttons play/pause/stop/next/previous
        self.toolbar =  wx.ToolBar(self.panel_direita, style=wx.NO_BORDER) 
        self.toolbar.SetMinSize((320,65))
        self.sizer_direita.Add(self.toolbar, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.toolbar.AddSeparator()        
        self.toolbar.AddSeparator() 
        self.toolbar.AddSeparator()        
        self.toolbar.AddSeparator()        
        self.toolbar.AddSeparator() 
        self.toolbar.AddSeparator() 
        previous = self.toolbar.AddLabelTool(wx.ID_PREVIEW_PREVIOUS,'Previous',
                                            wx.Bitmap('images/previous.png'))
        stop = self.toolbar.AddLabelTool(wx.ID_STOP,'Stop',
                                            wx.Bitmap('images/stop.png'))
        play = self.toolbar.AddLabelTool(wx.ID_UP,'Play/Pause',
                                            wx.Bitmap('images/play.png'))
        nextt = self.toolbar.AddLabelTool(wx.ID_PREVIEW_NEXT,'Next',
                                            wx.Bitmap('images/next.png'))     
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnPlayPause, play)
        self.Bind(wx.EVT_TOOL, self.OnStop, stop)
        self.Bind(wx.EVT_TOOL, self.OnPrevious, previous)
        self.Bind(wx.EVT_TOOL, self.OnNext, nextt)
        
        
        line = wx.StaticLine(self.panel_direita, size=(320,2), style=wx.LI_HORIZONTAL)
        self.sizer_direita.Add(line,0,border=0)
        
        self.desenha_graficos()
        
       
        
        
        # Filter's variables
        
        # A tuple composed of 3 lists: (checkbuttons, edit buttons, filters)
        self.filters = ([],[],[])
        # Applied filters (Regular Mode)
        self.filtros_aplicados = []
        # Instance of the Player class (player.py)
        self.player = None
        # Serial reading variable
        self.pedal = None
        # Preset = list of list of filters
        self.preset = []
        # List (ListBox) with the edited preset
        self.list_edit_filters = None
        # Position in the preset
        self.posicao_preset = 0
        self.filter_default_list(self.panel_esquerda, self.sizer_esquerda)
        self.modo_tocando()
        
        self.Show(True)    
        self.Maximize()
        
    """
    Functions containing all the gui modes: Regular Mode, Preset Editing Mode and Preset Mode
    """
    
    def modo_tocando(self):
        """
        Set the window to the Regular Mode
        """
        self.posicao_preset  = 0
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
        if self.list_edit_filters is not None:
             self.list_edit_filters.Destroy()
             self.list_edit_filters = None
        for i in range(len(self.filters[0])): 
            self.filters[0][i].SetValue(False)
            self.filters[1][i].Enable(True)  
        self.filtros_aplicados = []
        self.status = 0
        self.preset_mode = 0
        self.preset = []
        self.menu.Enable(wx.ID_NEW, 1)
        self.menu.Enable(wx.ID_OPEN, 1)
        self.menu.Enable(wx.ID_SAVE, 0)
        self.menubar.EnableTop(1, False)
        self.botoes_pause()
        if self.pedal is None:
             self.pedal = sc.SerialData(func_proximo=lambda: self.OnNext(None),
                                   func_anterior=lambda: self.OnPrevious(None))
             self.pedal.start()
        filters.pedal = self.pedal.pedal


    def modo_edita_preset(self):
        """
        Set the window to the Preset Editing Mode
        """
        self.posicao_preset = 0
        self.status = 0
        if self.player is not None and not self.player.player.finished:
            self.data_input = []
            self.data_output = []
            self.on_redraw_graph(None)
            self.player.pausar()
        if self.list_edit_filters is not None:
             self.list_edit_filters.Destroy()
             self.list_edit_filters = None
        if len(self.filters[0]) == 0:
            self.sizer_esquerda.Remove(self.panel_preset)
            self.panel_preset.Destroy()            
            self.filter_default_list(self.panel_esquerda, self.sizer_esquerda)
            
        self.filtros_aplicados = []
        
        self.preset_mode = 2
        self.menu.Enable(wx.ID_NEW, 1)
        self.menu.Enable(wx.ID_OPEN, 1)
        self.menubar.EnableTop(1, True)
        self.menu.Enable(wx.ID_SAVE, True)
        self.menu_preset.Enable(wx.ID_SETUP, True)
        self.menu_preset.Enable(wx.ID_EDIT, False)
        self.botoes_pause()
        self.data_input = []
        self.data_output = []

    def modo_tocando_preset(self):
        """
        Set the window to the Preset Mode
        """
        self.posicao_preset = 0
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
        if self.list_edit_filters is not None:
            self.list_edit_filters.Destroy()
            self.list_edit_filters = None
        
        self.filtros_aplicados = []
        self.status = 0
        self.preset_mode = 1
        self.menu.Enable(wx.ID_NEW, 1)
        self.menu.Enable(wx.ID_OPEN, 1)
        self.menubar.EnableTop(1, True)
        self.menu.Enable(wx.ID_SAVE, False)
        self.menu_preset.Enable(wx.ID_SETUP, False)
        self.menu_preset.Enable(wx.ID_EDIT, True)
        self.botoes_pause()
        
     
   
   
    """
    Functions to handle the events of mode change
    """
    def OnNewPreset(self, e):
         """
         Creates a new preset
         """
         self.pausa_grafico = True
         if self.preset_mode == 1 and self.status == 1:
            filters.pedal = ControlStream(0.1)
            self.pedal.kill()
         self.modo_edita_preset()         
         self.preset = [[]]
         self.filter_list_box(self.panel_direita, self.sizer_direita, self.preset)
         self.list_edit_filters.SetSelection(0)
         self.mostra_lista_filtro([])

         
         try:
            self.timer_graph.stop()
            self.panel_graficos.Destroy()
            self.panel_graficos = None
         except:
            pass
         self.panel_direita.Fit()
         self.panel_direita.Layout()
         self.Layout()
         self.panel_direita.Update()
         self.panel_direita.Update()
         self.sizer_direita.Layout()
          
    def OnSavePreset(self, e):
        """
        Saves the opened preset into a file
        """
        openFileDialog = wx.FileDialog(self, "Type the file's name to save your preset", "", "",
                                       "Preset's File (*.preset)|*.preset", wx.FD_SAVE)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        data.save_preset(openFileDialog.GetPath(), self.preset)
            
    def OnLoadPreset(self, e):
        """
        Loads a preset to edit
        """      
        openFileDialog = wx.FileDialog(self, "Type the file's name to load your preset", "", "",
            "Preset's File (*.preset)|*.preset", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        self.preset = data.load_preset(openFileDialog.GetPath())
        if self.preset_mode == 1 and self.status == 1:
            filters.pedal = ControlStream(0.1)
            self.pedal.kill()
        self.OnEditPreset(None)
       
    def OnStartPreset(self ,e):
        """
        Starts playing a preset
        """
        self.posicao_preset  = 0
        self.filters = ([],[],[])
        self.filtros_aplicados = []        
        self.sizer_esquerda.Remove(self.panel_filtros)
        self.panel_filtros.Destroy()
        self.panel_filtros = None
        self.modo_tocando_preset()
        self.panel_preset = wx.Panel(self.panel_esquerda)
        self.sizer_esquerda.Add(self.panel_preset, 1, wx.EXPAND)      
        self.lista_preset = wx.ListCtrl(self.panel_preset,style=wx.LC_REPORT)
        
        temp_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_preset.SetSizer(temp_sizer)
        self.panel_preset.SetBackgroundColour("#880000")
        self.lista_preset.InsertColumn(0, "Filtros")
        
        temp_sizer.Add(self.lista_preset,1,wx.EXPAND)
        self.panel_esquerda.Fit()
        self.sizer_principal.Layout()
        for item in self.preset[0]:
           self.lista_preset.InsertStringItem(sys.maxint, item.name)

        self.lista_preset.SetColumnWidth(0, self.lista_preset.GetSize()[0]-5)
        if self.pedal is None:
            self.pedal = sc.SerialData(func_proximo=lambda: self.OnNext(None),
                                   func_anterior=lambda: self.OnPrevious(None))
            self.pedal.start()
        filters.pedal = self.pedal.pedal
        
        self.desenha_graficos()
        self.panel_direita.Update()
        self.panel_direita.Fit()
        self.panel_direita.Layout()
        self.panel_graficos.Fit()
        self.panel_graficos.Layout()
        self.panel_graficos.Update()
        self.sizer_graficos.Layout()
        self.Layout()
        self.panel_direita.Update()
        self.sizer_direita.Layout()
        self.sizer_principal.Layout()
        
    def OnEditPreset(self, e):
        """
        Edits a playing preset
        """
        self.pausa_grafico = True
        if self.preset_mode == 1 and self.status == 1:
            filters.pedal = ControlStream(0.1)
            self.pedal.kill()
        self.posicao_preset = 0
        self.modo_edita_preset()        
        self.filter_list_box(self.panel_direita, self.sizer_direita, self.preset)
        self.list_edit_filters.SetSelection(0)
        self.mostra_lista_filtro(self.preset[0])
        
        try:
            self.timer_graph.stop()
            self.panel_graficos.Destroy()
            self.panel_graficos = None
        except:
            pass
        self.panel_direita.Fit()
        self.panel_direita.Layout()
        self.Layout()
        self.panel_direita.Update()
        self.sizer_direita.Layout()
    def OnVoltar(self, e):
        """
        Goes to Regular Mode (quiting either Preset Editing Mode or Preset Mode)
        """
        self.posicao_preset  = 0
        if self.preset_mode == 1: # Regular Mode
            if self.status == 1:
                filters.pedal = ControlStream(0.1)
                self.pedal.kill()
            self.sizer_esquerda.Remove(self.panel_preset)
            self.panel_preset.Destroy()
            self.filter_default_list(self.panel_esquerda,self.sizer_esquerda)
            self.panel_esquerda.Fit()
            self.sizer_principal.Layout()
            self.panel_direita.Fit()
            self.panel_direita.Layout()
            self.Layout()
            self.panel_direita.Update()
            self.panel_direita.Update()
            self.sizer_direita.Layout()
           
            self.modo_tocando()
        if self.preset_mode == 2: # Preset Editing Mode
            self.modo_tocando()
            self.desenha_graficos()
            self.panel_direita.Update()
            self.panel_direita.Fit()
            self.panel_direita.Layout()
            self.panel_graficos.Fit()
            self.panel_graficos.Layout()
            self.panel_graficos.Update()
            self.sizer_graficos.Layout()
            self.Layout()
            self.panel_direita.Update()
            self.sizer_direita.Layout()
            self.sizer_principal.Layout()
    
    """
    Functions to set the buttons (play/pause)
    And to manage its events (play, pause, stop, next, previous)
    """
    
    def botoes_pause(self):
        """
        Set the buttons (Play/Pause/Stop/Next/Previous)
        to the paused state (it depends on the preset_mode variable)
        """        
        if self.preset_mode == 0:
            self.toolbar.EnableTool(wx.ID_UP,True)
            self.toolbar.EnableTool(wx.ID_STOP,True)  
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS,False)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT,False)
       
        if self.preset_mode == 1:
            self.toolbar.EnableTool(wx.ID_UP,True)
            self.toolbar.EnableTool(wx.ID_STOP,True)  
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS,True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT,True)   
        if self.preset_mode == 2:
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
            self.toolbar.EnableTool(wx.ID_UP, True)
            self.toolbar.EnableTool(wx.ID_STOP,False)  
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
    
    def botoes_play(self):
        """
        Set the buttons(Play/Pause/Stop/Next/Previous) to the playing state
        """  
        if self.preset_mode == 0:
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, False)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, False)
        if self.preset_mode == 1:
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.EnableTool(wx.ID_STOP, True)        
        self.toolbar.EnableTool(wx.ID_UP,True)  
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/pause.png'))
    
    
    def OnPlayPause (self, e):
        """
        Event to play or pause
        """
        if self.preset_mode == 0: # Playing WITHOUT preset
            if self.status == 0:
                # Start playing          
                self.player = player.Player(self.filtros_aplicados)
                self.botoes_play()
                self.status = 1
                self.timer_graph.start()
            elif self.status == 1:
                # Pause
                self.timer_graph.stop()
                self.player.pausar()
                self.botoes_pause()
                self.status = 2
            else:
                # Resume
                self.player.tocar(self.filtros_aplicados)
                self.botoes_play()
                self.status = 1
                self.timer_graph.start()
        if self.preset_mode == 1: # Playing WITH preset
            if self.status == 0:
                # Start playing 
                self.player = player.Player(self.preset[self.posicao_preset])
                self.botoes_play()
                self.status = 1
                self.timer_graph.start()
            elif self.status == 1:
                # Pause
                self.timer_graph.stop()
                self.player.pausar()
                self.botoes_pause()
                self.status = 2
            else:
                # Resume
                self.player.tocar(self.preset[self.posicao_preset])
                self.botoes_play()
                self.status = 1
                self.timer_graph.start()
        
        if self.preset_mode == 2: # Preset Editing Mode (Start playing)
            self.OnStartPreset(None)   
            self.OnPlayPause(None)
       
    def OnStop (self, e):
        """
        Stop event
        """
        if self.preset_mode == 0: # Regular Mode
            self.data_input = []
            self.data_output = []
            self.status = 0
            if self.player is not None:
                self.player.pausar()
            self.botoes_pause()
            
        
        if self.preset_mode == 1: # Playing Preset
            self.data_input = []
            self.data_output = []
            self.status = 0
            if self.player is not None:
                self.player.pausar()
            self.botoes_pause()
            self.posicao_preset = 0
            self.lista_preset.DeleteAllItems()
            for filt in self.preset[self.posicao_preset]:
                self.lista_preset.InsertStringItem(sys.maxint, filt.name)

        self.on_redraw_graph(None)
    def OnNext (self, e):
        """
        Changes the preset's position to the next position
        """        
        if self.preset_mode == 1: # Playing
            self.posicao_preset+=1
            if self.posicao_preset >= len(self.preset):
                self.posicao_preset = 0
            self.lista_preset.DeleteAllItems()
            for filt in self.preset[self.posicao_preset]:
                self.lista_preset.InsertStringItem(sys.maxint, filt.name)
            if self.status != 1:
                return
            self.pausa_grafico = True
            self.player.muda_filtro(self.preset[self.posicao_preset], self)
           
            self.pausa_grafico = False
        elif self.preset_mode == 2: # Editing
            atual = int(self.list_edit_filters.GetItems()[int(self.list_edit_filters.GetSelection())])
            atual+=1
            if atual >= len(self.list_edit_filters.GetItems()):
                self.list_edit_filters.Append(str(atual))
                self.preset.append([])
            self.list_edit_filters.SetSelection(atual)
            self.mostra_lista_filtro(self.get_edit_list_selection())
   
    def OnPrevious (self, e):
        """
        Changes the preset's position to the previous position
        """   
        if self.preset_mode == 1: #Playing
            self.posicao_preset-=1
            if self.posicao_preset < 0:
                self.posicao_preset = len(self.preset)-1
            self.lista_preset.DeleteAllItems()
            for filt in self.preset[self.posicao_preset]:
                self.lista_preset.InsertStringItem(sys.maxint, filt.name)
            if self.status != 1:
                return
            self.pausa_grafico = True
            self.player.muda_filtro(self.preset[self.posicao_preset], self)
            self.pausa_grafico = False
        elif self.preset_mode == 2: #Editing
            atual = int(self.list_edit_filters.GetItems()[int(self.list_edit_filters.GetSelection())])
            atual-=1
            if atual < 0:
                return
            self.list_edit_filters.SetSelection(atual)
            self.mostra_lista_filtro(self.get_edit_list_selection())
          
    """
    Functions that manage the filter's editing
    Both on Preset Editing Mode and Regular Mode
    """
    def filter_list_box (self, parent, sizer, preset):
         """
         Creates a ListBox to edit the preset
         """
         self.list_edit_filters = wx.ListBox(parent, -1, size=(320,400))
         sizer.Add(self.list_edit_filters, 0)
         self.toolbar.Realize()
         self.Bind(wx.EVT_LISTBOX, self.OnClick)
         for i in range(len(preset)):
             self.list_edit_filters.Append(str(i))
    
    def get_edit_list_selection(self):
        """
        Returns the filters of the current preset's position.
        """
        if self.preset_mode == 2:
            sel = self.list_edit_filters.GetSelection()
            lista = []
            if sel == wx.NOT_FOUND:
                self.list_edit_filters.SetSelection(0)
                sel = 0
            else:
                sel = int(sel)
            sel = int(self.list_edit_filters.GetItems()[sel])
            lista = self.preset[sel]
            return lista         
    
    def mostra_lista_filtro(self, lista):
        """
        When on Preset Edigint Mode, it shows the filters in the current
        position
        """
        for i in range(len(self.filters[0])): 
            self.filters[0][i].SetValue(False)
            self.filters[1][i].Enable(False)  
        for filtro in lista:
            for i in range(len(self.filters[0])):
                if filtro.name == self.filters[2][i].name:
                    self.filters[0][i].SetValue(True)
                    self.filters[1][i].Enable(True)  
                    break                  
   
            
    def OnClick(self, e):
        """
        Click event on the preset's Listbox
        """
        self.mostra_lista_filtro(self.get_edit_list_selection())
            
    
    def filter_default_list(self, panel, sizer):
        """
        Creates the filters default list with the checkbox and the edit button
        """
        self.panel_filtros = wx.Panel(panel)
        self.panel_filtros.SetBackgroundColour("#666666")
        sizer.Add(self.panel_filtros,1, wx.EXPAND)
        box_esquerda = wx.BoxSizer(wx.VERTICAL)
        lista_filtros = filters.Filtro.filtros
        i = 0;
        for name,funcs in lista_filtros.items():
            if i % 2 == 0:  
                
                panel_de_dois = wx.Panel(self.panel_filtros)
                panel_de_dois.SetBackgroundColour("#666666")
                sizer_de_dois = wx.BoxSizer(wx.HORIZONTAL)
                if i == 0:
                    box_esquerda.Add(panel_de_dois, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 8) 
                else:
                    box_esquerda.Add(panel_de_dois, 1, wx.EXPAND | wx.BOTTOM, 8)  
                panel_de_dois.SetSizer(sizer_de_dois)
            panelTemp = wx.Panel(panel_de_dois)
            panelTemp.SetBackgroundColour("#DDDDDD")
            if i % 2 == 0:
                sizer_de_dois.Add(panelTemp, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
            else:
                sizer_de_dois.Add(panelTemp, 1, wx.EXPAND |  wx.RIGHT, 8)
            sizer_filtros = wx.BoxSizer(wx.VERTICAL)
            titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
            label_lista = wx.StaticText(panelTemp, label=name)
            label_lista.SetFont(titulo)
            label_lista.SetForegroundColour("#111111")
            sizer_filtros.Add(label_lista, 0, wx.EXPAND | wx.ALL, 10)
            panelTemp.SetSizer(sizer_filtros)
            for func in funcs:
                filtro = func()
                panel_um = wx.Panel(panelTemp)     
                sizer_um = wx.BoxSizer(wx.HORIZONTAL)
                check = wx.CheckBox(panel_um,label=filtro.name)
                botao = wx.Button(panel_um,label="Edit")
                sizer_um.Add(check, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 10)
                sizer_um.Add(botao, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 10)
                panel_um.SetSizer(sizer_um)
                check.Bind(wx.EVT_CHECKBOX, self.check_filter)
                botao.Bind(wx.EVT_BUTTON, self.edit_filter)
                sizer_filtros.Add(panel_um, 0, wx.EXPAND | wx.ALL, 12)
                self.filters[0].append(check)
                self.filters[1].append(botao)
                self.filters[2].append(filtro)
            i += 1
        data.load_defaults(self.filters[2])
        self.panel_filtros.SetSizer(box_esquerda)

        self.panel_esquerda.Fit()
        self.sizer_principal.Layout()
        self.panel_direita.Fit()
        self.panel_direita.Layout()
        self.Layout()
        self.panel_direita.Update()
        self.panel_direita.Update()
        self.sizer_direita.Layout()
        
    def check_filter(self, e):
        """
        Checkbox filter click event
        """
        obj = e.GetEventObject()
        ind = self.filters[0].index(obj)
        if self.preset_mode == 0:
            
            if obj.GetValue():
                self.filtros_aplicados.append(self.filters[2][ind])
            else:
                self.filtros_aplicados.remove(self.filters[2][ind])
            if self.status == 1:
                self.player.muda_filtro(self.filtros_aplicados, self)
        elif self.preset_mode == 2: # Editing
            if obj.GetValue():
                novo_filtro = copy.deepcopy(self.filters[2][ind])
                self.get_edit_list_selection().append(novo_filtro)
                self.filters[1][ind].Enable(True)
            else:
                tudo = self.get_edit_list_selection()
                for filtro in tudo:
                    if filtro.name == self.filters[2][ind].name:
                        tudo.remove(filtro)
                        break;
                self.filters[1][ind].Enable(False)
                    

    def edit_filter (self, e):
        """
        Open the window to edit the filter's parameters
        The filter is in the list in the self.filters tuple when preset_mode=1
        """
        if self.preset_mode == 0:
            filtro = self.filters[2][self.filters[1].index(e.GetEventObject())]
            janela = edit_window(self,e.GetEventObject(),filtro,False)
            janela.ShowModal()
            janela.Destroy()       
        elif self.preset_mode == 2:
            filtro = self.filters[2][self.filters[1].index(e.GetEventObject())]
            for filt in self.get_edit_list_selection():
                if filt.name == filtro.name:
                    filtro = filt
                    break
            janela = edit_window(self,e.GetEventObject(),filtro,True)
            janela.ShowModal()
            janela.Destroy() 
        
    """
    Functions to handlde the graphs
    """
    def desenha_graficos(self):
        titulo = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.pausa_grafico = False
        # Graphs Panel/Sizer 
        self.panel_graficos = wx.Panel(self.panel_direita, size=(320,0))
        self.sizer_graficos = wx.BoxSizer(wx.VERTICAL)
        self.panel_graficos.SetSizer(self.sizer_graficos)  
        # Input        
        txt = wx.StaticText(self.panel_graficos, label=u"Input")
        txt.SetFont(titulo)
        txt.SetForegroundColour("#FFFFFF")
        self.sizer_graficos.Add(txt,0, wx.LEFT, 10)
        self.timer_graph = self.create_input_graph(self.panel_graficos,self.sizer_graficos)
        
        
        # Output
        txt2 = wx.StaticText(self.panel_graficos, label=u"Output")
        txt2.SetFont(titulo)
        txt2.SetForegroundColour("#FFFFFF")       
        self.sizer_graficos.Add(txt2,0, wx.LEFT, 10)
        self.timer_graph2 = self.create_output_graph(self.panel_graficos,self.sizer_graficos)        
        self.sizer_direita.Add(self.panel_graficos,0,wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        
        
        line2 = wx.StaticLine(self.panel_graficos, size=(320,2), style=wx.LI_HORIZONTAL)
        self.sizer_graficos.Add(line2,0,border=0)
        
    # Functions create_input_graph, create_output_graph e on_redraw_graph
    # Based on http://eli.thegreenplace.net/files/prog_code/wx_mpl_dynamic_graph.py.txt 
    def create_output_graph(self, parent, sizer):
        """
        Creates a graph that plots the output
        """
        graph_panel = wx.Panel(parent, size=(320,0))
        self.data_output = []
        dpi = 160
        fig = Figure((2.0, 1.0), dpi=dpi)
        self.axes_output = fig.add_subplot(111)
        fig.add_subplot()
        fig.subplots_adjust(bottom=0.009,left=0.003,right=0.997, top=0.991)
        self.axes_output.set_axis_bgcolor('black')
        pylab.setp(self.axes_output.get_xticklabels(), fontsize=4)
        pylab.setp(self.axes_output.get_yticklabels(), fontsize=4)        
        self.plot_data_output = self.axes_output.plot(self.data_output, 
            linewidth=1,
            color=(0, 0, 1),
            )[0] 
        self.axes_output.grid(True, color='gray')
        self.canvas_output = FigCanvas(graph_panel, -1, fig)        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.canvas_output, 0)        
        graph_panel.SetSizer(vbox)
        sizer.Add(graph_panel, 0, wx.TOP | wx.BOTTOM, 5)
        self.axes_output.set_xbound(lower=0, upper=100)
        self.axes_output.set_ybound(lower=-1.0, upper=1.0)

    
    def create_input_graph(self, parent, sizer):
        """
        Creates a graph that plots the input
        It returns a timer what starts the plotting
        """
        graph_panel = wx.Panel(parent, size=(320,0))
        self.input_data_generator = DataGen(self)
        self.data_input = []
        dpi = 160
        fig = Figure((2.0, 1.0), dpi=dpi)
        self.axes_input = fig.add_subplot(111)
        fig.add_subplot()
        fig.subplots_adjust(bottom=0.009,left=0.003,right=0.997, top=0.991)
        self.axes_input.set_axis_bgcolor('black')
        pylab.setp(self.axes_input.get_xticklabels(), fontsize=4)
        pylab.setp(self.axes_input.get_yticklabels(), fontsize=4)        
        self.plot_data_input = self.axes_input.plot(self.data_input, 
            linewidth=1,
            color=(1, 0, 0),
            )[0] 
        self.axes_input.grid(True, color='gray')
        self.canvas_input = FigCanvas(graph_panel, -1, fig)        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.canvas_input, 0)        
        graph_panel.SetSizer(vbox)
        sizer.Add(graph_panel, 0, wx.TOP | wx.BOTTOM, 5)
        self.axes_input.set_xbound(lower=0, upper=100)
        self.axes_input.set_ybound(lower=-1.0, upper=1.0)
        redraw_timer_input = MyThread(self.graph_refresh_time, self.on_redraw_graph, self) #wx.Timer(self)
        return redraw_timer_input
        
        
    def on_redraw_graph(self, event):
        """
        Function that is called by the timer thread to update the graph
        """
        if self.pausa_grafico:
            return
        if self.status != 1:
            self.plot_data_input.set_xdata(np.arange(len(self.data_input)))
            self.plot_data_input.set_ydata(np.array(self.data_input))
            self.plot_data_output.set_xdata(np.arange(len(self.data_output)))
            self.plot_data_output.set_ydata(np.array(self.data_output))
            self.canvas_input.draw()
            self.canvas_output.draw()
            self.timer_graph.stop()
            return
            
        tupla = self.input_data_generator.next()
        if tupla is None:
            return
        self.data_input.append(tupla[0])
        self.data_output.append(tupla[1])
        xmax_in = len(self.data_input) if len(self.data_input) > 100 else 100
        xmin_in = xmax_in - 100   
        size = round(max(abs(max(self.data_input[-100:])),abs(min(self.data_input[-100:])),abs(max(self.data_output[-100:])),abs(min(self.data_output[-100:]))),2)
        if size == 0.00:
            size = 1.     
        ymax_in = size*1.1
        ymin_in = size*(-1.1)     
       
        
        xmax_out = len(self.data_output) if len(self.data_output) > 100 else 100
        xmin_out = xmax_out - 100       
        ymax_out = size*1.1
        ymin_out = size*(-1.1)      
       
        self.axes_input.set_xbound(lower=xmin_in, upper=xmax_in)
        self.axes_input.set_ybound(lower=ymin_in, upper=ymax_in)
        self.plot_data_input.set_xdata(np.arange(len(self.data_input)))
        self.plot_data_input.set_ydata(np.array(self.data_input))
        
        
        self.axes_output.set_xbound(lower=xmin_out, upper=xmax_out)
        self.axes_output.set_ybound(lower=ymin_out, upper=ymax_out)
        self.plot_data_output.set_xdata(np.arange(len(self.data_output)))
        self.plot_data_output.set_ydata(np.array(self.data_output))
        
        
        if self.panel_graficos is not None:
            self.canvas_input.draw()
            self.canvas_output.draw()
        

    def OnQuit(self, e):
        self.__del__()
  
    def __del__(self):
        """
        Kills other threads
        """
        self.status = 0
        try:
            self.OnStop(None)
        except:
            pass
        del self.timer_graph
        if self.player is not None and not self.player.player.finished:
            del self.player
        try:
            del self.pedal
        except:
            pass
        self.Destroy()
        
       
   
class edit_window (wx.Dialog):
     """
     Edit Window.     
     It can save the changed parameters as default 
     or if you are in Preset Editing Mode, it only saves temporally.
     """
     def __init__(self, window, check, filtro, usando_preset=False):
        """
        window: It is the main window
        check: The filter checkbox
        filtro: The filter
        usando_preset: If you are in Preset Editing Mode, it's True, otherwise,
        it's False
        """
        super(edit_window, self).__init__(None) 
        self.filtro = filtro
        self.check = check
        self.window = window
        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle(filtro.name)
        self.preset = usando_preset
     
     def InitUI(self):
        """
        Initializes the edit window
        """
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        sb = wx.StaticBox(pnl, label=u'Parameters')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL) 
        params = self.filtro.params
        i = 0
        self.texts = []
        for nome,tupla in params.items():
            panel_parametro = wx.Panel(pnl)
            sizer_parametro = wx.BoxSizer(wx.VERTICAL)
            panel_parametro.SetSizer(sizer_parametro)
            
            
            panel_texto = wx.Panel(panel_parametro)
            sizer_parametro.Add(panel_texto)
            sizer_texto = wx.BoxSizer(wx.HORIZONTAL)
            panel_texto.SetSizer(sizer_texto)
            texto = wx.StaticText(panel_texto, label=nome + ": ")
            valor = wx.TextCtrl(panel_texto, size=(50,-1), name=nome)
            valor.SetValue(str(float(self.filtro.vparams[i])))
                
            sizer_texto.Add(texto, wx.EXPAND | wx.RIGHT, 5)
            sizer_texto.Add(valor, wx.EXPAND | wx.LEFT, 5)
            self.texts.append(valor)
            
            slider = FloatSlider(panel_parametro,value=float(self.filtro.vparams[i]),min_val=float(tupla[2][0])
                        , max_val=float(tupla[2][1]),res = float((tupla[2][1]-tupla[2][0])/10000.0)
                        ,name=nome, size=(230,-1), texto=valor)
            valor.Bind(wx.EVT_TEXT, slider.UpdateValue)
            sizer_parametro.Add(slider)
            sbs.Add(panel_parametro)
            i+=1
            
        pnl.SetSizer(sbs)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Save')
        closeButton = wx.Button(self, label='Cancel')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)
        vbox.Add(pnl, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, 
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        okButton.Bind(wx.EVT_BUTTON, self.OnSave)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
   
     def OnClose(self, e): 
        self.Destroy()
    
     def OnSave(self, e):
         """
         Saves the changes.
         """
         valores = []
         i = 0
         for texto in self.texts:
             try:
                 valor = float(texto.GetValue())
             except:
                 valor = float(self.filtro.params.values()[i][0])
             i += 1
             valores.append(valor)
         self.filtro.vparams = valores
         if not self.preset:
             data.salva_defaults(self.window.filters[2])
             if self.window.player is not None:
                 self.window.player.muda_filtro(self.window.filtros_aplicados, self.window)
         self.Destroy()


def create_main_window():
    """
    Function that creates the main window and instantiates everything needed
    to start the program
    """  
    app = wx.App()
    window = main_window(None,title="Digital Pedalboard",name="main_window")
    app.MainLoop()
    return window

window = create_main_window()
