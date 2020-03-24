#!/usr/bin/python3

from lab_ui import Ui_MainWindow as gui
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
import sys 

from numpy import log10
from math import sqrt


from tools import clicker_control, basic_tool 
class Hand(basic_tool):    
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
        loc_x = event.scenePos().x()
        loc_y = event.scenePos().y()

        for mass_id in self.parent.objects:
            mass = self.parent.objects[mass_id]

            if abs(mass.x-loc_x)<5 and abs(mass.y-loc_y)<5:
                return( mass_id )
        

    def primary_mouse_depressed(self, event):
        what = self.get_under_here( event )
        self.selected = what
        self.parent.update_gui()

    def primary_mouse_released( self, event ):
        self.draw( self.selected )
        self.selected = self.get_under_here( event )
        self.parent.update_gui()

    def primary_mouse_held(self, event ):
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
        if self.selected is not None:
            try:
                self.parent.remove( self.selected )    
            except KeyError:
                pass
        
            self.draw( self.selected )
            return
        else:
            where = self.get_under_here(event)
            self.parent.remove( where )
            self.draw( where )



    def draw(self, which):
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
    def __init__(self, x_pos, y_pos, mass):
        self.x = x_pos
        self.y = y_pos
        self.mass = mass
        
        self.size = 5+10*log10(self.mass)
    
        self.points = [None for i in range(4) ]
        self.upd_points()

    def upd_points(self):

        self.size = 5+10*log10(self.mass)

        # make the points 
        self.points = [ None for i in range(4) ]
        self.points[0]= QtCore.QPointF(self.x+0.5*self.size, self.y+0.5*self.size)     
        self.points[1]= QtCore.QPointF(self.x+0.5*self.size, self.y-0.5*self.size) 
        self.points[3]= QtCore.QPointF(self.x-0.5*self.size, self.y+0.5*self.size) 
        self.points[2]= QtCore.QPointF(self.x-0.5*self.size, self.y-0.5*self.size) 

class main_window(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = gui()
        self.ui.setupUi(self)
        
        self.scene = clicker_control( self.ui.graphicsView, self)

        self.hand = Hand(self)
        self.scene._active = self.hand 

        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        self.scale = 100.

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
        self.circle = self.scene.addEllipse( -5*self.scale,-5*self.scale, 10*self.scale, 10.*self.scale, pen=self.pen, brush=self.brush)

        if self.line is not None:
            self.scene.removeItem( self.line )
            self.line = None
        
        these = [QtCore.QPointF(0., 0.), QtCore.QPointF( 0.5*torque[0]/self.scale, 0.5*torque[1]/self.scale)]
        self.brush.setStyle(1)

        self.line = self.scene.addPolygon( QtGui.QPolygonF(these), pen=self.pen, brush=self.brush)

        self.circle.setZValue(0)
        self.line.setZValue(1)

    def register( self, new_obj ):
        assert( isinstance( new_obj, Mass))
        
        where = 0 
        while where in self.objects:
            where+=1 

        self.objects[where] = new_obj 
        self.hand.selected = where 
        return(where )

    def remove(self, what):
        del self.objects[what]
        self.update_circle()

    def update_gui(self):
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
        new = Mass( self.ui.x_spin.value()*self.scale*0.5, -self.ui.y_spin.value()*self.scale*0.5, self.ui.mass_spin.value())

        where = self.register( new )
        self.hand.draw( where )

        self.update_circle()

    def set_obj_but( self ):
        if self.hand.selected is not None:
            this = self.hand.selected
            self.objects[this].x_pos = self.ui.x_spin.value()*self.scale*0.5
            self.objects[this].y_pos = -self.ui.y_spin.value()*self.scale*0.5
            self.objects[this].mass  = self.ui.mass_spin.value()
            self.objects[this].upd_points()
            self.hand.draw( this )
            self.update_circle()

app = QApplication(sys.argv)
app_instance = main_window()


if __name__=="__main__":
    app_instance.show()
    sys.exit( app.exec_())
