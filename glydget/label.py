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
''' Simple text label. '''
import pyglet
import cached
import theme
from widget import Widget


class Label(Widget):
    ''' Simple text label. '''


    def __init__(self, text='Label'):
        ''' Creates label. '''

        self._text = text
        self._label = cached.Label(text = self._text)
        Widget.__init__(self)
        self.style = theme.Label


    def _build(self, batch=None, group=None):
        ''' Build widget and add it to batch and group.

        **Parameters**
            `batch` : `Batch`
                Optional graphics batch to add the object to.
            `group` : `Group`
                Optional graphics group to use.
        '''

        Widget._build(self, batch) #, group)
        self._label.delete()
        self._label = cached.Label(text = self._text, multiline=False,
                                  batch=self._batch, group=self._fg_group,
                                  anchor_x='left', anchor_y='top')
        self._deleted = False
        self._update_style()
        self._update_state()
        self._update_size()


    def _delete(self):
        ''' Delete label. '''

        Widget._delete(self)
        self._label.delete()


    def move(self, x, y):
        ''' Move object to (x,y).

        :Parameters:
            `x` : int
                X coordinate ot the top-left corner
            `y` : int
                Y coordinate ot the top-left corner
        '''
        dx, dy = x-self.x, y-self.y
        Widget.move(self,x,y)
        widget = self._label
        widget.x = widget.x+dx
        widget.y = widget.y+dy


    def _update_size(self, propagate=False):
        ''' Update size. '''

        p = self._style.padding
        self._minimum_size = [p[2]+p[3]+self._label.content_width,
                              p[0]+p[1]+self._label.content_height]
        if self.parent and propagate:
            self.parent._update_size(propagate)
        elif propagate:
            self._allocate(self.size_request[0],
                                     self.size_request[1])



    def _allocate(self, width, height):
        ''' Set size allocation.

        **Parameters**
            `width` : int
                Width in pixels
            `height` : int
                Height  in pixels
        '''
        Widget._allocate(self, width, height)
        if self._deleted:
            return
        label = self._label
        style = self._style
        p = style.padding
        halign = style.halign
        valign = style.valign
        content_width = self.width-p[2]-p[3]
        content_height = self.height-p[0]-p[1]
        label.x = int(self.x+p[2]+(content_width-label.content_width)*halign)
        label.y = int(self.y-p[0]-(content_height-label.content_height)*valign)



    def _update_state(self):
        ''' Update state. '''

        if self._deleted:
            return
        Widget._update_state(self)
        self._label.color = self._style.colors[self._state]


    def _update_style(self):
        ''' Update style.'''

        if self._deleted:
            return
        style = self._style
        self._label.font_name = style.font_name
        self._label.font_size = style.font_size
        self._label.bold = style.bold
        self._label.italic = style.italic
        Widget._update_style(self)



    def _get_text(self):
        return self._label.text

    def _set_text(self, text):
        self._text = text
        self._label.text = text

    text = property(_get_text, _set_text, doc='Displayed text')
