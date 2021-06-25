# JPLAG needs the following folder structure: ROOT/user1/*.java, ROOT/user2/*.java, ...
# We presume that each subdir in <week-dir> corresponds to an individual student.
# We get all files matching the regex filter and depack them to a dir constructed as <output-dir>/<user-dir>
# Archive dirs are handled separately.
# We prefix all older students with an "arc[<directory>]" string

import re
import os
import pathlib
import shutil
from pyunpack import Archive

ARCHIVE_FILE_MASK = ".+\\.(zip|rar)"  # supported archive types


def _output_dir(name):
    return f"jpl_in_{name}"


def _cleanup_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def _trailing_dir_name(full_path):
    return os.path.basename(os.path.normpath(full_path))


class JplInSubmission:
    def __init__(self, re_pattern, in_user_dir, output_dir):
        self.re_pattern = re_pattern
        self.in_user_dir = in_user_dir
        self.output_dir = output_dir

    def process(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for file in os.listdir(self.in_user_dir):
            if re.fullmatch(self.re_pattern, file):
                print(f"Processing file {file}")
                self._process_file(os.path.join(self.in_user_dir, file))

    def _process_file(self, in_path):
        if re.fullmatch(ARCHIVE_FILE_MASK, in_path):
            Archive(in_path).extractall(self.output_dir)  # depack
        else:
            shutil.copy(in_path, self.output_dir)  # simply copy


class JplInAssignment:
    def __init__(self, re_pattern, in_dir, name, is_arc):
        self.re_pattern = re_pattern
        self.prefix = f"arc[{_trailing_dir_name(in_dir)}]" if is_arc else ""
        self.week_dir = os.path.join(in_dir, name)
        self.output_dir = _output_dir(name)

    def process(self):
        print(f"{self.week_dir}, {self.output_dir}, {self.prefix}")

        for user_dir in os.listdir(self.week_dir):
            print(f"Processing user {user_dir}")
            in_dir = os.path.join(self.week_dir, user_dir)
            out_dir = os.path.join(self.output_dir, f"{self.prefix}{user_dir}")
            JplInSubmission(self.re_pattern, in_dir, out_dir).process()

        for p in pathlib.Path(self.output_dir).rglob("__macosx"):  # cleanup
            shutil.rmtree(p)


# NOTE: we should be inside the project dir here
def preprocess_dirs(submissions_dir, archive_dirs, re_pattern, assignment_name):
    _cleanup_dir(_output_dir(assignment_name))

    JplInAssignment(re_pattern, submissions_dir, assignment_name, False).process()
    for dir in archive_dirs:
        JplInAssignment(re_pattern, dir, assignment_name, True).process()
