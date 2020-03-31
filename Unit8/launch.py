#!/usr/bin/python3

from lab_gui import Ui_MainWindow as gui
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


from numpy import log10, pi
from math import sqrt

import os 
import sys # used by hacky hacky

# hacky way to import these libs from the parent library
# without having to make this an actual module and fuss around with setting the path variable
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from tools import clicker_control, basic_tool 

"""
A data-taking and visualization tool for UTA's unit 8

Uses my GUI/scene interface code from MultiHex
https://github.com/BenSmithers/MultiHex
"""

class Dimensions:
    """
    Object to contain the dimensions of masses. This implements a little function to get a partial integral over the volume (so you can get displacement)
    """
    def __init__(self, dy):
        assert( isinstance(dy,float) or isinstance( dy, int) )
        self.dy = dy

    def get_integral(self, y):
        """
        Integrate the dx's... kinda needs to go from top to bottom 
        """

        if y<0:
            return(0)
        elif y<self.dy:
            return(1.*y)
        else:
            return(1.*self.dy)


class Cylinder(Dimensions):
    """
    Implements cylindrical dimensions
    """
    def __init__(self, width, dy=1.0):
        Dimensions.__init__(self, dy)
        assert( isinstance(width, float) or isinstance(width, int))

        self.width = width


    def get_integral(self, y):
        """
        Just the volume of a cylinder 
        """
        if y<0:
            return 0
        elif y<=self.dy:
            return (pi*(0.5*self.width)**2)*y
        else:
            return self.volume

    @property
    def volume(self):
        return self.get_integral(self.dy)

class Irregular(Dimensions):
    """
    Implements an irregularly shaped object 
    """
    def __init__(self, width, dy=1.0):
        Dimensions.__init__(self, dy)
        assert( isinstance(width, float) or isinstance(width, int))

        self.width = width


    def get_integral(self, y):
        """
        This was wholly unnecessary.

        It's supposed to be two tubes connected by a truncated cone... "irregular"
        """
        if y<0:
            return 0
        elif y<0.3*self.dy:
            return (pi*(0.5*self.width)**2)*y
        elif y<0.6*self.dy:
            R=0.5*self.width
            return (pi*(0.5*self.width)**2)*(0.3*self.dy) + (1./3)*(y-0.3*self.dy)*(pi*( (0.5*R)**2 + 0.5*R*R + R**2)) 
        elif y<=self.dy:
            R=0.5*self.width
            return (pi*(0.5*self.width)**2)*(0.3*self.dy) + (1./3)*(y-0.3*self.dy)*(pi*( (0.5*R)**2 + 0.5*R*R + R**2)) + (pi*(0.25*self.width)**2)*(0.4*self.dy)
        else:
            return self.volume

    @property
    def volume(self):
        return self.get_integral(self.dy)

class Mass:
    """
    Class for the objects we're moving around. 

    These have mass, dimension, a location, and a color 
    """
    def __init__(self, mass, x,y, color, dimension):
        assert( isinstance( mass,int) or isinstance(mass,float))
        assert( isinstance( x,int) or isinstance(x,float))
        assert( isinstance( y,int) or isinstance(y,float))

        self.mass = mass
        self._x = x
        self._y = y

        assert( isinstance(color,list))
        assert( len(color)==3)
        for item in color:
            assert( isinstance(item, float) or isinstance(item, int) )

        self.color = color

        assert(isinstance(dimension, Dimensions))
        self.dimensions = dimension

    def get_submerged_volume(self, waterlevel):
        """
        Gets amount of fluid displaced based on the masses height and dimensions. Note: volume in scaled coordinates 
        """
        assert(isinstance(waterlevel, float) or isinstance(waterlevel, int))

        if (self.y+self.dimensions.dy) < waterlevel:
            return(0)
        elif self.y>waterlevel:
            # return full volume
            return( self.dimensions.volume )
        else:
            # integrate! 
            return( self.dimensions.get_integral(self.y + self.dimensions.dy- waterlevel ) )

    @property
    def x(self):
        return(self._x)

    @property 
    def y(self):
        return(self._y)

class new_tool(basic_tool):
    """
    Clicker Control interface for moving the masses around, drawing the masses, and getting the apparent force they apply 
    """
    def __init__(self, parent):
        basic_tool.__init__(self, parent)
        self.parent = parent 

        self.selected = None
        self.drawn = {}

        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()


    def primary_mouse_held(self, event):
        if self.selected is not None:
            self.parent.masses[self.selected]._x = event.scenePos().x()
            self.parent.masses[self.selected]._y = event.scenePos().y()
            self.draw(self.selected) 

            vol = self.parent.masses[self.selected].get_submerged_volume(self.parent.waterlevel)
            vol /= (self.parent.scale_factor**3)

            displaced_fluid = vol*self.parent.water_density*9.80

            self.parent.ui.force_lbl.setText("{:.2f} N".format (self.parent.masses[self.selected].mass*9.80 - displaced_fluid ))


    def primary_mouse_depressed(self, event):
        here = [event.scenePos().x(), event.scenePos().y() ]

        for obj in self.parent.masses:
            if abs(self.parent.masses[obj].x - here[0])<10.0 and abs(self.parent.masses[obj].y - here[1])<10.0:
                self.selected = obj
                return

        self.selected = None
        self.parent.ui.force_lbl.setText("0.0 N")

    def draw(self, which):
        if which in self.drawn:
            self.parent.scene.removeItem( self.drawn[which])
            del self.drawn[which]

        try:
            obj = self.parent.masses[which]
        except KeyError:
            return


        self.pen.setStyle(1)
        self.brush.setStyle(1)
        self.pen.setColor(QtGui.QColor(obj.color[0], obj.color[1], obj.color[2]))
        self.brush.setColor(QtGui.QColor(obj.color[0], obj.color[1], obj.color[2]))

        # hacky way to draw the cylinders and irregularly shaped thing 
        if isinstance(obj.dimensions, Cylinder):
            points = [ None for i in range(4) ]
            points[0]= QtCore.QPointF(obj.x-0.5*obj.dimensions.width,obj.y)     
            points[1]= QtCore.QPointF(obj.x-0.5*obj.dimensions.width, obj.y+obj.dimensions.dy) 
            points[2]= QtCore.QPointF(obj.x+0.5*obj.dimensions.width, obj.y+obj.dimensions.dy) 
            points[3]= QtCore.QPointF(obj.x+0.5*obj.dimensions.width, obj.y)

        else:
            points = [ None for i in range(8) ]
            points[0]= QtCore.QPointF(obj.x-0.5*obj.dimensions.width,obj.y)
            points[1]= QtCore.QPointF(obj.x-0.5*obj.dimensions.width, obj.y + obj.dimensions.dy*0.3)
            points[2]= QtCore.QPointF(obj.x-0.25*obj.dimensions.width, obj.y + obj.dimensions.dy*0.6)
            points[3]= QtCore.QPointF(obj.x-0.25*obj.dimensions.width, obj.y + obj.dimensions.dy)
            points[4]= QtCore.QPointF(obj.x+0.25*obj.dimensions.width, obj.y + obj.dimensions.dy)
            points[5]= QtCore.QPointF(obj.x+0.25*obj.dimensions.width, obj.y + obj.dimensions.dy*0.6)
            points[6]= QtCore.QPointF(obj.x+0.5*obj.dimensions.width, obj.y + obj.dimensions.dy*0.3)
            points[7]= QtCore.QPointF(obj.x+0.5*obj.dimensions.width, obj.y)

        self.drawn[which] = self.parent.scene.addPolygon( QtGui.QPolygonF( points ), pen=self.pen, brush=self.brush)
        self.drawn[which].setZValue(10)

class main_window(QMainWindow):
    """
    Datatype for the application itself 
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = gui()
        self.ui.setupUi(self)
        

        self.scene = clicker_control( self.ui.graphicsView, self)
       
        self.scene._active = new_tool(self)

        #connect the Screen to the clicker control 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()

        self.waterlevel = 500. # y-level to draw the fluid (goo)

        self.scale_factor = 1000. # so that the objects aren't really really really tiny 
        # scale factor is px/meter 
        basic =Cylinder(self.scale_factor*0.0255,self.scale_factor*0.0446)
        weird = Irregular(self.scale_factor*0.0255,self.scale_factor*0.0446)

        self.masses = { 0: Mass(0.1912, 100,100, [36, 31, 105],basic),
                        1: Mass(0.0619, 150,100,[212, 142, 61],basic),
                        2: Mass(0.1751, 200,100,[32, 27, 36],basic),
                        3: Mass(0.0949, 250,100,[149, 149, 158],weird)
                        }

        self.water_color = (66, 135, 245)
        self.water_density = 1000.

        self.drawn_water = None
        self.drawn_bowl = None

        self.combo_index_change()
        self.draw_waterline()

        self.ui.fluid_box.currentIndexChanged.connect( self.combo_index_change )
     
        for mass in self.masses:
            self.scene._active.draw(mass)


    def draw_waterline(self):
        """
        Draws both the cup and the water (or goo)
        """
        # draw a line to contain the water
        self.pen.setWidth(5)
        self.pen.setColor(QtGui.QColor(0,0,0))


        points = [QtCore.QPointF(250, 450),QtCore.QPointF(250, 800), QtCore.QPointF(650, 800),QtCore.QPointF(650, 450) ]

        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF(points))

        if self.drawn_bowl is not None:
            self.scene.removeItem(self.drawn_bowl)
        if self.drawn_water is not None:
            self.scene.removeItem(self.drawn_water)

        self.pen.setStyle(1)
        self.brush.setStyle(0)
        self.drawn_bowl = self.scene.addPath( path, pen=self.pen, brush=self.brush)
        self.drawn_bowl.setZValue(2)

        self.pen.setStyle(0)
        self.brush.setStyle(1)
        points = [QtCore.QPointF(250, self.waterlevel),QtCore.QPointF(250, 800), QtCore.QPointF(650, 800),QtCore.QPointF(650, self.waterlevel) ]
        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF(points))
        self.brush.setColor(QtGui.QColor(self.water_color[0],self.water_color[1],self.water_color[2]))

        self.drawn_water = self.scene.addPath( path, pen=self.pen, brush=self.brush)


    def combo_index_change(self):
        """
        Called when the user checks a new option in the drop-down menu 
        """
        this_sub = self.ui.fluid_box.currentText()

        if this_sub == "Water":
            self.water_density = 1000.
            self.water_color = (66, 135, 245)
        elif this_sub == "Air":
            self.water_density = 0.
            self.water_color = (255, 255, 255)
        else:
            self.water_density = 1234.
            self.water_color = (103, 191, 137)

        self.draw_waterline()

        

        
# create an instance of the application and launch it 
app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    app_instance.show()
    sys.exit( app.exec_())

