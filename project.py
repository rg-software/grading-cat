import json
import os
import shutil
import sys
import types

from PySide6 import QtCore
from PySide6.QtWidgets import *

import config
import jplag_preprocessor
import jplag_runner
import moodle_downloader
from project_config_editor import ProjectConfigDialog

CurrentProjectPath = None # initially no project file is loaded

#### Internal functions ####

def _updateSettingsItems():
    _getMainWin().ui.actionSettings.setEnabled(True)
    _getMainWin().ui.actionSync_with_Data_Source.setEnabled(True)
    _getMainWin().ui.actionDetect.setEnabled(True)

# starting folder for project open dialog (may be revised)
def _getDefaultDir():
    return os.path.dirname(os.path.realpath(__file__))

def _getProjectSettings():
    json_path = os.path.join(CurrentProjectPath, 'config.json')
    with open(json_path) as f:
        config = json.load(f)
    return config

def _saveProjectSettings(config):
    json_path = os.path.join(CurrentProjectPath, 'config.json')
    with open(json_path, 'w') as f:
        json.dump(config, f)

# better make it a global main window object rather than search it like this
def _getMainWin():
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget

#### API Functions ####

def updateMainWinTitle():
    _getMainWin().setWindowTitle(f'{config.APPLICATION_TITLE}: {CurrentProjectPath}')


def updateSettingsItems():
    getMainWin().ui.actionSettings.setEnabled(True)
    getMainWin().ui.actionSync_with_Data_Source.setEnabled(True)
    getMainWin().ui.actionDetect.setEnabled(True)


# TODO: ensure some project is open
def setSettings():
    isOk, config = ProjectConfigDialog.show(_getMainWin(), _getProjectSettings())
    if isOk:
        _saveProjectSettings(config)

# TODO: ensure some project is open
def syncWithDataSource():
    progress = QProgressDialog("Downloading files...", "Cancel", 0, 1, _getMainWin())
    progress.setMinimumDuration(0)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.processAppEvents = types.MethodType(lambda x: QtCore.QCoreApplication.instance().processEvents(), progress)

    os.chdir(CurrentProjectPath)
    moodle_downloader.download(_getProjectSettings(), progress)

# TODO: ensure some project is open
def detect():
    prj_config = _getProjectSettings()
    os.chdir(os.path.join(CurrentProjectPath, prj_config["moodle_submissions_dir"]))
    assignments = [d for d in os.listdir() if os.path.isdir(d)]
    r, isOk = QInputDialog.getItem(_getMainWin(), config.APPLICATION_TITLE, 'Choose assignment', assignments, editable=False)
    if isOk:
        os.chdir(CurrentProjectPath)
        dirs = [prj_config["moodle_submissions_dir"]] + prj_config["archive_dirs"]
        jplag_preprocessor.preprocess_dirs(dirs, prj_config['assignment_regex'], r)
        jplag_runner.run(prj_config['jplag_args'], r)
    
    # TODO: return diagram data
    return ""

# must be called before we do anything
def newProject():
    r = QFileDialog.getExistingDirectory(_getMainWin(), "Choose project folder", _getDefaultDir(), QFileDialog.ShowDirsOnly)
    if r:
        global CurrentProjectPath
        CurrentProjectPath = r
        shutil.copyfile(os.path.join(_getDefaultDir(), 'project_config_template.json'), os.path.join(CurrentProjectPath, 'config.json'))
        updateMainWinTitle()
        setSettings()
        _updateSettingsItems()

def openProject():
    r = QFileDialog.getExistingDirectory(_getMainWin(), "Choose project folder", _getDefaultDir(), QFileDialog.ShowDirsOnly)
    if r:
        global CurrentProjectPath
        CurrentProjectPath = r
        updateMainWinTitle()
        _updateSettingsItems()




def newDetectionSession():
    r = 'testassignment'
    with open(f'jpl_out_{r}.log') as f:
        text = f.read()
    return text
    
    # TODO: it must work even if the user cancels the session
    return None
    #print("new detection session")

    #Эта та функция, которая запускает JPlag, и радует нас результатами :) 
    #Нужна ли тебе для запуска, какая-то особая форма? Диалог? Я сделаю. 
    #Мне же нужно, чтобы на выходе был результат следующего вида:
    #<имя1>-<имя2>: <число>\n 
    #как в примере 
    return "s1252001-s1260009: 32.753624\ns1252001-s1260017: 21.987314\ns1252001-s1260027: 41.365463"
    #или как в файле jpl_out_Upload Solutions for Exercises 3.x.log
    #Можешь, проверить, открыв тот файл, который ты мне присылал, или подобный
    # filename = QFileDialog.getOpenFileName(None,"Load File","","Text (*.log);;All Files (*)")[0]
    # if filename != '':
    #     file = open(filename)
    #     try: text = file.read()
    #     finally: file.close()    
   
    # return text


def dataSource():
    #Здесь, по моему замыслу, настраивается доступ к Мудлу или его альтернативам. 
    #Я могу сделать удобную форму для этого. 
    #Идея в том, что если у тебя уже есть готовый проект, но что-то поменялось, 
    #например, пароль к Мудлу или еще что-то, 
    #ты можешь зайти сюда и поменять настройки. 
    print("data source")

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

