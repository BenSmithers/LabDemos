from PyQt5.QtWidgets import QGraphicsScene, QGraphicsDropShadowEffect
from PyQt5 import QtGui, QtCore



"""
This code is borrowed from my MultiHex library. Check it out!

https://github.com/BenSmithers/MultiHex
"""

import os # used for some of the icons

from math import sqrt, pi
rthree =  sqrt(3)

class basic_tool:
    """
    Prototype a basic tool 
    """
    def __init__(self, parent=None):
        pass
    def primary_mouse_depressed(self,event):
        """
        Called when the right mouse button is depressed 

        @param event 
        """
        pass
    def primary_mouse_released(self, event):
        """
        This is called when the right mouse button is released from a localized click. 

        @param event - location of release
        """
        pass
    def primary_mouse_held(self,event ):
        """
        Called continuously while the right mouse button is moved and depressed 

        @param event - current mouse location
        @param setp  - vector pointing from last called location to @place
        """
        pass
    def secondary_mouse_held(self, event):
        """
        Called continuously while the right mouse button is moved and depressed 
        """
        pass
    def secondary_mouse_released(self, event ):
        """
        Left click released event, used to select something

        @param event - Qt event object. has where the mouse is
        """
        pass
    def mouse_moved(self, event):
        """
        Called continuously while the mouse is in the widget

        @param place - where the mouse is 
        """
        pass
    def drop(self):
        """
        Called when this tool is being replaced. Cleans up anything it has drawn and should get rid of (like, selection circles). This is needed when closing one of the guis 
        """
        pass
    def toggle_mode(self, force=None):
        """
        Toggles the 'mode' of the tool. Optionally passed a 'corce' argument 
        """
        pass

    def clear(self):
        """
        Called when parent window is closing. Clears list of drawn items 
        """
        pass 
    def __str__(self):
        return("BasicTool of type {}".format(type(self)))


class clicker_control(QGraphicsScene):
    """
    Manages the mouse interface for to the canvas.
    """
    def __init__(self, parent=None, master=None):
        QGraphicsScene.__init__(self, parent)

        self._active = None #basic_tool object
        self._primary_held = False
        self._secondary_held = False
        
        self.parent = parent
        self.master = master

        self._alt_held = False

        self._primary = QtCore.Qt.LeftButton
        self._secondary = QtCore.Qt.RightButton

    def keyPressEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = True
    def keyReleaseEvent(self, event):
        event.accept()
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_held = False

        if event.key() == QtCore.Qt.Key_Plus or event.key()==QtCore.Qt.Key_PageUp or event.key()==QtCore.Qt.Key_BracketRight:
            self.parent.scale( 1.05, 1.05 )

        if event.key() == QtCore.Qt.Key_Minus or event.key()==QtCore.Qt.Key_PageDown or event.key()==QtCore.Qt.Key_BracketLeft:
            self.parent.scale( 0.95, 0.95 )


    def mousePressEvent(self, event):
        """
        Called whenever the mouse is pressed within its bounds (The drawspace)
        """
        if event.button()==self._primary:
            event.accept() # accept the event
            self._primary_held = True # say that the mouse is being held 
            self._active.primary_mouse_depressed( event )
        elif event.button()==self._secondary:
            event.accept()
            self._secondary_held = True

    def mouseReleaseEvent( self, event):
        """
        Called when a mouse button is released 
        """
        if event.button()==self._primary:
            # usually a brush event 
            event.accept()
            self._primary_held = False
            self._active.primary_mouse_released(event)

        elif event.button()==self._secondary:
            # usually a selection event
            event.accept()
            self._secondary_held = False
            self._active.secondary_mouse_released( event )

   #mouseMoveEvent 
    def mouseMoveEvent(self,event):
        """
        called continuously as the mouse is moved within the graphics space. The "held" boolean is used to distinguish between regular moves and click-drags 
        """
        event.accept()
        if self._primary_held:
            self._active.primary_mouse_held( event )
        if self._secondary_held:
            self._active.secondary_mouse_held( event )
 
        self._active.mouse_moved( event )


    # in c++ these could've been templates and that would be really cool 
    def to_hex(self):
        """
        We need to switch over to calling the writer control, and have the selector clean itself up. These two cleaners are used to git rid of any drawn selection outlines 
        """
        self._active.drop()
        self._active = self.master.writer_control

    def to_region(self):
        """
        same...
        """
        self._active.drop()
        self._active = self.master.region_control

