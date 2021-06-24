# TODO: this is a temporary "function collection" module, to be reorganized

import config


def newDiagramFromJPlag(text):
    # text = "s1252001-s1260009: 32.753624\ns1252001-s1260017: 21.987314\ns1252001-s1260027: 41.365463"
    resultsList = text.split("\n")
    studentA = []
    studentB = []
    rate = []
    students = []
    matrix = []
    for i in range(len(resultsList)):
        resultsList[i].replace(" ", "")
        if len(resultsList[i]) > 0 and "-" in resultsList[i] and ":" in resultsList[i]:
            part1 = resultsList[i].split("-")
            part2 = part1[1].split(":")
            studentA.append(part1[0])
            studentB.append(part2[0])
            rate.append(part2[1])
            if studentA[i] not in students:
                students.append(studentA[i])
            if studentB[i] not in students:
                students.append(studentB[i])

    for i in range(len(students)):
        line = []
        for j in range(len(students)):
            line.append(0)
        matrix.append(line)

    for i in range(len(studentA)):
        indexA = students.index(studentA[i])
        indexB = students.index(studentB[i])
        matrix[indexA][indexB] = int(float(rate[i]))
        matrix[indexB][indexA] = int(float(rate[i]))

    return students, matrix


def saveMatrix(students, rate):
    # window.ui.lineEdit.clear
    config.STUDENTS_LIST.clear()
    config.RESULT_MATRIX.clear()
    config.HIDED_STUDENTS.clear()
    config.SELECTED_STUDENTS.clear()
    config.SELECTED_STUDENT = ""

    config.STUDENTS_LIST.extend(students)
    config.RESULT_MATRIX.extend(rate)


def newSessionDiagram(text):
    if text != "":
        students, matrix = newDiagramFromJPlag(text)
        if len(students) > 1 and len(matrix) == len(students):
            saveMatrix(students, matrix)
            if (
                len(config.STUDENTS_LIST) > 1
                and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX)
                and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0])
            ):
                return True

    return False
