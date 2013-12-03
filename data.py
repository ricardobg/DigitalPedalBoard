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
Arquivo para gerenciar o salvamento e carregamento de dados
Gerencia valores padrão e também arquivos de preset
"""

import pickle

arquivo_default = "default.data"


def load_preset(preset_file):
    """
    Carrega um preset, retorna None se não encontrar o arquivo ou arquivo inválido.
    As configurações do preset (parametros dos filtros) são salvas também
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
    Lê a lista de Defaults, carregando os filtros com os padrões
    """
    try:
        arquivo = open(arquivo_default,"r")
        padroes = pickle.load(arquivo)
        for filtro in lista_filtros:
            if padroes.has_key(filtro.name):
                filtro.vparams = padroes[filtro.name]
                #filtro.update_default()
    except:
        pass


def salva_defaults(lista_filtros):
    """
    Função que salva os valores default
    """
    padroes = {}
    for filtro in lista_filtros:
        padroes[filtro.name] = filtro.vparams
    pickle.dump(padroes,open(arquivo_default,"w"))

    