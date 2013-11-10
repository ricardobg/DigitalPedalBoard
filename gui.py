# -*- coding: utf-8 -*-
"""
File to create windows and widgets

"""
import data
import filters
import wx
import player
#import numpy

#wx.lib.agw.floatspin.FloatSpin.
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
     def __init__(self, window, check, filtro):
        super(edit_window, self).__init__(None) 
        self.filtro = filtro
        self.check = check
        self.window = window
        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle(filtro.name)
        
     
     
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
         self.window.filters_edicao[self.check].vparams = valores
         self.window.filters_edicao[self.check].update_default()
         if self.window.preset_mode == 0:
             data.salva_defaults(self.window.filters_edicao.values())
         self.Destroy()
    
class main_window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(main_window, self).__init__(*args, **kwargs) 
        self.InitUI()
    
    def modo_normal(self):
        self.status = 0
        self.preset = []
        self.preset_mode = 0
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
        self.botoes_pause()
        pass
    def modo_edita_preset(self):
        self.status = 0
        self.preset_mode = 2
        self.botoes_edit_preset()
        pass
    def modo_executa_preset(self):
        self.status = 1
        self.preset_mode = 1
        pass
    
    def InitUI(self):    
        # Cria o menu       
        #self.SetScrollbar(wx.VERTICAL, 0, 16, 50)
        menubar = wx.MenuBar()
        menu = wx.Menu()
        item1 = menu.Append(wx.ID_NEW, "Novo Preset", "Criar novo preset de filtros")
        item2 = menu.Append(wx.ID_OPEN, "Carregar Preset", "Carregar preset de filtros")
        item4 = menu.Append(wx.ID_SAVE, "Salvar Preset", "Salvar preset de filtros")
        item3 = menu.Append(wx.ID_EXIT, "Sair", "Sair do aplicativo")
        menubar.Append(menu, 'Arquivo')
        menu.Enable(wx.ID_SAVE, 0)
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnNewPreset, item1)
        self.Bind(wx.EVT_MENU, self.OnLoadPreset, item2)
        self.Bind(wx.EVT_MENU, self.OnQuit, item3)
        self.Bind(wx.EVT_MENU, self.OnSavePreset, item4)
        # Status do player 0-Parado,1-Tocando,2-Pausado
        self.status = 0      
        
        # Status do uso do preset. 0-sem usar, 1-Reproduzindo, 2-Editando
        self.preset_mode = 0
        self.preset = []
        # Cria  barra de menus (play/pause/next/previous)
        self.toolbar = self.CreateToolBar()
        previous = self.toolbar.AddLabelTool(wx.ID_PREVIEW_PREVIOUS,'Previous', wx.Bitmap('images/previous.png'))
        stop = self.toolbar.AddLabelTool(wx.ID_STOP,'Stop', wx.Bitmap('images/stop.png'))
        play = self.toolbar.AddLabelTool(wx.ID_UP,'Play/Pause', wx.Bitmap('images/play.png'))
        nextt = self.toolbar.AddLabelTool(wx.ID_PREVIEW_NEXT,'Next', wx.Bitmap('images/next.png'))
          
        self.botoes_pause()
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnPlayPause, play)
        self.Bind(wx.EVT_TOOL, self.OnStop, stop)
        self.Bind(wx.EVT_TOOL, self.OnPrevious, previous)
        self.Bind(wx.EVT_TOOL, self.OnNext, nextt)


        # Cria os panels que contem os filtros
        self.panel_principal = wx.Panel(self, -1)
        self.panel_principal.SetBackgroundColour("#4f5049")
        self.sizer_principal = wx.BoxSizer(wx.HORIZONTAL)
       
        self.panel_filtros = wx.Panel(self.panel_principal)
        self.panel_filtros.SetBackgroundColour('#ffffff')
        
        
        self.panel_direita = wx.Panel(self.panel_principal,size=(320,0))
        self.panel_direita.SetBackgroundColour('#000000')
        self.sizer_principal.Add(self.panel_filtros, 1, wx.EXPAND | wx.ALL, 7)      
        self.sizer_principal.Add(self.panel_direita, 0, wx.EXPAND | wx.ALL, 7)    
        self.panel_principal.SetSizer(self.sizer_principal)
        
        
        #self.filter_list("teste")    
        #self.panel = wx.Panel(self.panel_principal)
        #self.filter_list("teste")
        self.filters = {}
        self.filters_edicao = {}
        self.filtros_aplicados = []
        self.player = None
        self.filter_default_list(self.panel_filtros)
        self.Show(True)    
        self.Maximize()
    
    def botoes_pause(self):
        self.toolbar.EnableTool(wx.ID_STOP,False)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS,False)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT,False)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
    def botoes_play(self):
        self.toolbar.EnableTool(wx.ID_STOP, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/pause.png'))
        
    def botoes_edit_preset(self):
        self.toolbar.EnableTool(wx.ID_STOP, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_PREVIOUS, True)
        self.toolbar.EnableTool(wx.ID_PREVIEW_NEXT, True)
        self.toolbar.EnableTool(wx.ID_UPT, False)
        self.toolbar.SetToolNormalBitmap(wx.ID_UP ,wx.Bitmap('images/play.png'))
        
    def OnSavePreset(self, e):
        pass
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
        if self.preset_mode == 1: # Criando um novo preset
            pass
    def OnStop (self, e):
        
        if self.preset_mode == 0:
            self.player.pausar()
            self.botoes_pause()
            self.status = 0
    def OnNext (self, e):
        """
        Função que muda para o próximo filtro do preset atual
        """        
        pass
    def OnPrevious (self, e):
        """
        Função que muda para o filtro anterior do preset atual
        """   
        pass
    def OnNewPreset(self, e):
         if self.status == 1:
             self.player.pausar()
         self.botoes_pause()
         self.status = 0
         
    
    def OnLoadPreset(self, e):
        pass
    
    def filter_default_list(self, panel):
        """
        Cria as listas de filtros padrão com checkbox e 
        """
        box_esquerda = wx.BoxSizer(wx.VERTICAL)
        lista_filtros = filters.Filtro.filtros
        i = 0;
        for name,funcs in lista_filtros.items():
            if i % 2 == 0:            
                panel_de_dois = wx.Panel(panel)
                panel_de_dois.SetBackgroundColour("#EEEEEE")
                sizer_de_dois = wx.BoxSizer(wx.HORIZONTAL)
                box_esquerda.Add(panel_de_dois, 1, wx.EXPAND | wx.ALL, 10)  
                panel_de_dois.SetSizer(sizer_de_dois)
            panel_filtros = wx.Panel(panel_de_dois)
            panel_filtros.SetBackgroundColour("#CCCCCC")
            sizer_de_dois.Add(panel_filtros, 1, wx.EXPAND | wx.RIGHT, wx.LEFT, 5)
            sizer_filtros = wx.BoxSizer(wx.VERTICAL)
            label_lista = wx.StaticText(panel_filtros, label=name)
            sizer_filtros.Add(label_lista, 0, wx.EXPAND | wx.LEFT | wx.TOP, 5)
            panel_filtros.SetSizer(sizer_filtros)
            for func in funcs:
                filtro = func.__func__()
                panel_um = wx.Panel(panel_filtros)     
                sizer_um = wx.BoxSizer(wx.HORIZONTAL)
                check = wx.CheckBox(panel_um,label=filtro.name)
                botao = wx.Button(panel_um,label="Editar")
                sizer_um.Add(check, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 10)
                sizer_um.Add(botao, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 10)
                panel_um.SetSizer(sizer_um)
                check.Bind(wx.EVT_CHECKBOX, self.check_filter)
                botao.Bind(wx.EVT_BUTTON, self.edit_filter)
                sizer_filtros.Add(panel_um, 0, wx.EXPAND | wx.ALL, 12)
                self.filters[check] = filtro.out
                self.filters_edicao[botao] = filtro
            i += 1
        data.load_defaults(self.filters_edicao.values())
        panel.SetSizer(box_esquerda)
    
    def edit_filter (self, e):
        """
        Abre janela para edição dos parâmetros do filtro
        O Filtro está no mapa filters_edicao
        """
        filtro = self.filters_edicao[e.GetEventObject()]
        janela = edit_window(self,e.GetEventObject(),filtro)
        janela.ShowModal()
        janela.Destroy()       
    def check_filter(self, e):
         obj = e.GetEventObject()
         if obj.GetValue():
             self.filtros_aplicados.append(self.filters[obj])
         else:
             self.filtros_aplicados.remove(self.filters[obj])
    #def Modo_Novo
    def filter_list(self, name):
        """
        Create a checkbox filter container.     
        """
        panel =  wx.Panel(self.panel_principal, size=(250,150))
        wx.TextCtrl(panel,pos=(3,3), size=(250,150))


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