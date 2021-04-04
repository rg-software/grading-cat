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
import shutil
import os
from project_config_editor import ProjectConfigDialog

CurrentProjectPath = None # initially no project file is loaded

# starting folder for project open dialog (may be revised)
def getDefaultDir():
    return os.path.dirname(os.path.realpath(__file__))

def getProjectSettings():
    json_path = os.path.join(CurrentProjectPath, 'config.json')
    with open(json_path) as f:
        config = json.load(f)
    return config

def saveProjectSettings(config):
    json_path = os.path.join(CurrentProjectPath, 'config.json')
    with open(json_path, 'w') as f:
        json.dump(config, f)


# TODO: should be a global main window object with the corresponding function and global app name setting
def getMainWin():
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

def updateMainWinTitle():
    getMainWin().setWindowTitle(f'Grading Cat: {CurrentProjectPath}')

# must be called before we do anything
def newProject():
    r = QFileDialog.getExistingDirectory(getMainWin(), "Choose project folder", getDefaultDir(), QFileDialog.ShowDirsOnly)
    if r:
        global CurrentProjectPath
        CurrentProjectPath = r
        shutil.copyfile(os.path.join(getDefaultDir(), 'project_config_template.json'), os.path.join(CurrentProjectPath, 'config.json'))
        # TODO(mm): rename to "project settings"
        updateMainWinTitle()
        detectingSoftware()

# TODO: rename to "project settings"
# TODO: should be DISABLED until a project is created or opened
def detectingSoftware():
    isOk, config = ProjectConfigDialog.show(getMainWin(), getProjectSettings())
    if isOk:
        saveProjectSettings(config)

def openProject():
    r = QFileDialog.getExistingDirectory(getMainWin(), "Choose project folder", getDefaultDir(), QFileDialog.ShowDirsOnly)
    if r:
        global CurrentProjectPath
        CurrentProjectPath = r
        updateMainWinTitle()

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

