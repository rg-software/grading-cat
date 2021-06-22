import sys
import os
import json
import interop.jplag_preprocessor
import interop.jplag_runner
import interop.moodle_downloader


def jplag_preprocessor(config, assignment_name):
    interop.jplag_preprocessor.preprocess_dirs(
        config["moodle_submissions_dir"],
        config["archive_dirs"],
        config["assignment_regex"],
        assignment_name,
    )


def jplag_runner(config, assignment_name):
    interop.jplag_runner.run(config["java_path"], config["jplag_args"], assignment_name)


def moodle_downloader(config, _):
    interop.moodle_downloader.download(config)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Commands:")
        print("jplag_preprocessor <project-dir> <assignment-name>")
        print("jplag_runner <project-dir> <assignment-name>")
        print("moodle_downloader <project-dir>")
        sys.exit(1)

    dir = os.getcwd()
    os.chdir(sys.argv[2])  # project dir
    with open("config.json") as f:
        config = json.load(f)

    args = sys.argv[3:] + [""]  # remaining args
    locals()[sys.argv[1]](config, args[0])
    os.chdir(dir)
