#!/usr/bin/python3

from lab_ui import Ui_MainWindow as gui
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
import sys 

from numpy import log10
from math import sqrt


from tools import clicker_control, basic_tool 
class Hand(basic_tool):
    """
    This is an object that the clicker_control sends its events to. It receives filtered input form the mouse, and manipulates objects and the GUI accordingly 
    """
    def __init__(self, parent=None):
        basic_tool.__init__(self, parent)

        self.parent = parent

        self.selected = None

        self.brush= QtGui.QBrush()
        self.pen = QtGui.QPen()

        self.brush.setStyle(1)
        self.pen.setStyle(1)

        
        self.drawn = {}
    
    def get_under_here( self, event ):
        """
        Return the mass-id of whatever's at the event

        Returns: int or Nonetype 
        """
        loc_x = event.scenePos().x()
        loc_y = event.scenePos().y()

        for mass_id in self.parent.objects:
            mass = self.parent.objects[mass_id]

            if abs(mass.x-loc_x)<5 and abs(mass.y-loc_y)<5:
                return( mass_id )
        

    def primary_mouse_depressed(self, event):
        """
        Called when the primary mouse button, the left button, is pressed

        Basically just selects the mass under the a button, and updates the GUI to show the thing 
        """
        what = self.get_under_here( event )
        self.selected = what
        self.parent.update_gui()

    def primary_mouse_released( self, event ):
        """
        Called when the primary mouse button, the left button, is released

        Same as before. Gets what's under the mouse and updates the Gui to show the mass/position
        """
        self.draw( self.selected )
        self.selected = self.get_under_here( event )
        self.parent.update_gui()

    def primary_mouse_held(self, event ):
        """
        Called when the primary mouse button is held

        If a mass is currently selected, it moves the selected object to the mouse. This implements DRAGGING 
        """
        if self.selected is None:
            return

        where = [event.scenePos().x() , event.scenePos().y() ]
        self.parent.objects[self.selected].x = event.scenePos().x()
        self.parent.objects[self.selected].y = event.scenePos().y()
        self.parent.objects[self.selected].upd_points()
        self.draw( self.selected )
        
        self.parent.update_gui()
        self.parent.update_circle()

    def secondary_mouse_released(self, event):
        """
        Called when the right-click is released

        Deletes whatever is selected preferentially, or alternatively whatever's  under the mouse 
        """
        if self.selected is not None:
            try:
                self.parent.remove( self.selected )   
            except KeyError:
                pass
            self.draw( self.selected )
            self.selected = None
            return
        else:
            where = self.get_under_here(event)
            if where is None:
                return
            else:
                self.parent.remove( where )
                self.draw( where )



    def draw(self, which):
        """
        Redraws the specified object 
        """
        self.brush.setColor( QtGui.QColor( 214,186,109 ))
        self.pen.setColor(QtGui.QColor( 173, 148, 80 ) )

        if which in self.drawn:
            self.parent.scene.removeItem( self.drawn[which] )
            del self.drawn[which]
        
        if which in self.parent.objects:
            obj = self.parent.objects[which]
            
            self.drawn[which] = self.parent.scene.addPolygon( QtGui.QPolygonF( obj.points ), pen= self.pen, brush=self.brush)
            self.drawn[which].setZValue(10)


class Mass:
    """
    A datatype to represent the Masses on the screen
    """
    def __init__(self, x_pos, y_pos, mass):
        self.x = x_pos
        self.y = y_pos
        self.mass = mass
        
        self.size = 5+10*log10(self.mass)
    
        self.points = [None for i in range(4) ]
        self.upd_points()

    def upd_points(self):
        """
        Updates the coordinates of the little square
        """

        self.size = 5+10*log10(self.mass)

        # make the points 
        # I keep them in this type so that they are easier to draw. 
        #    Drawing a QtPolygon takes a list of QtPoints. The F is for float 
        self.points = [ None for i in range(4) ]
        self.points[0]= QtCore.QPointF(self.x+0.5*self.size, self.y+0.5*self.size)     
        self.points[1]= QtCore.QPointF(self.x+0.5*self.size, self.y-0.5*self.size) 
        self.points[3]= QtCore.QPointF(self.x-0.5*self.size, self.y+0.5*self.size) 
        self.points[2]= QtCore.QPointF(self.x-0.5*self.size, self.y-0.5*self.size) 

class main_window(QMainWindow):
    """
    Datatype for the application itself 
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = gui()
        self.ui.setupUi(self)
        
        self.scene = clicker_control( self.ui.graphicsView, self)

        self.hand = Hand(self)
        self.scene._active = self.hand 

        # connect the Screen to the clicker control 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        self.scale = 100. # this is used as an overall scaling factor so that we are dealing in "inches" instead of pixels 

        self.objects = {}


        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.pen.setWidth(5.)
        self.brush.setStyle(0)
        self.pen.setStyle(1)
        self.circle = None
        self.line = None
        self.update_circle()
        


        self.ui.pushButton_3.clicked.connect( self.add_object_but )
        self.ui.pushButton_2.clicked.connect( self.set_obj_but )

    def update_circle(self):
        """
        Updates the circle and the torque line. Redraws them both
        """
        torque = [0., 0.]

        for mass_id in self.objects:
            mass = self.objects[mass_id]
            torque[1] += -1*mass.mass*mass.x
            torque[0] += mass.mass*mass.y

        off = min(sqrt( torque[0]**2 + torque[1]**2 )/1000., 10 )

        if self.circle is not None: 
            self.scene.removeItem( self.circle )
            self.circle = None 

        self.brush.setStyle(1)
        new_color = QtGui.QColor( 255*off/10., 255*(10-off)/10., 0, 100)
        self.brush.setColor( new_color )
        # we need to use weird scaling things like this so the circle is drawn appropriately large compared to where things get placed 
        # also so that the circle is placed centered at the origin 
        self.circle = self.scene.addEllipse( -5*self.scale,-5*self.scale, 10*self.scale, 10.*self.scale, pen=self.pen, brush=self.brush)

        if self.line is not None:
            self.scene.removeItem( self.line )
            self.line = None 

        # the line 
        these = [QtCore.QPointF(0., 0.), QtCore.QPointF( 0.5*torque[0]/self.scale, 0.5*torque[1]/self.scale)]
        self.brush.setStyle(1)

        self.line = self.scene.addPolygon( QtGui.QPolygonF(these), pen=self.pen, brush=self.brush)

        self.circle.setZValue(0)
        self.line.setZValue(1)

    def register( self, new_obj ):
        """
        Adds a new mass to the registered list of masses 
        Finds the smallest unasigned mass ID in this map of 
        (int) -> Mass
        and assigns it
        """
        assert( isinstance( new_obj, Mass))
        
        where = 0 
        while where in self.objects:
            where+=1 

        self.objects[where] = new_obj 
        self.hand.selected = where 
        return(where )

    def remove(self, what):
        """
        Removes the mass from our map

        May raise KeyError 
        """
        del self.objects[what]
        self.update_circle()

    def update_gui(self):
        """
        Updates the GUI according to the Hand's selection
        """
        if self.hand.selected is None:
            self.ui.x_spin.setValue( 0 *2/self.scale)
            self.ui.y_spin.setValue( 0 *2/self.scale)
            self.ui.mass_spin.setValue(10.)
        else:
            obj = self.objects[ self.hand.selected ]
            self.ui.x_spin.setValue( obj.x *2/self.scale)
            self.ui.y_spin.setValue( -obj.y *2/self.scale)
            self.ui.mass_spin.setValue( obj.mass )

    def add_object_but( self ):
        """
        called when the "Place" button is pressed

        Gets the current entries in the spin boxes and uses those to make a new mass 
        """
        new = Mass( self.ui.x_spin.value()*self.scale*0.5, -self.ui.y_spin.value()*self.scale*0.5, self.ui.mass_spin.value())

        where = self.register( new )
        self.hand.draw( where )

        self.update_circle()

    def set_obj_but( self ):
        """
        Called when the "set" button is pressed

        Uses the values of the spin boxes to set the Hand's selection to new values 
        """
        if self.hand.selected is not None:
            this = self.hand.selected
            self.objects[this].x_pos = self.ui.x_spin.value()*self.scale*0.5
            self.objects[this].y_pos = -self.ui.y_spin.value()*self.scale*0.5
            self.objects[this].mass  = self.ui.mass_spin.value()
            self.objects[this].upd_points()
            self.hand.draw( this )
            self.update_circle()


# create an instance of the application and launch it 
app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    app_instance.show()
    sys.exit( app.exec_())
