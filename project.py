# Should be considered a singleton representing a currently loaded project.

import json
import os
import shutil
import sys
from main_utils import appPath
from dotmap import DotMap

import interop.jplag_preprocessor as jplag_preprocessor
import interop.jplag_runner as jplag_runner
import interop.moodle_downloader as moodle_downloader


_CurrentProjectPath = None  # initially no project file is loaded
_CurrentAssignment = None  # TODO: to remove


def _templatesDir():
    return appPath()  # may be revised


def settings():
    assert _CurrentProjectPath
    json_path = os.path.join(_CurrentProjectPath, "config.json")
    with open(json_path) as f:
        return DotMap(json.load(f))


def saveSettings(config):
    json_path = os.path.join(_CurrentProjectPath, "config.json")
    with open(json_path, "w") as f:
        json.dump(config, f)


def newProject(project_path):  # initialize project at given path
    global _CurrentProjectPath
    _CurrentProjectPath = project_path
    shutil.copyfile(
        os.path.join(_templatesDir(), "config_template.json"),
        os.path.join(_CurrentProjectPath, "config.json"),
    )


def openProject(project_path):  # open project at given path
    global _CurrentProjectPath
    _CurrentProjectPath = project_path


def syncWithDataSource(progress_object):
    assert _CurrentProjectPath
    os.chdir(_CurrentProjectPath)
    moodle_downloader.download(settings(), progress_object)


#######


def assignments():
    assert _CurrentProjectPath
    os.chdir(os.path.join(_CurrentProjectPath, settings().moodle_submissions_dir))
    r = [d for d in os.listdir() if os.path.isdir(d)]
    os.chdir(_CurrentProjectPath)
    return r


def detect(asgn):
    assert _CurrentProjectPath
    global _CurrentAssignment

    _CurrentAssignment = asgn
    cfg = settings()
    os.chdir(_CurrentProjectPath)

    # do not run if we already have results
    if not os.path.exists(f"jpl_out_{asgn}.log"):
        jplag_preprocessor.preprocess_dirs(
            cfg.moodle_submissions_dir,
            cfg.archive_dirs,
            cfg.assignment_regex,
            asgn,
        )
        jplag_runner.run(cfg.java_path, cfg.jplag_args, asgn)

    # must be in a format
    # "<user1>-<user2>: <sim_ratio>\n<user1>-<user3>: <sim_ratio>\n..."
    with open(f"jpl_out_{asgn}.log") as f:
        return f.read()


#### MP ####
def сall_me_whatever_you_like(studentID_1, studentID_2):
    # TODO: always shows 'match0.html' -- for testing
    html_path = os.path.join(
        _CurrentProjectPath, f"jpl_out_{_CurrentAssignment}", "match0.html"
    )
    isOk = MatchViewerDialog.show(_getMainWin(), studentID_1, studentID_2, html_path)
    if isOk:
        print("Yay!")
    # CurrentAssignment
    # do whatever you want


def dataSource():
    # Здесь, по моему замыслу, настраивается доступ к Мудлу или его альтернативам.
    # Я могу сделать удобную форму для этого.
    # Идея в том, что если у тебя уже есть готовый проект, но что-то поменялось,
    # например, пароль к Мудлу или еще что-то,
    # ты можешь зайти сюда и поменять настройки.
    print("data source")


def importExportSettings():
    # Эта функция на случай, если ты уже все под себя настроил в одном проекте,
    # и не хочешь заниматься тем же самым в новом.
    # Думаю, можно просто дать возможность выбрать файл настроек из другого проекта,
    # и скопировать их в текущий. Понятно, что это не самая жизненно необходимая функция,
    # но очень может быть полезной, а сделать несложно… наверное.
    print("import and export settings")


def exportTemplate():
    # Да, здесь я признаю, увлеклась.
    # Даже точно не помню какой изначально был план :)
    # Наверное, это будет зависеть от того, что такое будет наш проект,
    # и что будет создаваться вначале. Но, вообще,
    # было бы неплохо иметь возможность загрузить некий каркас,
    # возможно с примерами, чтобы пользователь мог попробовать все, до того,
    # как переименует все файлы нужным образом, и еще так по-всякому по-разному заморозится.
    # Но, это, конечно та функция, которую ты ужалишь первой, и на том и будет, наш компромисс :D
    # Как-то так...
    print("export template")
