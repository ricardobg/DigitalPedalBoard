# -*- coding: utf-8 -*-
"""
File to create windows and widgets

"""
import data
import filters
import wx
import player

def sair(e):
    window.Close()

class edit_window (wx.Dialog):
     def __init__(self, filtro):
        super(edit_window, self).__init__(None) 
        self.filtro = filtro
        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle(filtro.name)
     def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label=u'Parâmetros')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        sbs.Add(wx.RadioButton(pnl, label='256 Colors', 
            style=wx.RB_GROUP))
        sbs.Add(wx.RadioButton(pnl, label='16 Colors'))
        sbs.Add(wx.RadioButton(pnl, label='2 Colors'))
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        hbox1.Add(wx.RadioButton(pnl, label='Custom'))
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
        sbs.Add(hbox1)
        
        pnl.SetSizer(sbs)
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, 
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
   
     def OnClose(self, e): 
        self.Destroy()
    
class main_window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(main_window, self).__init__(*args, **kwargs) 
        self.InitUI()
        
    def InitUI(self):    
        # Cria o menu       
        #self.SetScrollbar(wx.VERTICAL, 0, 16, 50)
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
        
        
        # Status do player 0-Parado,1-Tocando,2-Pausado
        self.status = 0        
        
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


        #Cria os panels que contem os filtros
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
    def OnQuit(self, e):
        if self.player is not None and not self.player.player.finished:
            self.player.pausar()
    
    def OnPlayPause (self, e):
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

    def OnStop (self, e):
        
        
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
        pass
    
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
        panel.SetSizer(box_esquerda)
    
    def edit_filter (self, e):
        """
        Abre janela para edição dos parâmetros do filtro
        O Filtro está no mapa filters_edicao
        """
        filtro = self.filters_edicao[e.GetEventObject()]
        janela = edit_window(filtro)
        janela.ShowModal()
        janela.Destroy()       
    def check_filter(self, e):
         obj = e.GetEventObject()
         if obj.GetValue():
             self.filtros_aplicados.append(self.filters[obj])
         else:
             self.filtros_aplicados.remove(self.filters[obj])
    def filter_checkbox(check_list, name, func_onclick):
        """
        Create the checkbox    
        """
        mycheck = wx.CheckBox(check_list, label=name)
        
        pass
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