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
''' Generic text entry. '''
import pyglet
import cached
import theme
from widget import Widget


class Entry(Widget):
    ''' Text entry. '''

    def __init__(self, text='Entry', on_change=None):
        ''' Create entry. '''

        self._text = text
        self._active = False
        self._label = cached.Label(text = self._text)
        doc = pyglet.text.document.UnformattedDocument(self._text or '')
        self._layout = pyglet.text.layout.IncrementalTextLayout(doc,1,1)
        self._caret = pyglet.text.caret.Caret(self._layout)
        Widget.__init__(self)
        self._focusable = True
        self._activable = True
        self._on_change_callback = on_change
        self.style = theme.Entry



    def _build(self, batch=None, group=None):
        ''' Build entry and add it to batch and group.

        **Parameters**
            `batch` : `Batch`
                Optional graphics batch to add the object to.
            `group` : `Group`
                Optional graphics group to use.
        '''

        Widget._build(self, batch) #, group)
        if self._label:
            self._label.delete()
            self._label = None
        if self._layout:
            self._layout.delete()
            self._layout = None
        if self._caret:
            self._caret.delete()
            self._caret = None

        # Dummy layout creation and deletion seems to make rendering faster
        doc = pyglet.text.document.UnformattedDocument('dummy')
        pyglet.text.layout.IncrementalTextLayout(doc, 1, 1, batch=self._batch).delete()
        if not self._active:
            self._label = cached.Label(text = self._text, multiline=False,
                                       batch=self._batch, group=self._fg_group,
                                       anchor_x='left', anchor_y='top')
        else:
            doc = pyglet.text.document.UnformattedDocument(self._text or '')
            self._layout = pyglet.text.layout.IncrementalTextLayout(
                doc, 1, 1, multiline=False, batch=self._batch, group=self._fg_group)
            self._layout.anchor_x = 'left'
            self._layout.anchor_y = 'top'
            self._caret = pyglet.text.caret.Caret(self._layout)
        self._deleted = False
        self._update_style()
        self._update_state()
        self._update_size()



    def _delete(self):
        ''' Delete entry. '''

        Widget._delete(self)
        if self._label:
            self._label.delete()
            self._label = None
        if self._layout:
            self._layout.delete()
            self._layout = None
        if self._caret:
            self._caret.delete()
            self._caret = None



    def move(self, x, y):
        ''' Move entry to (x,y).

        :Parameters:
            `x` : int
                X coordinate ot the top-left corner
            `y` : int
                Y coordinate ot the top-left corner
        '''
        dx, dy = x-self.x, y-self.y
        Widget.move(self,x,y)
        widget = self._label or self._layout
        if widget:
            widget.x = widget.x+dx
            widget.y = widget.y+dy



    def _update_size(self, propagate=False):
        ''' Update size. '''

        if self._label:
            h = self._label.content_height
        else:
            font = self._layout.document.get_font()
            h = font.ascent-font.descent
        p = self._style.padding
        self._minimum_size = [p[2]+p[3]+96, p[0]+p[1]+h]
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
        if self._deleted:
            return
        Widget._allocate(self, width, height)
        text = self._text
        style = self._style
        padding = style.padding
        content_width = self.width-padding[2]-padding[3]
        content_height = self.height-padding[0]-padding[1]
        label = self._label
        layout = self._layout
        # Dear Glydget, I do not want you to fuck up my content strings. Sincerely, Steve.
        if label and False:
            # Ellipsize text if necessary
            if label.content_width > content_width:
                n,m = 1, len(text)
                while (m-n) > 1:
                    i = (n+m)//2
                    if i < (len(text)-1):
                        label.text = text[:i]+u'…'
                    else:
                        label.text = text
                    if label.content_width < content_width:
                        n = i
                    else:
                        m = i
                if n < (len(text)-2):
                    label.text = text[:n]+u'…'
                else:
                    label.text = text
            label.x = int(self.x+padding[2])
            label.y = int(self.y-padding[0])
        elif layout:
            layout.width = content_width
            layout.height = self._minimum_size[1]
            layout.x = int(self.x+padding[2])
            layout.y = int(self.y-padding[0])



    def _update_state(self):
        ''' Update state. '''

        if self._deleted:
            return
        Widget._update_state(self)
        if self._label:
            self._label.color = self._style.colors[self._state]
        else:
            doc = self._layout.document
            doc.set_style(0, len(doc.text),{
                    'color': self._style.colors[self._state]})
            self._caret.color = self._style.colors[self._state][0:3]



    def _update_style(self):
        ''' Update style. '''

        if self._deleted:
            return
        style = self._style
        if self._label:
            self._label.font_name = style.font_name
            self._label.font_size = style.font_size
            self._label.bold = style.bold
            self._label.italic = style.italic
        elif self._layout:
            doc = self._layout.document
            doc.set_style(0, len(doc.text),
               {'italic':    style.italic,
                'bold':      style.bold,
                'font_name': style.font_name,
                'font_size': style.font_size})
        Widget._update_style(self)



    def activate(self):
        ''' Activate entry. '''

        if not self._activable:
            return

        if not self._active:
            self._active = True
            self._build(self._batch, self._fg_group)
            if not self.parent:
                self._allocate(self.size_request[0],
                                         self.size_request[1])
            else:
                self._allocate(self.width,
                                         self.height)
        Widget.activate(self)



    def deactivate(self):
        ''' Deactivate entry. '''

        if not self._activable:
            return

        if self._active == True:
            self._active = False
            self._build(self._batch, self._fg_group)
            if not self.parent:
                self._allocate(self.size_request[0], self.size_request[1])
            else:
                self._allocate(self.width, self.height)
        Widget.deactivate(self)



    def on_mouse_press(self, x, y, *args):
        Widget.on_mouse_press(self, x, y, *args)
        if self._hit(x,y) and self._caret:
            return self._caret.on_mouse_press(x, y, *args)



    def on_mouse_drag(self, *args):
        if self._caret:
            return self._caret.on_mouse_drag(*args)



    def on_text(self, text):
        if self._caret:
            if text == '\r':
                self._text = self._layout.document.text
                if self._on_change_callback:
                    self._on_change_callback(self)
                self.deactivate()
                return True
            else:
                self._caret.on_text(text)
                return True


    def on_text_motion(self, motion):
        if self._caret:
            self._caret.on_text_motion(motion)
            return True


    def on_text_motion_select(self, motion):
        if self._caret:
            self._caret.on_text_motion_select(motion)
            return True



    def _get_text(self):
        if self._label:
            return self._label.text
        elif self._layout:
            return self._layout.document.text

    def _set_text(self, text):
        self._text = text
        if self._label:
            self._label.text = text
            w,h = self._size_allocation
            self._allocate(w,h)
        elif self._layout:
            self._layout.document.text = text

    text = property(_get_text, _set_text, doc='Text entry')


