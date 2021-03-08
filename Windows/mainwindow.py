#!/usr/bin/python
# -*- coding: utf-8 -*-

### Author : Thibaut Picart ###

#import APIs
import os,sys,json, pickle
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QT_VERSION_STR, Qt

# import my files
from scene import Scene
from  save_load import save, load



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        #self.resize(500, 300)
        self.setWindowTitle("Graphic Editor v0.6")
        self.create_scene()
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        

    def create_scene(self) :
        view=QtWidgets.QGraphicsView()
        self.scene=Scene(self)
        view.setScene(self.scene)
        self.setCentralWidget(view)

    def create_actions(self) :
        #### FILE ####

        #New
        self.action_new = QtWidgets.QAction(
            QtGui.QIcon('../icons/new.png'), 'New', self)
        self.action_new.setShortcut('Ctrl+N')
        self.action_new.setStatusTip('New file')

        #Open
        self.action_open = QtWidgets.QAction(
            QtGui.QIcon('../icons/open.png'), 'Open', self)
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.setStatusTip('Open file')

        #Save
        self.action_save = QtWidgets.QAction(QtGui.QIcon('../icons/save.png'), 'Save', self)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.setStatusTip('Save to file')

        #Save as
        self.action_save_as = QtWidgets.QAction(QtGui.QIcon('../icons/save_as.png'), 'Save As', self)
        self.action_save_as.setShortcut("Shift+Ctrl+S")
        self.action_save_as.setStatusTip('Save as')

        #Exit
        self.action_exit = QtWidgets.QAction(QtGui.QIcon('../icons/exit.png'), 'Exit', self)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.setStatusTip('Exit application')

        #### TOOLS ####

        #Move
        self.action_move = QtWidgets.QAction(QtGui.QIcon('../icons/move.png'),self.tr("&Move"),self)
        self.action_move.setShortcut('Ctrl+M')
        self.action_move.setCheckable(True)
        self.action_move.setChecked(True)

        #Line
        self.action_line = QtWidgets.QAction(QtGui.QIcon('../icons/tool_line.png'),self.tr("&Line"), self)
        self.action_line.setShortcut('Ctrl+L')
        self.action_line.setCheckable(True)
        self.action_line.setChecked(False)

        #Rectangle
        self.action_rectangle = QtWidgets.QAction(QtGui.QIcon('../icons/tool_rectangle.png'),self.tr("&Rectangle"), self)
        self.action_rectangle.setShortcut('Ctrl+R')
        self.action_rectangle.setCheckable(True)
        self.action_rectangle.setChecked(False)

        #Ellipse
        self.action_ellipse = QtWidgets.QAction(QtGui.QIcon('../icons/tool_ellipse.png'),self.tr("&Ellipse"), self)
        self.action_ellipse.setShortcut('Ctrl+E')
        self.action_ellipse.setCheckable(True)
        self.action_ellipse.setChecked(False)

        #Polygon
        self.action_polygon = QtWidgets.QAction(QtGui.QIcon('../icons/tool_polygon.png'),self.tr("&Polygon"), self)
        self.action_polygon.setShortcut('Ctrl+P')
        self.action_polygon.setCheckable(True)
        self.action_polygon.setChecked(False)

        #Text
        self.action_text = QtWidgets.QAction(QtGui.QIcon('../icons/tool_text.png'),self.tr("&Text"), self)
        self.action_text.setShortcut('Ctrl+T')
        self.action_text.setCheckable(True)
        self.action_text.setChecked(False)

        #Erase
        self.action_erase = QtWidgets.QAction(QtGui.QIcon('../icons/clear.png'),self.tr("Erase"), self)
        self.action_erase.setCheckable(True)
        self.action_erase.setChecked(False)

        #Tools group
        self.group_action_tools = QtWidgets.QActionGroup(self)
        self.group_action_tools.addAction(self.action_move)
        self.group_action_tools.addAction(self.action_line)
        self.group_action_tools.addAction(self.action_rectangle)
        self.group_action_tools.addAction(self.action_ellipse)
        self.group_action_tools.addAction(self.action_polygon)
        self.group_action_tools.addAction(self.action_text)
        self.group_action_tools.addAction(self.action_erase)

        #### STYLE ####

        #Pen Color
        self.action_pen_color = QtWidgets.QAction(QtGui.QIcon('../icons/tool_pen.png'),self.tr("Color"), self)

        #Pen Lines     
        self.action_pen_SolidLine = QtWidgets.QAction(self.tr("SolidLine"), self)
        self.action_pen_DashLine = QtWidgets.QAction(self.tr("DashLine"), self)
        self.action_pen_DotLine = QtWidgets.QAction(self.tr("DotLine"), self)
        self.action_pen_DashDotLine = QtWidgets.QAction(self.tr("DashDotLine"), self)
        self.action_pen_DashDotDotLine = QtWidgets.QAction(self.tr("DashDotDotLine"), self)
        self.action_pen_CustomDashLine = QtWidgets.QAction(self.tr("CustomDashLine"), self)

        #Pen Width
        self.action_pen_width = QtWidgets.QAction(self.tr("Width"), self)

        #Brush Color
        self.action_brush_color = QtWidgets.QAction(QtGui.QIcon('../icons/colorize.png'),self.tr("Color"), self)

        #Brush Fill styles
        self.action_brush_SolidPattern = QtWidgets.QAction(self.tr("SolidPattern"), self)
        self.action_brush_Dense1Pattern = QtWidgets.QAction(self.tr("Dense1Pattern"), self)
        self.action_brush_Dense2Pattern = QtWidgets.QAction(self.tr("Dense2Pattern"), self)
        self.action_brush_Dense3Pattern = QtWidgets.QAction(self.tr("Dense3Pattern"), self)
        self.action_brush_Dense4Pattern = QtWidgets.QAction(self.tr("Dense4Pattern"), self)
        self.action_brush_Dense5Pattern = QtWidgets.QAction(self.tr("Dense5Pattern"), self)
        self.action_brush_Dense6Pattern = QtWidgets.QAction(self.tr("Dense6Pattern"), self)
        self.action_brush_Dense7Pattern = QtWidgets.QAction(self.tr("Dense7Pattern"), self)
        self.action_brush_NoBrush = QtWidgets.QAction(self.tr("NoBrush"), self)
        self.action_brush_HorPattern = QtWidgets.QAction(self.tr("HorPattern"), self)
        self.action_brush_VerPattern = QtWidgets.QAction(self.tr("VerPattern"), self)
        self.action_brush_CrossPattern = QtWidgets.QAction(self.tr("CrossPattern"), self)
        self.action_brush_BDiagPattern = QtWidgets.QAction(self.tr("BDiagPattern"), self)
        self.action_brush_FDiagPattern = QtWidgets.QAction(self.tr("FDiagPattern"), self)
        self.action_brush_DiagCrossPattern = QtWidgets.QAction(self.tr("DiagCrossPattern"), self)
      

        #Text font
        self.action_text_font = QtWidgets.QAction(QtGui.QIcon('../icons/tool_font.png'),self.tr("Font"), self)



    def create_menus(self) :

        ### STATUS BAR ###
        self.statusbar=self.statusBar()
        ### MENUBAR ###
        menubar = self.menuBar()

        #File
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_new)
        menu_file.addAction(self.action_open)
        menu_file.addAction(self.action_save)
        menu_file.addAction(self.action_save_as)
        menu_file.addAction(self.action_exit)

        #Tools
        menu_tools = menubar.addMenu('&Tools')
        menu_tools.addAction(self.action_move)
        menu_tools.addAction(self.action_line)
        menu_tools.addAction(self.action_rectangle)
        menu_tools.addAction(self.action_ellipse)
        menu_tools.addAction(self.action_polygon)
        menu_tools.addAction(self.action_text)
        menu_tools.addAction(self.action_erase)

        #Style
        menu_style=menubar.addMenu('&Style')

            #Submenu pen
        menu_style_pen=menu_style.addMenu('Pen')
        menu_style_pen.addAction(self.action_pen_color)

        menu_style_pen_line=menu_style_pen.addMenu('Line')
        menu_style_pen_line.addAction(self.action_pen_SolidLine)
        menu_style_pen_line.addAction(self.action_pen_DashLine)
        menu_style_pen_line.addAction(self.action_pen_DotLine)
        menu_style_pen_line.addAction(self.action_pen_DashDotLine)
        menu_style_pen_line.addAction(self.action_pen_DashDotDotLine)
        menu_style_pen_line.addAction(self.action_pen_CustomDashLine)

        menu_style_pen.addAction(self.action_pen_width)
            
            #Submenu brush
        menu_style_brush=menu_style.addMenu('Brush')
        menu_style_brush.addAction(self.action_brush_color)

        menu_style_brush_fill=menu_style_brush.addMenu('Fill')
        menu_style_brush_fill.addAction(self.action_brush_SolidPattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense1Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense2Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense3Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense4Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense5Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense6Pattern)
        menu_style_brush_fill.addAction(self.action_brush_Dense7Pattern)
        menu_style_brush_fill.addAction(self.action_brush_NoBrush)
        menu_style_brush_fill.addAction(self.action_brush_HorPattern)
        menu_style_brush_fill.addAction(self.action_brush_VerPattern)
        menu_style_brush_fill.addAction(self.action_brush_CrossPattern)
        menu_style_brush_fill.addAction(self.action_brush_BDiagPattern)
        menu_style_brush_fill.addAction(self.action_brush_FDiagPattern)
        menu_style_brush_fill.addAction(self.action_brush_DiagCrossPattern)
      

            #Font

        menu_style.addAction(self.action_text_font)


        #Help
        menu_help=menubar.addMenu(self.tr("&Help"))
        self.action_about_us = menu_help.addAction(self.tr("& About Us"))
        self.action_about_qt = menu_help.addAction(self.tr("& About Qt"))
        self.action_about_app = menu_help.addAction(self.tr("& About the Application"))

        ### TOOLBAR ###

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.action_new)
        toolbar.addAction(self.action_open)
        toolbar.addAction(self.action_save)
        toolbar.addAction(self.action_exit)
        toolbar.addAction(self.action_move)
        toolbar.addAction(self.action_line)
        toolbar.addAction(self.action_rectangle)
        toolbar.addAction(self.action_ellipse)
        toolbar.addAction(self.action_polygon)
        toolbar.addAction(self.action_text)
        toolbar.addAction(self.action_erase)
        toolbar.addAction(self.action_pen_color)
        toolbar.addAction(self.action_brush_color)
        toolbar.addAction(self.action_text_font)

        ### CONTEXT MENU ###

        self.contextMenu=QtWidgets.QMenu(self)

        ## Tools
        context_menu_tools = self.contextMenu.addMenu('&Tools')
        context_menu_tools.addAction(self.action_move)
        context_menu_tools.addAction(self.action_line)
        context_menu_tools.addAction(self.action_rectangle)
        context_menu_tools.addAction(self.action_ellipse)
        context_menu_tools.addAction(self.action_polygon)
        context_menu_tools.addAction(self.action_text)
        context_menu_tools.addAction(self.action_erase)

        ## Style
        context_menu_style=self.contextMenu.addMenu('&Style')

    
        #Submenu pen
        context_menu_style_pen=context_menu_style.addMenu('Pen')
        context_menu_style_pen.addAction(self.action_pen_color)

        context_menu_style_pen_line=context_menu_style_pen.addMenu('Line')
        context_menu_style_pen_line.addAction(self.action_pen_SolidLine)
        context_menu_style_pen_line.addAction(self.action_pen_DashLine)
        context_menu_style_pen_line.addAction(self.action_pen_DotLine)
        context_menu_style_pen_line.addAction(self.action_pen_DashDotLine)
        context_menu_style_pen_line.addAction(self.action_pen_DashDotDotLine)
        context_menu_style_pen_line.addAction(self.action_pen_CustomDashLine)

        context_menu_style_pen.addAction(self.action_pen_width)

        #Submenu brush
        context_menu_style_brush=context_menu_style.addMenu('Brush')
        context_menu_style_brush.addAction(self.action_brush_color)

        context_menu_style_brush_fill=context_menu_style_brush.addMenu('Fill')
        context_menu_style_brush_fill.addAction(self.action_brush_SolidPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense1Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense2Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense3Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense4Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense5Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense6Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_Dense7Pattern)
        context_menu_style_brush_fill.addAction(self.action_brush_NoBrush)
        context_menu_style_brush_fill.addAction(self.action_brush_HorPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_VerPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_CrossPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_BDiagPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_FDiagPattern)
        context_menu_style_brush_fill.addAction(self.action_brush_DiagCrossPattern)

        #Text Font
        context_menu_style.addAction(self.action_text_font)
        
        

        

    def connect_actions(self) :
        #file
        self.action_new.triggered.connect(self.file_new)
        self.action_open.triggered.connect(self.file_open)
        self.action_save.triggered.connect(self.file_save)
        self.action_save_as.triggered.connect(self.file_save_as)
        self.action_exit.triggered.connect(self.file_exit)
        
        #Tools
        self.action_move.triggered.connect(lambda checked, tool="move": self.set_action_tool(checked, tool))
        self.action_line.triggered.connect(lambda checked, tool="line": self.set_action_tool(checked,tool))
        self.action_rectangle.triggered.connect(lambda checked, tool="rectangle": self.set_action_tool(checked,tool))
        self.action_ellipse.triggered.connect(lambda checked, tool="ellipse": self.set_action_tool(checked,tool))
        self.action_polygon.triggered.connect(lambda checked, tool="polygon": self.set_action_tool(checked,tool))
        self.action_text.triggered.connect(lambda checked, tool="text": self.set_action_tool(checked,tool))
        self.action_erase.triggered.connect(lambda checked, tool="erase": self.set_action_tool(checked,tool))


        #Style
        self.action_pen_color.triggered.connect(self.pen_color_selection)
        self.action_pen_SolidLine.triggered.connect(lambda test, line=Qt.SolidLine: self.pen_line_selection(test,line))
        self.action_pen_DashLine.triggered.connect(lambda test, line = Qt.DashLine: self.pen_line_selection(test,line))
        self.action_pen_DotLine.triggered.connect(lambda test, line = Qt.DotLine: self.pen_line_selection(test,line))
        self.action_pen_DashDotLine.triggered.connect(lambda test, line = Qt.DashDotLine: self.pen_line_selection(test,line))
        self.action_pen_DashDotDotLine.triggered.connect(lambda test, line = Qt.DashDotDotLine: self.pen_line_selection(test,line))
        self.action_pen_CustomDashLine.triggered.connect(lambda test, line = Qt.CustomDashLine: self.pen_line_selection(test,line))


        self.action_pen_width.triggered.connect(self.pen_width_selection)
        self.action_brush_color.triggered.connect(self.brush_color_selection)
        
        self.action_brush_SolidPattern.triggered.connect(lambda test, style=Qt.SolidPattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense1Pattern.triggered.connect(lambda test, style=Qt.Dense1Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense2Pattern.triggered.connect(lambda test, style=Qt.Dense2Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense3Pattern.triggered.connect(lambda test, style=Qt.Dense3Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense4Pattern.triggered.connect(lambda test, style=Qt.Dense4Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense5Pattern.triggered.connect(lambda test, style=Qt.Dense5Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense6Pattern.triggered.connect(lambda test, style=Qt.Dense6Pattern: self.brush_fill_selection(test,style))
        self.action_brush_Dense7Pattern.triggered.connect(lambda test, style=Qt.Dense7Pattern: self.brush_fill_selection(test,style))
        self.action_brush_NoBrush.triggered.connect(lambda test, style=Qt.NoBrush: self.brush_fill_selection(test,style))
        self.action_brush_HorPattern.triggered.connect(lambda test, style=Qt.HorPattern: self.brush_fill_selection(test,style))
        self.action_brush_VerPattern.triggered.connect(lambda test, style=Qt.VerPattern: self.brush_fill_selection(test,style))
        self.action_brush_CrossPattern.triggered.connect(lambda test, style=Qt.CrossPattern: self.brush_fill_selection(test,style))
        self.action_brush_BDiagPattern.triggered.connect(lambda test, style=Qt.BDiagPattern: self.brush_fill_selection(test,style))
        self.action_brush_FDiagPattern.triggered.connect(lambda test, style=Qt.FDiagPattern: self.brush_fill_selection(test,style))
        self.action_brush_DiagCrossPattern.triggered.connect(lambda test, style=Qt.DiagCrossPattern: self.brush_fill_selection(test,style))
               

        self.action_text_font.triggered.connect(self.text_font_selection)

        #help
        self.action_about_us.triggered.connect(self.help_about_us)
        self.action_about_qt.triggered.connect(self.help_about_qt)
        self.action_about_app.triggered.connect(self.help_about_app)
        


    def contextMenuEvent(self, event) :
        contextAction = self.contextMenu.exec_(self.mapToGlobal(event.pos()))


    ###### FILE ######

    # New file
    def file_new(self):
        buttonReply = QtWidgets.QMessageBox.question(self, 'PyQt5 message', "Are you sure you want to open a new file ? Non-saved data will be lost.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            self.scene=None
            self.create_scene()
        self.statusbar.showMessage('New file opened')
       

    # Exit
    def file_exit(self):
        buttonReply = QtWidgets.QMessageBox.question(self, 'PyQt5 message', "Are you sure you want to quit ? Non-saved data will be lost.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
        print(int(buttonReply))
        if buttonReply == QtWidgets.QMessageBox.Yes:
            exit(0)


        
   
    #Open file
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        if fileopen.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)==None :
            print("fileopen.open(QtCore.QIODevice.WriteOnly)==None")
            return -1
        else :
            receivedData=load(str(filename[0]))
            self.scene.clear()
            self.scene.loadFile(receivedData)
            self.statusbar.showMessage('File Opened')



    # Save file
    def file_save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())
        filesave=QtCore.QFile(filename[0])
        if filesave.open(QtCore.QIODevice.WriteOnly)==None :
            print("filesave.open(QtCore.QIODevice.WriteOnly)==None")
            return -1
        else :
            items=[self.scene.lines, self.scene.rects, self.scene.ellipses, self.scene.texts, self.scene.polygons]
            save(items, str(filename[0]))
            self.statusbar.showMessage('File saved')
            


    #Save file as
    def file_save_as(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())
        filesave=QtCore.QFile(filename[0])
        if filesave.open(QtCore.QIODevice.WriteOnly)==None :
            print("filesave.open(QtCore.QIODevice.WriteOnly)==None")
            return -1
        else :
            items=[self.scene.lines, self.scene.rects, self.scene.ellipses, self.scene.texts, self.scene.polygons]
            save(items, str(filename[0]))
            self.statusbar.showMessage('File saved')


    ###### TOOL ######
    # Tool selector
    def set_action_tool(self,checked, tool) :
        self.scene.set_tool(self, tool)
        self.statusbar.showMessage('Selected Tool : ' + tool)

    ###### STYLE ######

    def pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            self.scene.set_pen_color(color)
            self.statusbar.showMessage('Changed Pen Color : ')
        else :
            print("color is not a valid one !")

    def pen_line_selection(self, test, line):
        self.scene.set_pen_line(line)
        self.statusbar.showMessage('Changed Pen Line')

    def pen_width_selection(self):
        width,ok = QtWidgets.QInputDialog.getInt(self,"Set width","Width:",3, 0, 30, 1)
        if ok:
            self.scene.set_pen_width(width)
            self.statusbar.showMessage('Changed Pen Width')



    def brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            self.scene.set_brush_color(color)
            self.statusbar.showMessage('Changed Brush Color')

        else :
            print("color is not a valid one !")


    def brush_fill_selection(self, test, style):
        self.scene.set_brush_style(style)
        self.statusbar.showMessage('Changed Brush Fill Style')

       
    def text_font_selection(self) :
        font, ok = QtWidgets.QFontDialog.getFont(QtGui.QFont("Helvetica [Cronyx]", 10), self);
        if ok :
            self.scene.set_text_font(font)
            self.statusbar.showMessage('Changed Text Font')




    ###### HELP ######

    def help_about_us(self):
        QtWidgets.QMessageBox.information(self, self.tr("About Me"),
                            self.tr("Author :\nThibaut Picart\n Copyright ENIB 2020"))
        
    def help_about_qt(self):
        QtWidgets.QMessageBox.information(self, self.tr("About Qt"),
                            self.tr("Thanks to the Qt API creators for \nallowing this application to exist."))

    def help_about_app(self):
        text=open('ReadMe.txt').read()
        QtWidgets.QMessageBox.information(self, self.tr("About the Application"), text)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

if __name__ == "__main__" :  
    print(QT_VERSION_STR)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.setWindowState(Qt.WindowMaximized);
    main.show()
    sys.exit(app.exec_())



