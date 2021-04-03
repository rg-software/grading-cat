import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6.QtGui import *
from operator import *
import config
import json
import os
from project_config_editor import ProjectConfigDialog

# When we run the app, we presume that 'empty' project is loaded. It is not saved anywhere
CurrentProjectPath = None

def getProjectSettings():
    json_path = 'project_config_template.json' if not CurrentProjectPath else os.path.join(CurrentProjectPath, 'config.json')
    with open(json_path) as f:
        config = json.load(f)
    return config


# TODO: should be a global main window object with the corresponding function and global app name setting
def getMainWin():
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

def updateMainWinTitle():
    getMainWin().setWindowTitle('Grading Cat: ' + str(CurrentProjectPath))

# TODO: rename to "project settings"
def detectingSoftware():
    isOk, config = ProjectConfigDialog.show(getMainWin(), getProjectSettings())

    # TODO: HERE MUST SAVE

    #Эта функция для задания настроек к JPag или каким-то его альтернативам. 
    #Скажи мне, какие для этого нужны поля, 
    #и я сделаю диалог с формой для задания таких настроек. 
    #Пока можно это вообще не трогать, но вообще, 
    #я думаю, полезно будет иметь возможность что-то поменять, дополнительно настраивать и подобное.
    print("detecting software")

#def 

#Привет, Максим! Это всё для тебя :)

#В этом файле функции, которые привязаны к меню (всё работает, я проверяла). 
#Ты можешь делать с ними все, что хочешь. 
#И даже, давать мне задания, как-то их заполнять, менять, улучшать, удалять, 
#добавлять новые функции, диалоги и формы.   
#Я еще не успела добавить никакие окна, но я надеюсь, это сделать завтра-послезавтра.  
#Но какую-то логику, возможно, уже можно добавить.
#Пока же, я планирую описать, как я думаю, они должны использоваться...

def newProject():
    print("new project")
    #Здесь будет открываться форма, для создания нового проекта. Я пока не успела сделать. 
    #Но, честно говоря, я не совсем понимаю, какие там нужны поля. 
    #В любом случае я сделаю, что-нибудь в ближайшее время, 
    #а потому уже можно будет править. Миром и проектами. 


def newDetectionSession():
    print("new detection session")

    #Эта та функция, которая запускает JPlag, и радует нас результатами :) 
    #Нужна ли тебе для запуска, какая-то особая форма? Диалог? Я сделаю. 
    #Мне же нужно, чтобы на выходе был результат следующего вида:
    #<имя1>-<имя2>: <число>\n 
    #как в примере 
    text = "s1252001-s1260009: 32.753624\ns1252001-s1260017: 21.987314\ns1252001-s1260027: 41.365463"
    #или как в файле jpl_out_Upload Solutions for Exercises 3.x.log
    #Можешь, проверить, открыв тот файл, который ты мне присылал, или подобный
    filename = QFileDialog.getOpenFileName(None,"Load File","","Text (*.log);;All Files (*)")[0]
    if filename != '':
        file = open(filename)
        try: text = file.read()
        finally: file.close()    
   
    return text

def openProject():
    #Здесь можно, выбрать папку уже существующего проекта. 
    #И автоматически загрузятся настройки этого проекта и что там еще нужно. 
    #Наверное, для этого можно использовать что-то такое
    #QFileDialog.getExistingDirectory( self, "Open a folder", "/home/my_user_name/", QFileDialog.ShowDirsOnly ) 

    #Еще у меня есть функция, которая открывает файл сохранения, я ее сюда не выносила. 
    #Но может, зря, может, нужно чтобы в таком случае, проект открывался автоматически. 
    #Но это не сложно будет добавить, я думаю.  
    print("open project")


def dataSource():
    #Здесь, по моему замыслу, настраивается доступ к Мудлу или его альтернативам. 
    #Я могу сделать удобную форму для этого. 
    #Идея в том, что если у тебя уже есть готовый проект, но что-то поменялось, 
    #например, пароль к Мудлу или еще что-то, 
    #ты можешь зайти сюда и поменять настройки. 
    print("data source")

def updateProjectData():
    #Эта функция для обновления Мудла. 
    #Не знаю нужна ли здесь какая-то особенная форма. 
    #Наверное, будет достаточно диалога окей/отменить. 
    #Но что нужно будет добавить, так это всплывающее сообщение после скачивания, 
    #или какой-то прогресс бар, да, как я понимаю. 
    #Вот, на самом деле не знаю, что проще… 
    #Но главное – это логика скачивания, а это с тебя ;) 
    print("update project data")

def importExportSettings():
    #Эта функция на случай, если ты уже все под себя настроил в одном проекте, 
    #и не хочешь заниматься тем же самым в новом.  
    #Думаю, можно просто дать возможность выбрать файл настроек из другого проекта, 
    #и скопировать их в текущий. Понятно, что это не самая жизненно необходимая функция, 
    #но очень может быть полезной, а сделать несложно… наверное. 
    print("import and export settings")

def exportTemplate():
    #Да, здесь я признаю, увлеклась. 
    #Даже точно не помню какой изначально был план :) 
    #Наверное, это будет зависеть от того, что такое будет наш проект, 
    #и что будет создаваться вначале. Но, вообще, 
    #было бы неплохо иметь возможность загрузить некий каркас, 
    #возможно с примерами, чтобы пользователь мог попробовать все, до того, 
    #как переименует все файлы нужным образом, и еще так по-всякому по-разному заморозится. 
    #Но, это, конечно та функция, которую ты ужалишь первой, и на том и будет, наш компромисс :D 
    #Как-то так...
    print("export template")

