# JPLAG needs the following folder structure: ROOT/user1/*.java, ROOT/user2/*.java, ...
# We presume that each subdir in <week-dir> corresponds to an individual student.
# We get all files matching the regex filter and depack them to a dir constructed as <output-dir>/<user-dir>
# Archive dirs are handled separately.
# We prefix all older students with an "arc[<directory>]" string
# and delete all "__macosx" folders

import re
import os
import pathlib
import shutil
from pyunpack import Archive

ARCHIVE_FILE_MASK = ".+\\.(zip|rar|7z|bz2|gz|tar)"  # supported types to be depacked


def _output_dir(name):
    return f"jpl_in_{name}"


def _cleanup_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def _trailing_dir_name(full_path):
    return os.path.basename(os.path.normpath(full_path))


class JplInSubmission:
    def __init__(self, re_patterns, in_user_dir, output_dir):
        self.re_patterns = re_patterns
        self.in_user_dir = in_user_dir
        self.output_dir = output_dir

    def process(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        re_extracted = [self._regex_extract(r) for r in self.re_patterns]
        for file in os.listdir(self.in_user_dir):
            matches = [bool(re.fullmatch(r, file)) for r in re_extracted]
            if True in matches:
                print(f"Processing file {file}")
                self._process_file(os.path.join(self.in_user_dir, file))

    def _regex_extract(self, line):  # the last chunk only in this case
        return line.split("::")[-1].strip()

    def _process_file(self, in_path):
        if re.fullmatch(ARCHIVE_FILE_MASK, in_path):
            Archive(in_path).extractall(self.output_dir)  # depack
        else:
            shutil.copy(in_path, self.output_dir)  # simply copy


class JplInAssignment:
    def __init__(self, re_patterns, in_dir, name, is_arc):
        self.re_patterns = re_patterns
        self.prefix = f"arc[{_trailing_dir_name(in_dir)}]" if is_arc else ""
        self.week_dir = os.path.join(in_dir, name)
        self.output_dir = _output_dir(name)

    def process(self):
        print(f"{self.week_dir}, {self.output_dir}, {self.prefix}")

        for user_dir in os.listdir(self.week_dir):
            print(f"Processing user {user_dir}")
            in_dir = os.path.join(self.week_dir, user_dir)
            out_dir = os.path.join(self.output_dir, f"{self.prefix}{user_dir}")
            JplInSubmission(self.re_patterns, in_dir, out_dir).process()

        for p in pathlib.Path(self.output_dir).rglob("__macosx"):  # cleanup
            shutil.rmtree(p)


# NOTE: we should be inside the project dir here
def preprocess_dirs(submissions_dir, arc_dirs, template_dir, re_patterns, asgn_name):
    out_dir = _output_dir(asgn_name)
    out_template_dir = os.path.join(out_dir, "templates")
    _cleanup_dir(out_dir)

    JplInAssignment(re_patterns, submissions_dir, asgn_name, False).process()
    for dir in arc_dirs:
        JplInAssignment(re_patterns, dir, asgn_name, True).process()

    if template_dir:
        shutil.copytree(template_dir, out_template_dir)
    else:
        os.makedirs(out_template_dir)  # let's have an empty folder at least
