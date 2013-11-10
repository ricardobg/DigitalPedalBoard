# -*- coding: utf-8 -*-
"""
File to handle data.
It handles user and filter settings.
"""

import pickle
arquivo_default = "default.data"


def load_preset(preset_file):
    """
    Carrega um preset, retorna None se não encontrar o arquivo ou arquivo inválido.
    As configurações do preset (parametros dos filtros) são salvas tambem
    e não interferem nos defaults dos filtros.
    """
    try:
        arquivo = open(preset_file,"r")
        preset = pickle.load(arquivo)
        return preset
    except:
        return None


def save_preset(preset_file, preset_list):
    """
    Salva um preset
    """
    pickle.dump(preset_list,open(preset_file,"w"))



def load_defaults(lista_filtros):
    """
    Lê a lista
    """
    try:
        arquivo = open(arquivo_default,"r")
        padroes = pickle.load(arquivo)
        for filtro in lista_filtros:
            if padroes.has_key(filtro.name):
                filtro.vparams = padroes[filtro.name]
                filtro.update_default()
    except:
        pass


def salva_defaults(lista_filtros):
    """
    Função que salva um mapa contendo o nome do filtro e uma lista dos valores padrão dos filtros
    """
    padroes = {}
    for filtro in lista_filtros:
        padroes[filtro.name] = filtro.vparams
    pickle.dump(padroes,open(arquivo_default,"w"))

    