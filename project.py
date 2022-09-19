# Should be considered a singleton representing a currently loaded project.

import json
import csv
import re
import os
import shutil
from collections import namedtuple, defaultdict
from main_utils import appPath
from dotmap import DotMap

import interop.jplag_preprocessor as jplag_preprocessor
import interop.jplag_runner as jplag_runner
import interop.moodle_downloader as moodle_downloader


_CurrentProjectPath = None  # initially no project file is loaded
_CurrentAssignment = None  # no detection performed


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
        json.dump(config, f, indent=4)


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


def assignments():
    assert _CurrentProjectPath
    os.chdir(os.path.join(_CurrentProjectPath, settings().moodle_submissions_dir))
    r = [d for d in os.listdir() if os.path.isdir(d)]
    os.chdir(_CurrentProjectPath)
    return r


def _filter_arc_records(log):
    def is_arc_student(student):
        return student.startswith("arc[")

    def student_name(student_name):
        m = re.match("(arc\[.+\]).+", student_name)
        return m.group(1) if m else student_name

    # log is in a format
    # "<user1>-<user2>: <sim_ratio>\n<user1>-<user3>: <sim_ratio>\n..."
    # archived users are "arc[dirname]user"

    Match = namedtuple("Match", ["student1", "student2", "score"])

    log_matches = []  # first, remove all archive-archive matches
    for log_line in log.strip().split("\n"):
        m = re.match("(.+)-(.+): (.+)", log_line)
        log_matches.append(Match(m.group(1), m.group(2), float(m.group(3))))

    # next, combine all students of the same archive
    # use max score over the archive
    log_filtered = defaultdict(float)
    for m in log_matches:
        if not (is_arc_student(m.student1) and is_arc_student(m.student2)):
            key = (student_name(m.student1), student_name(m.student2))

            if key not in log_filtered:
                key = tuple(reversed(key))

            log_filtered[key] = max(log_filtered[key], m.score)

    # TODO: use dictionary as an input format for the matrix
    return "\n".join([f"{n1}-{n2}: {v}" for (n1, n2), v in log_filtered.items()])


def detect(asgn):
    global _CurrentAssignment
    assert _CurrentProjectPath

    cfg = settings()
    os.chdir(_CurrentProjectPath)
    _CurrentAssignment = asgn

    # do not run if we already have results
    if not os.path.exists(f"jpl_out_{asgn}.log"):
        jplag_preprocessor.preprocess_dirs(
            cfg.moodle_submissions_dir,
            cfg.archive_dirs,
            cfg.assignment_regexes,
            asgn,
        )
        jplag_runner.run(cfg.java_path, cfg.jplag_args, asgn)

    with open(f"jpl_out_{asgn}.log") as f:
        return _filter_arc_records(f.read())


def htmlReportPath(studentID_1, studentID_2):
    assert _CurrentProjectPath
    assert _CurrentAssignment

    asgn_path = os.path.join(_CurrentProjectPath, f"jpl_out_{_CurrentAssignment}")
    csv_path = os.path.join(asgn_path, "pair_report.csv")

    with open(csv_path) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if (studentID_1, studentID_2) in [(row[0], row[1]), (row[1], row[0])]:
                return os.path.join(asgn_path, row[2])

    assert False, "match not found"


#### MP ####
# NOTE(mm): obsolete function, but referenced in one place
def viewMatchReport(studentID_1, studentID_2):
    # TODO: should be in main window
    pass

    # # TODO: always shows 'match0.html' -- for testing
    # html_path = os.path.join(
    #     _CurrentProjectPath, f"jpl_out_{_CurrentAssignment}", "match0.html"
    # )
    # isOk = MatchViewerDialog.show(_getMainWin(), studentID_1, studentID_2, html_path)
    # if isOk:
    #     print("Yay!")
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
