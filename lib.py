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
File with some important unrelated classes
"""
import wx
from threading import *
from player import *

# Based on http://stackoverflow.com/questions/4709087/wxslider-with-floating-point-values
class FloatSlider(wx.Slider):
    """
    Class that modifies the Slider class of wx and makes it accept float (instead of only integers) 
    """

    def __init__(self, parent, id=-1, value=0.00, min_val=None, max_val=None, res=1e-4,
                 size=wx.DefaultSize, style=wx.SL_HORIZONTAL,
                 name='floatslider', texto=None):
        self._value = value
        self.defaultValue = float(value)
        self._min = min_val
        self._max = max_val
        self.texto = texto
        self._res = res
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


class DataGen(object):
    """
    Class that generates a list of stream's values
    Used to generate a graph.
    """
    def __init__(self, window):
        self.window = window
    def next(self):
        if self.window.player is not None:
            retorno = self.window.player.last_input_output()      
            return retorno

class MyThread(Thread):
    """
    Graph Thread
    """
    def __init__(self, time, func, window):
        Thread.__init__(self)
        self.stopped = Event()
        self.func = func
        self.time = time
        self.window = window
        self._parar = False
    def run(self):
        while not self.stopped.wait(self.time/1000.0):
           if self._parar:
               return
           self.func(None)
    def stop(self):
        self._parar = True
    def __del__(self):
        self.parar = True
    def start(self):
        if self._parar:
            self.__init__(self.time, self.func, self.window)
        self._parar = False
        Thread.start(self)
        
