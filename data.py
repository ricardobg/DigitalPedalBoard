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
File that handles saving and loading data.
It manages the default values and preset files.
"""
import pickle

default_file = "default.data"


def load_preset(preset_file):
    """
    Loads a preset (list of list of filters). 
    Returns None if the file can't be opened.
    """
    try:
        arquivo = open(preset_file,"r")
        preset = pickle.load(arquivo)
        return preset
    except:
        return None


def save_preset(preset_file, preset_list):
    """
    Saves a preset. 
    The paramaters of the preset effects don't interfere on the default values.
    """
    pickle.dump(preset_list,open(preset_file,"w"))



def load_defaults(lista_filtros):
    """
    Reads the default values file, and loads it into the filters.
    """
    try:
        arquivo = open(default_file,"r")
        padroes = pickle.load(arquivo)
        for filtro in lista_filtros:
            if padroes.has_key(filtro.name):
                filtro.vparams = padroes[filtro.name]
    except:
        pass


def salva_defaults(lista_filtros):
    """
    Saves the default values.
    """
    padroes = {}
    for filtro in lista_filtros:
        padroes[filtro.name] = filtro.vparams
    pickle.dump(padroes,open(default_file,"w"))

    