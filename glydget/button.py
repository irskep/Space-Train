#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# glydget - an OpenGL widget toolkit
# Copyright (c) 2009 - Nicolas P. Rougier
#
# This file is part of glydget.
#
# glydget is free software: you can  redistribute it and/or modify it under the
# terms of  the GNU General  Public License as  published by the  Free Software
# Foundation, either  version 3 of the  License, or (at your  option) any later
# version.
#
# glydget is  distributed in the hope that  it will be useful,  but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy  of the GNU General Public License along with
# glydget. If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
''' Text button.

The Button widget is displayed as a push button with a text label. The Button is
generally used to attach a method that is called when the button is clicked.
'''
from label import Label
import theme


class Button(Label):
    ''' Text button. '''

    def __init__(self, text='Label', on_click=None):
        ''' Creates button. '''

        Label.__init__(self, text)
        self._focusable = True
        self._activable = True
        self._on_click = on_click
        self.style = theme.Button



    def activate(self):
        ''' Activate button. '''

        Label.activate(self)
        if self._on_click:
            self._on_click(self)
        self.deactivate()
