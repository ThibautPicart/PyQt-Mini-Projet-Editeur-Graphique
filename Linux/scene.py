#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QT_VERSION_STR

class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self,parent=None) :
        QtWidgets.QGraphicsScene.__init__(self)
        self.tool='move'
        self.begin,self.end,self.offset=QtCore.QPoint(0,0),QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.item=None
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(3)
        self.brush=QtGui.QBrush(QtCore.Qt.blue)
        self.widget=None
        self.font=None
        self.drawing=False
        self.line=None
        self.rect=None
        self.ellipse=None
        self.penwidth=3
        self.pencolor=QtCore.Qt.red
        self.penline=1
        self.brushcolor=QtCore.Qt.green
        self.brushstyle=1

        #polygon
        self.polyLines=[]
        self.polygon=[]
        self.polyRects=[]
       

        #Save
        self.lines={}
        self.lines["number"]=0
        self.rects={}
        self.rects["number"]=0
        self.ellipses={}
        self.ellipses["number"]=0
        self.texts={}
        self.texts["number"]=0
        self.polygons={}
        self.polygons["number"]=0


    def set_tool(self, widget, tool) :
        self.widget=widget
        self.tool=tool

    def set_pen_color(self,color) :
        self.pen.setColor(color)
        self.pencolor=color

    def set_pen_line(self, line) :
        self.pen.setStyle(line)
        self.penline=line


    def set_pen_width(self, width) :
        self.pen.setWidth(width)
        self.penwidth=width



    def set_brush_color(self,color) :
        self.brush.setColor(color)
        self.brushcolor=color
 
    def set_brush_style(self, style) :
        self.brush.setStyle(style)
        self.brushstyle=style

    def set_text_font(self, font) :
        self.font=font

    def mousePressEvent(self, event):
        self.begin = self.end = event.scenePos()
        self.item=self.itemAt(self.begin,QtGui.QTransform())
        if self. item :
            if self.tool=='erase' :
                self.removeItem(self.item)                
             
            elif self.tool=="move" :
                self.offset =self.begin-self.item.pos()

        elif self.tool=='rectangle' :
            self.rect=QtWidgets.QGraphicsRectItem(self.begin.x(),self.begin.y(), 0, 0)

        elif self.tool=='ellipse' :
            self.ellipse=QtWidgets.QGraphicsEllipseItem(self.begin.x(),self.begin.y(), 0, 0)

        elif self.tool=='line' :
            self.line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(),self.end.x(), self.end.y())

        elif self.tool=='polygon':
            c=event.scenePos()
            self.polyRects.append(QtWidgets.QGraphicsRectItem(c.x()-10,c.y()-10,20,20))
            self.addItem(self.polyRects[-1])
            self.polygon.append(c)



                
    def mouseMoveEvent(self, event):
        # print("Scene.mouseMoveEvent()")
        self.end = event.scenePos()
        width=self.end.x()-self.begin.x()
        height=self.end.y()-self.begin.y()

        if self.item  and self.tool=="move":

            self.item.setPos(event.scenePos() - self.offset)


        if self.tool=='rectangle' :
            self.removeItem(self.rect)
            self.rect=QtWidgets.QGraphicsRectItem(self.begin.x(),self.begin.y(), width, height)
            self.rect.setPen(self.pen)
            self.rect.setBrush(self.brush)
            self.addItem(self.rect)

        elif self.tool=='ellipse' :
            self.removeItem(self.ellipse)
            self.ellipse=QtWidgets.QGraphicsEllipseItem(self.begin.x(),self.begin.y(), width, height)
            self.ellipse.setPen(self.pen)
            self.ellipse.setBrush(self.brush)
            self.addItem(self.ellipse)

        elif self.tool=='line' :
            self.removeItem(self.line)
            self.line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(),self.end.x(), self.end.y())
            self.line.setPen(self.pen)
            self.addItem(self.line)



    def mouseDoubleClickEvent(self, event) :
        if(self.tool=='polygon') :
            qpoly=QtGui.QPolygonF(self.polygon)
            qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
            qgpoly.setPen(self.pen)
            qgpoly.setBrush(self.brush)
            self.addItem(qgpoly)
            self.addPoly()
            del self.polygon[:]
            for i in range(len(self.polyRects)) :
                self.removeItem(self.polyRects[i])
            del self.polyRects[:]



        

 
    def mouseReleaseEvent(self, event):
        print("Scene.mouseReleaseEvent()",self.tool)
        self.end = event.scenePos()
        x=self.begin.x()
        y=self.begin.y()
        width=self.end.x()-self.begin.x()
        height=self.end.y()-self.begin.y()
        if self.item and self.tool=="move":
            print(" item ")
            self.item.setPos(event.scenePos() - self.offset)
#            self.item.ungrabMouse()
            self.item=None
        if self.tool=='line' :
            #self.setMouseTracking(False)
            self.addLine(x, y, self.end.x(), self.end.y())
            self.line=None
        elif self.tool=='rectangle' :
            self.addRectangle(x, y, width, height)
            self.rect=None
        elif self.tool=='ellipse' :
            self.addEllipse(x, y, width, height)
            self.ellipse=None
        elif self.tool=='text' :
            t,ok = QtWidgets.QInputDialog.getText(self.widget,"Set Text","Enter text:")
            if ok :
                text=QtWidgets.QGraphicsTextItem(t)
                if self.font :
                    text.setFont(self.font)
                    print("Chosen font -> ",self.font)
                text.setPos(x,y)
                self.addItem(text)
                self.addText(t, x, y, self.font)




    def addLine(self, bx, by, ex, ey) :
        n=str(self.lines["number"])
        self.lines[n+"bx"] = bx 
        self.lines[n+"by"] = by
        self.lines[n+"ex"] = ex
        self.lines[n+"ey"] = ey
        self.lines[n+"color"] = self.pencolor
        self.lines[n+"width"] = self.penwidth
        self.lines[n+"penline"] = self.penline
        self.lines["number"]+=1
      

    def addRectangle(self, x, y, w, h) :
        n=str(self.rects["number"])
        self.rects[n+"x"] = x
        self.rects[n+"y"] = y
        self.rects[n+"w"] = w
        self.rects[n+"h"] = h
        self.rects[n+"color"] = self.pencolor
        self.rects[n+"width"] = self.penwidth
        self.rects[n+"penline"] = self.penline
        self.rects[n+"brushcolor"] = self.brushcolor
        self.rects[n+"brushstyle"] = self.brushstyle
        self.rects["number"]+=1

    def addEllipse(self, x, y, w, h) :
        n=str(self.ellipses["number"])
        self.ellipses[n+"x"] = x
        self.ellipses[n+"y"] = y
        self.ellipses[n+"w"] = w
        self.ellipses[n+"h"] = h
        self.ellipses[n+"color"] = self.pencolor
        self.ellipses[n+"width"] = self.penwidth
        self.ellipses[n+"penline"] = self.penline
        self.ellipses[n+"brushcolor"] = self.brushcolor
        self.ellipses[n+"brushstyle"] = self.brushstyle
        self.ellipses["number"]+=1

    def addText(self, t, x, y, font) :
        n=str(self.texts["number"])
        self.texts[n+"t"] = t
        self.texts[n+"x"] = x
        self.texts[n+"y"] = y
        #self.texts[n+"font"] = font
        self.texts["number"]+=1

    def addPoly(self) :
        n=str(self.polygons["number"])
        for i in range(len(self.polygon)) :
            self.polygons[n+str(i)+"x"]=self.polygon[i].x()
            self.polygons[n+str(i)+"y"]=self.polygon[i].y()
        self.polygons[n+"points"]=len(self.polygon)
        self.polygons[n+"color"] = self.pencolor
        self.polygons[n+"width"] = self.penwidth
        self.polygons[n+"penline"] = self.penline
        self.polygons[n+"brushcolor"] = self.brushcolor
        self.polygons[n+"brushstyle"] = self.brushstyle
        self.polygons["number"]+=1


        


        


    def loadFile(self, items) :
        #lines
        nLines = items[0]["number"]
        for i in range(nLines) :
            bx = items[0][str(i)+"bx"]
            by = items[0][str(i)+"by"]
            ex = items[0][str(i)+"ex"]
            ey = items[0][str(i)+"ey"]
            self.line=QtWidgets.QGraphicsLineItem(bx,by,ex,ey)
            self.set_pen_width(items[0][str(i)+"width"])
            self.set_pen_color(items[0][str(i)+"color"]) 
            self.set_pen_line(items[0][str(i)+"penline"])
            self.line.setPen(self.pen)
            self.addItem(self.line)
            self.line=None

        #Rects
        nRects = items[1]["number"]
        for i in range(nRects) :
            x = items[1][str(i)+"x"]
            y = items[1][str(i)+"y"]
            w = items[1][str(i)+"w"]
            h = items[1][str(i)+"h"]
            self.rect=QtWidgets.QGraphicsRectItem(x,y,w,h)
            self.set_pen_width(items[1][str(i)+"width"])
            self.set_pen_color(items[1][str(i)+"color"]) 
            self.set_pen_line(items[1][str(i)+"penline"])
            self.set_brush_style(items[1][str(i)+"brushstyle"])
            self.set_brush_color(items[1][str(i)+"brushcolor"])
            self.rect.setPen(self.pen)
            self.rect.setBrush(self.brush)
            self.addItem(self.rect)
            self.rect=None

        #Ellipses
        nEllipses = items[2]["number"]
        for i in range(nEllipses) :
            x = items[2][str(i)+"x"]
            y = items[2][str(i)+"y"]
            w = items[2][str(i)+"w"]
            h = items[2][str(i)+"h"]
            self.ellipse=QtWidgets.QGraphicsEllipseItem(x,y,w,h)
            self.set_pen_width(items[2][str(i)+"width"])
            self.set_pen_color(items[2][str(i)+"color"]) 
            self.set_pen_line(items[2][str(i)+"penline"])
            self.set_brush_style(items[2][str(i)+"brushstyle"])
            self.set_brush_color(items[2][str(i)+"brushcolor"])
            self.ellipse.setPen(self.pen)
            self.ellipse.setBrush(self.brush)
            self.addItem(self.ellipse)
            self.ellipse=None

        #Texts
        nTexts = items[3]["number"]
        for i in range(nTexts) :
            t = items[3][str(i)+"t"]
            x = items[3][str(i)+"x"]
            y = items[3][str(i)+"y"]
            #font = items[3][str(i)+"font"]
            text=QtWidgets.QGraphicsTextItem(t)
            # if(font) :
            #     text.setFont(font)
            text.setPos(x,y)
            self.addItem(text)

        #Polygons
        nPolys = items[4]["number"]
        for i in range(nPolys) :
            polygon=[]
            for p in range(items[4][str(i)+"points"]) :
                polygon.append(QtCore.QPointF(items[4][str(i)+str(p)+"x"], items[4][str(i)+str(p)+"y"]))
                qpoly=QtGui.QPolygonF(polygon)
                qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
                self.set_pen_width(items[4][str(i)+"width"])
                self.set_pen_color(items[4][str(i)+"color"]) 
                self.set_pen_line(items[4][str(i)+"penline"])
                self.set_brush_style(items[4][str(i)+"brushstyle"])
                self.set_brush_color(items[4][str(i)+"brushcolor"])
                qgpoly.setPen(self.pen)
                qgpoly.setBrush(self.brush)
                self.addItem(qgpoly)

