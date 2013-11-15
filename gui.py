# -*- coding: utf-8 -*-
"""
File to create windows and widgets

"""
import data
import filters
import wx
import player
import copy
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import serialcom as sc
# http://zetcode.com/wxpython/advanced/
class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
    def OnResize(self, event):
        pass
#import numpy

# Adaptado de http://stackoverflow.com/questions/4709087/wxslider-with-floating-point-values
class FloatSlider(wx.Slider):

    def __init__(self, parent, id=-1, value=0.00, min_val=None, max_val=None, res=1e-4,
                 size=wx.DefaultSize, style=wx.SL_HORIZONTAL,
                 name='floatslider', texto=None):
        self._value = value
        self.defaultValue = float(value)
        self._min = min_val
        self._max = max_val
        self.texto = texto
        self._res = res
        #self.precision = int(numpy.log10(1/res))
        #print self.precision
        ival, imin, imax = [round(v/res) for v in (value, min_val, max_val)]
        self._islider = super(FloatSlider, self)
        self._islider.__init__(
            parent, id, ival, imin, imax, size=size, style=style, name=name
        )
        self.Bind(wx.EVT_SCROLL, self._OnScroll)

    def _OnScroll(self, event):
        ival = self._islider.GetValue()
        imin = self._islider.GetMin()
        imax = self._islider.GetMax()
        if ival == imin:
            self._value = self._min
        elif ival == imax:
            self._value = self._max
        else:
            self._value = ival * self._res
        self.texto.SetValue(str(self._value))
        event.Skip()
        #print 'OnScroll: value=%f, ival=%d' % (self._value, ival)

    def GetValue(self):
        return self._value

    def GetMin(self):
        return self._min

    def GetMax(self):
        return self._max

    def GetRes(self):
        return self._res

    def SetValue(self, value):
        self._islider.SetValue(round(value/self._res))
        self._value = value

    def SetMin(self, minval):
        self._islider.SetMin(round(minval/self._res))
        self._min = minval

    def SetMax(self, maxval):
        self._islider.SetMax(round(maxval/self._res))
        self._max = maxval

    def SetRes(self, res):
        self._islider.SetRange(round(self._min/res), round(self._max/res))
        self._islider.SetValue(round(self._value/res))
        self._res = res

    def SetRange(self, minval, maxval):
        self._islider.SetRange(round(minval/self._res), round(maxval/self._res))
        self._min = minval
        self._max = maxval
    def UpdateValue(self, e):
        valor = e.GetEventObject().GetValue()
        try:
            valor = float(valor)
        except:
            if valor == "":        
                valor = self.defaultValue
                
            else:
                valor = self.defaultValue
                e.GetEventObject().SetValue(float(valor))
            
        self.SetValue(valor)

class edit_window (wx.Dialog):
     def __init__(self, window, check, filtro, usando_preset=False):
        super(edit_window, self).__init__(None) 
        self.filtro = filtro
        self.check = check
        self.window = window
        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle(filtro.name)
        self.preset = usando_preset
     
     def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        sb = wx.StaticBox(pnl, label=u'Parâmetros')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL) 
        params = self.filtro.params
        i = 0
        self.texts = []
        for nome,tupla in params.items():
            # (valor_padrao, tipo, (valor_inicial,valor_final))
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
            """sbs.Add(wx.RadioButton(pnl, label='256 Colors', 
                style=wx.RB_GROUP))
            sbs.Add(wx.RadioButton(pnl, label='16 Colors'))
            sbs.Add(wx.RadioButton(pnl, label='2 Colors'))
            
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
            hbox1.Add(wx.RadioButton(pnl, label='Custom'))
            hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
            sbs.Add(hbox1)
            """
            i+=1
            
        pnl.SetSizer(sbs)
       
       
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Salvar')
        closeButton = wx.Button(self, label='Cancelar')
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
         valores = []
         i = 0
         for texto in self.texts:
             try:
                 valor = float(texto.GetValue())
             except:
                 valor = float(self.filtro.params.values()[i][0])
             i += 1
             valores.append(valor)
         #self.window.filters_edicao[self.check].vparams = valores
         #self.window.filters_edicao[self.check].update_default()
         self.filtro.vparams = valores
         if not self.preset:
             data.salva_defaults(self.window.filters[2])
         self.Destroy()
    
class main_window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(main_window, self).__init__(*args, **kwargs) 
        self.InitUI()
    """
    Modos (Tocando, Editando Preset, Tocando Preset)
    """
    def modo_tocando(self):
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
        self.menubar.EnableTop(1, False)
        
      #  self.botoes_pause()
        
        self.toolbar.EnableTool(wx.ID_STOP, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, False)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, False)
        self.toolbar.EnableTool(wx.ID_UP, True)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
        
        pass
    def modo_edita_preset(self):
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
        if self.list_edit_filters is not None:
             self.list_edit_filters.Destroy()
             self.list_edit_filters = None
        self.filtros_aplicados = []
        self.status = 0
        self.preset_mode = 2
        self.menu.Enable(wx.ID_NEW, 1)
        self.menu.Enable(wx.ID_OPEN, 1)
        self.menubar.EnableTop(1, True)
        self.menu_preset.Enable(wx.ID_SAVE, True)
        self.menu_preset.Enable(wx.ID_SETUP, True)
        self.menu_preset.Enable(wx.ID_EDIT, False)
        
        self.toolbar.EnableTool(wx.ID_STOP, False)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.EnableTool(wx.ID_UP, False)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
        


    def modo_tocando_preset(self):
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
        self.menu_preset.Enable(wx.ID_SAVE, False)
        self.menu_preset.Enable(wx.ID_SETUP, False)
        self.menu_preset.Enable(wx.ID_EDIT, True)
        
        self.toolbar.EnableTool(wx.ID_STOP, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.EnableTool(wx.ID_UP, True)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
        
        pass
    def panel_normal(self, parent):
        pass
    def panel_preset (self, parent):
        pass
    def __del__(self):
        if self.player is not None and not self.player.player.finished:
            del self.player
        del self.pedal
    def OnStartPreset(self ,e):
        self.filters = ([],[],[])
        self.filtros_aplicados = []        
        self.sizer_esquerda.Remove(self.panel_filtros)
        self.panel_filtros.Destroy()
       # self.panel_filtros.Show(False)
        self.panel_filtros = None
        self.modo_tocando_preset()
        self.panel_preset = wx.Panel(self.panel_esquerda)
        self.sizer_esquerda.Add(self.panel_preset, 1, wx.EXPAND)      
#        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin()
        self.lista_preset = wx.ListCtrl(self.panel_preset,style=wx.LC_REPORT)
        
        temp_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_preset.SetSizer(temp_sizer)
        self.panel_preset.SetBackgroundColour("#880000")
        self.lista_preset.InsertColumn(0, "Filtros")
        
        temp_sizer.Add(self.lista_preset,1,wx.EXPAND)
        #self.lista_preset.SetResizeColumn(0)
        self.panel_esquerda.Fit()
        self.sizer_principal.Layout()
        for item in self.preset[0]:
           self.lista_preset.InsertStringItem(sys.maxint, item.name)

        self.lista_preset.SetColumnWidth(0, self.lista_preset.GetSize()[0]-5)
        self.pedal = sc.SerialData(func_proximo=lambda: self.OnNext(None),
                                   func_anterior=lambda: self.OnPrevious(None))
        filters.pedal = self.pedal.pedal
     
    def OnEditPreset(self, e):
        pass
    def OnVoltar(self, e):
        if self.preset_mode == 1:
            self.sizer_esquerda.Remove(self.panel_preset)
            self.panel_preset.Destroy()
            self.filter_default_list(self.panel_esquerda,self.sizer_esquerda)
            self.panel_esquerda.Fit()
            self.sizer_principal.Layout()
            
           
        self.modo_tocando()
        pass
    def InitUI(self):    
        # Cria o menu       
        #self.SetScrollbar(wx.VERTICAL, 0, 16, 50)
        self.menubar = wx.MenuBar()
        self.menu = wx.Menu()
        item1 = self.menu.Append(wx.ID_NEW, "Novo Preset", "Criar novo preset de filtros")
        item2 = self.menu.Append(wx.ID_OPEN, "Carregar Preset", "Carregar preset de filtros")
        item3 = self.menu.Append(wx.ID_EXIT, "Sair", "Sair do aplicativo")
        self.menubar.Append(self.menu , 'Arquivo')
       

        self.menu_preset = wx.Menu()
        item_voltar = self.menu_preset.Append(wx.ID_BACKWARD, "Voltar", "Voltar")   
        item_salvar = self.menu_preset.Append(wx.ID_SAVE, "Salvar Preset", "Salvar preset de filtros")
        item_editar = self.menu_preset.Append(wx.ID_EDIT, "Editar Preset", "Editar Preset")
        item_start = self.menu_preset.Append(wx.ID_SETUP, "Executar Preset", "Executar Preset")
        self.menubar.Append(self.menu_preset , 'Preset')
       
             
        
        self.SetMenuBar(self.menubar) 
        
        self.menubar.EnableTop(1, False)
        self.Bind(wx.EVT_MENU, self.OnNewPreset, item1)
        self.Bind(wx.EVT_MENU, self.OnLoadPreset, item2)
        self.Bind(wx.EVT_MENU, self.OnQuit, item3)
        self.Bind(wx.EVT_MENU, self.OnEditPreset, item_editar)
        self.Bind(wx.EVT_MENU, self.OnSavePreset, item_salvar)
        self.Bind(wx.EVT_MENU, self.OnStartPreset, item_start)
        self.Bind(wx.EVT_MENU, self.OnVoltar, item_voltar)
        # Status do player 0-Parado,1-Tocando,2-Pausado
        self.status = 0      
        
        # Status do uso do preset. 0-sem usar, 1-Tocando Preset, 2-Editando preset
        self.preset_mode = 0
        # Preset = lista de lista de filtros
        self.preset = []
      
        # Cria  barra de menus (play/pause/next/previous)
        """
        self.toolbar = self.CreateToolBar()
        previous = self.toolbar.AddLabelTool(wx.ID_PREVIEW_PREVIOUS,'Previous', wx.Bitmap('images/previous.png'))
        stop = self.toolbar.AddLabelTool(wx.ID_STOP,'Stop', wx.Bitmap('images/stop.png'))
        play = self.toolbar.AddLabelTool(wx.ID_UP,'Play/Pause', wx.Bitmap('images/play.png'))
        nextt = self.toolbar.AddLabelTool(wx.ID_PREVIEW_NEXT,'Next', wx.Bitmap('images/next.png'))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnPlayPause, play)
        self.Bind(wx.EVT_TOOL, self.OnStop, stop)
        self.Bind(wx.EVT_TOOL, self.OnPrevious, previous)
        self.Bind(wx.EVT_TOOL, self.OnNext, nextt)
       
       
        """
        
        

        self.list_edit_filters = None
        # Cria os panels que contem os filtros
       # self.panel_principal = wx.Panel(self, -1)
      #  wx.lib.scrolledpanel   
        self.panel_principal = wx.ScrolledWindow(self,-1)
        self.panel_principal.SetScrollbars(1,1,1000,1000)
        self.panel_principal.SetBackgroundColour("#4f5049")
        self.sizer_principal = wx.BoxSizer(wx.HORIZONTAL)
       
        self.panel_esquerda = wx.Panel(self.panel_principal)
        self.panel_esquerda.SetBackgroundColour('#ffffff')
     
        self.sizer_esquerda = wx.BoxSizer(wx.VERTICAL)
        self.sizer_direita = wx.BoxSizer(wx.VERTICAL)

        self.panel_esquerda.SetSizerAndFit(self.sizer_esquerda)
        self.panel_direita = wx.Panel(self.panel_principal,size=(320,0))
        #self.panel_direita.SetSizer(self.sizer_direita)
        self.panel_direita.SetBackgroundColour('#000000')
        self.sizer_principal.Add(self.panel_esquerda, 1, wx.EXPAND | wx.ALL, 7)      
        self.sizer_principal.Add(self.panel_direita, 0, wx.EXPAND | wx.ALL, 7)    
        self.panel_principal.SetSizer(self.sizer_principal)
        
        # Botões no panel_direita
        self.panel_botoes = wx.Panel(self.panel_direita, size=(260,60))
        self.sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_direita.Add(self.panel_botoes, 0, wx.EXPAND | wx.ALL, 2)
                
        
        previous = wx.BitmapButton(self.panel_botoes, bitmap=wx.Bitmap('images/previous.png'))
        stop = wx.BitmapButton(self.panel_botoes, bitmap=wx.Bitmap('images/stop.png'))
        play= wx.BitmapButton(self.panel_botoes, bitmap=wx.Bitmap('images/play.png'))
        nextt = wx.BitmapButton(self.panel_botoes, bitmap=wx.Bitmap('images/next.png'))

        self.Bind(wx.EVT_BUTTON, self.OnPlayPause, play)
        self.Bind(wx.EVT_BUTTON, self.OnStop, stop)
        self.Bind(wx.EVT_BUTTON, self.OnPrevious, previous)
        self.Bind(wx.EVT_BUTTON, self.OnNext, nextt)
        self.sizer_botoes.Add(previous, 0, wx.EXPAND | wx.ALL, 1)        
        self.sizer_direita.Add(stop, 0, wx.EXPAND | wx.ALL, 1)   
        self.sizer_botoes.Add(play, 0, wx.EXPAND | wx.ALL, 1)   
        self.sizer_botoes.Add(nextt, 0, wx.EXPAND | wx.ALL, 1)  
        self.panel_botoes.SetSizer(self.sizer_botoes)
        # Variáveis relacionadas ao filtro
        #Uma tupla formada por 3 listas (check,edita,filtro)
        self.filters = ([],[],[])
        self.filtros_aplicados = []
        self.player = None
        
         
        self.filter_default_list(self.panel_esquerda, self.sizer_esquerda)
        self.modo_tocando()
        
        self.Show(True)    
        self.Maximize()
        
   
        
  
    
    def botoes_pause(self):
                
        if self.preset_mode == 0:
            self.toolbar.EnableTool(wx.ID_STOP,True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS,False)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT,False)
       
        if self.preset_mode == 1:
            self.toolbar.EnableTool(wx.ID_STOP,True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS,True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT,True)   

        self.toolbar.EnableTool(wx.ID_UP,True)    
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
    
    def botoes_play(self):
        if self.preset_mode == 0:
            self.toolbar.EnableTool(wx.ID_STOP, True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, False)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, False)
        if self.preset_mode == 1:
            self.toolbar.EnableTool(wx.ID_STOP, True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
            self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        
        self.toolbar.EnableTool(wx.ID_UP,True)  
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/pause.png'))
        
    def botoes_edit_preset(self):
        self.toolbar.EnableTool(wx.ID_STOP, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.EnableTool(wx.ID_UP, False)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
        
    def OnQuit(self, e):
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
    
    def OnPlayPause (self, e):
        if self.preset_mode == 0: # Reproduzindo sem preset
            if self.status == 0:
                # Começa a tocar            
                self.player = player.Player(self.filtros_aplicados)
                self.botoes_play()
                self.status = 1
            elif self.status == 1:
                # Pausa
                self.player.pausar()
                self.botoes_pause()
                self.status = 2
            else:
                # Resume
                self.player.tocar()
                self.botoes_play()
                self.status = 1
        if self.preset_mode == 1: # Reproduzindo um preset
            
            if self.status == 0:
                # Começa a tocar   
                self.player = player.Player(tuple(self.preset))
                self.botoes_play()
                self.status = 1
            elif self.status == 1:
                # Pausa
                self.player.pausar()
                self.botoes_pause()
                self.status = 2
            else:
                # Resume
                self.player.tocar()
                self.botoes_play()
                self.status = 1
       
    def OnStop (self, e):
        if self.preset_mode == 0:
            if self.player is not None:
                self.player.pausar()
            self.botoes_pause()
            self.status = 0
        
        if self.preset_mode == 1:
            if self.player is not None:
                self.player.pausar()
            self.botoes_pause()
            self.status = 0
            
    def OnNext (self, e):
        """
        Função que muda para o próximo filtro do preset atual
        """        
        if self.preset_mode == 1: #Tocando
            self.player.next_filter()
            self.lista_preset.DeleteAllItems()
            for filt in self.player.filtros[self.player.posicao]:
                self.lista_preset.InsertStringItem(sys.maxint, filt.name)
        elif self.preset_mode == 2: #Editando
            atual = int(self.list_edit_filters.GetItems()[int(self.list_edit_filters.GetSelection())])
            atual+=1
            if atual >= len(self.list_edit_filters.GetItems()):
                self.list_edit_filters.Append(str(atual))
                self.preset.append([])
            self.list_edit_filters.SetSelection(atual)
            self.mostra_lista_filtro(self.get_edit_list_selection())
   
    def OnPrevious (self, e):
        """
        Função que muda para o filtro anterior do preset atual
        """   
        if self.preset_mode == 1: #Tocando
            self.player.previous_filter()
            self.lista_preset.DeleteAllItems()
            for filt in self.player.filtros[self.player.posicao]:
                self.lista_preset.InsertStringItem(sys.maxint, filt.name)
        
        elif self.preset_mode == 2: #Editando
            atual = int(self.list_edit_filters.GetItems()[int(self.list_edit_filters.GetSelection())])
            atual-=1
            if atual < 0:
                return
            self.list_edit_filters.SetSelection(atual)
            self.mostra_lista_filtro(self.get_edit_list_selection())
        
    def mostra_lista_filtro(self, lista):
        for i in range(len(self.filters[0])): 
            self.filters[0][i].SetValue(False)
            self.filters[1][i].Enable(False)  
        for filtro in lista:
            for i in range(len(self.filters[0])):
                if filtro.name == self.filters[2][i].name:
                    self.filters[0][i].SetValue(True)
                    self.filters[1][i].Enable(True)  
                    break
                    
    def salva_lista_filtro(self, lista):
        pass
    
    def get_edit_list_selection(self):
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
    def OnClick(self, e):
        """
        Onclick da edição de preset
        """
        self.mostra_lista_filtro(self.get_edit_list_selection())
            
    def filter_list_box (self, parent, sizer, preset):
         self.list_edit_filters = wx.ListBox(parent, -1,size=(320,600))
        # sizer.Add(self.list_edit_filters, 0, wx.EXPAND | wx.TOP, 10)
         self.Bind(wx.EVT_LISTBOX, self.OnClick)
         for i in range(len(preset)):
             self.list_edit_filters.Append(str(i))
             
    def OnNewPreset(self, e):
         self.modo_edita_preset()         
         self.preset = [[]]
         self.filter_list_box(self.panel_direita, self.sizer_direita, self.preset)
         self.list_edit_filters.SetSelection(0)
         self.mostra_lista_filtro([])
    def OnSavePreset(self, e):
        openFileDialog = wx.FileDialog(self, "Digite o nome do arquivo para salvar o seu preset", "", "",
                                       "Arquivos de Preset (*.preset)|*.preset", wx.FD_SAVE)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        #arquivo = open(openFileDialog.GetPath(),)
        data.save_preset(openFileDialog.GetPath(), self.preset)
            
    def OnLoadPreset(self, e):
        # Abre a janela perguntando o arquivo        
        openFileDialog = wx.FileDialog(self, "Digite o nome do arquivo para carregar o seu preset", "", "",
                                       "Arquivos de Preset (*.preset)|*.preset", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        #arquivo = open(openFileDialog.GetPath(),)
        self.modo_edita_preset()        
        self.preset = data.load_preset(openFileDialog.GetPath())
        self.filter_list_box(self.panel_direita, self.sizer_direita, self.preset)
        self.list_edit_filters.SetSelection(0)
        self.mostra_lista_filtro(self.preset[0])
        
    
    def filter_default_list(self, panel, sizer):
        """
        Cria as listas de filtros padrão com checkbox e 
        """
        self.panel_filtros = wx.Panel(panel)
        sizer.Add(self.panel_filtros,1, wx.EXPAND | wx.ALL,1)
        box_esquerda = wx.BoxSizer(wx.VERTICAL)
        lista_filtros = filters.Filtro.filtros
        i = 0;
        for name,funcs in lista_filtros.items():
            if i % 2 == 0:            
                panel_de_dois = wx.Panel(self.panel_filtros)
                panel_de_dois.SetBackgroundColour("#EEEEEE")
                sizer_de_dois = wx.BoxSizer(wx.HORIZONTAL)
                box_esquerda.Add(panel_de_dois, 1, wx.EXPAND | wx.ALL, 10)  
                panel_de_dois.SetSizer(sizer_de_dois)
            panelTemp = wx.Panel(panel_de_dois)
            panelTemp.SetBackgroundColour("#CCCCCC")
            sizer_de_dois.Add(panelTemp, 1, wx.EXPAND | wx.RIGHT, wx.LEFT, 5)
            sizer_filtros = wx.BoxSizer(wx.VERTICAL)
            label_lista = wx.StaticText(panelTemp, label=name)
            sizer_filtros.Add(label_lista, 0, wx.EXPAND | wx.LEFT | wx.TOP, 5)
            panelTemp.SetSizer(sizer_filtros)
            for func in funcs:
                filtro = func()
                panel_um = wx.Panel(panelTemp)     
                sizer_um = wx.BoxSizer(wx.HORIZONTAL)
                check = wx.CheckBox(panel_um,label=filtro.name)
                botao = wx.Button(panel_um,label="Editar")
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
        self.panel_filtros.Fit()        
        panel.Fit()
        panel.Layout()
        self.Layout()
        self.panel_filtros.Update()
        panel.Update()
        sizer.Layout()
    
    def edit_filter (self, e):
        """
        Abre janela para edição dos parâmetros do filtro
        O Filtro está na lista na tupla self.filters para preset_mode=1
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
    
    def check_filter(self, e):
        obj = e.GetEventObject()
        ind = self.filters[0].index(obj)
        if self.preset_mode == 0:
            if obj.GetValue():
                self.filtros_aplicados.append(self.filters[2][ind])
            else:
                self.filtros_aplicados.remove(self.filters[2][ind])
        elif self.preset_mode == 2: # Editando
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


def filter_window():
    """
    Open a popup to show filter settings
    """
    pass

window = create_main_window()