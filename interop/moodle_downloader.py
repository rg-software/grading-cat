# https://docs.moodle.org/dev/Web_service_API_functions#Core_web_service_functions

# The api documentation that provides more extensive documentation on not only
# what the required parameters are for all the available webservice functions
# but also the expected response and their structures in both REST and XML-RPC
# is accessible from the moodle site.
# For access to these docs you must have admin access as they are found in
# admin submenu located at:
# site administration > Plugins > Web services > API Documentation

import requests
import os
import re
import ast
from dotmap import DotMap


class StubProgressObject:  # for CLI (in GUI we use the real one)
    def setMaximum(self, _):
        pass

    def setValue(self, _):
        pass

    def processAppEvents(self):
        pass

    def wasCanceled(self):
        return False


def _regex_rename(conv_list, str):
    for pattern, repl in conv_list:
        if re.fullmatch(pattern, str):
            return re.sub(pattern, repl, str)
    return str


class MoodleSession:
    def __init__(self, cfg):
        self.rest_url = f"{cfg.server_url}/webservice/rest/server.php"
        self.login_url = f"{cfg.server_url}/login/token.php"
        self.token = self._get_token(cfg.username, cfg.password)
        self.user_dirs = self._user_dirs(cfg.course_shortname, cfg.username_conversions)
        self.assignment_conversions = cfg.assignment_conversions

    def _user_dirs(self, course_shortname, conversions):
        userdata = self._course_users(course_shortname)
        users = {}  # id -> email-based username
        for user in [DotMap(u) for u in userdata]:
            conv = ast.literal_eval(conversions)
            # '-' in files is bad for analyzing JPlag output
            new_uname = _regex_rename(conv, user.email).replace("-", "_")
            print(f"Renaming user: {user.email} -> {new_uname}")
            users[user.id] = new_uname
        return users

    def _call(self, function, p):
        p.update(
            {
                "wstoken": self.token,
                "wsfunction": function,
                "moodlewsrestformat": "json",
            }
        )
        return requests.get(self.rest_url, params=p).json()

    def _get_token(self, username, password):
        p = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app",
        }
        return requests.get(self.login_url, params=p).json()["token"]

    def _course_by_shortname(self, shortname):  # list of all matching courses
        courses = self._call(
            "core_course_get_courses_by_field",
            {"field": "shortname", "value": shortname},
        )

        return courses["courses"][0]  # only one course matches the given name

    def _course_users(self, course_shortname):
        course_id = self._course_by_shortname(course_shortname)["id"]
        return self._call(
            "core_enrol_get_enrolled_users",
            {"courseid": course_id},
        )

    def userdir(self, user_id):
        return self.user_dirs[user_id]

    def course_assignments(self, course_shortname):
        course_id = self._course_by_shortname(course_shortname)["id"]
        # assignments with ext info
        r = self._call(
            "mod_assign_get_assignments",
            {"courseids[0]": course_id},
        )
        return [Assignment(self, d) for d in r["courses"][0]["assignments"]]

    def course_submissions(self, assignment_id):
        # submissions with ext info
        r = self._call(
            "mod_assign_get_submissions",
            {"assignmentids[0]": assignment_id},
        )
        return [Submission(self, d) for d in r["assignments"][0]["submissions"]]

    def download_file(self, url, path):
        r = requests.get(f"{url}?token={self.token}")
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)


class SubmittedFile:
    def __init__(self, session, dict):
        self.session = session
        self.file = DotMap(dict)

    def process(self, working_dir):
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        # RFE: maybe check if some files got updated?
        # RFE: maybe download new/delete old files instead?
        target_path = os.path.join(working_dir, self.file.filename)
        if not os.path.exists(target_path):  # skip existing files
            print(f"\t\tDownloading file: {self.file.filename}")
            self.session.download_file(self.file.fileurl, target_path)


class Submission:
    def __init__(self, session, dict):
        self.session = session
        self.submission = DotMap(dict)

    def process(self, working_dir):
        user_dir = self.session.userdir(self.submission.userid)
        full_dir = os.path.join(working_dir, user_dir)

        print(f"\tProcessing user: {user_dir}")
        for plugin in self.submission.plugins:  # need to find attached files
            if "fileareas" in plugin:
                # perhaps, can be several areas, let's take the first one
                areas = plugin["fileareas"]
                for f in areas[0]["files"]:
                    SubmittedFile(self.session, f).process(full_dir)


class Assignment:
    def __init__(self, session, dict):
        self.session = session
        self.assignment = DotMap(dict)
        conv = ast.literal_eval(session.assignment_conversions)
        self.new_name = _regex_rename(conv, self.assignment.name)
        print(f"Renaming asignment: {self.assignment.name} -> {self.new_name}")

    def process(self, working_dir, progressObject):
        # such as "Exercises for Week 1"
        print(f"Saving assignment '{self.assignment.name}' data")
        submissions = self.session.course_submissions(self.assignment.id)
        full_dir = os.path.join(working_dir, self.new_name)

        for submission in submissions:
            progressObject.processAppEvents()
            if progressObject.wasCanceled():
                raise RuntimeError()
            submission.process(full_dir)


# NOTE: we should be inside the project dir here
def download(cfg, progressObject=StubProgressObject()):
    cfg = DotMap(cfg)  # TODO: move DotMap() call to the outer module
    s = MoodleSession(cfg)

    assignments = s.course_assignments(cfg.course_shortname)
    progressObject.setMaximum(len(assignments) - 1)

    try:
        for i, assignment in enumerate(assignments):
            progressObject.setValue(i)
            assignment.process(cfg.moodle_submissions_dir, progressObject)

    except RuntimeError:
        print("Download process canceled")
