# Grading Cat

## Setup

```shell
poetry install
```

## Working Process

1. Prepare a project directory `<ProjectDir>` and place there a configuration file `config.json`.

1. Download/sync student submissions:

    ```shell
    poetry run python moodle_downloader.py <ProjectDir>
    ```

1. To work with a specific assignment, prepare it for JPlag processing:

    ```shell
    poetry run python jplag_preprocessor.py <ProjectDir> <AssignmentName>
    ```

1. Then process it with JPlag:

    ```shell
    poetry run python jplag_runner.py <ProjectDir> <AssignmentName>
    ```

## Technical Notes

1. GradingCat activities are structured into "projects". A project corresponds to a single course with a number of activities, requiring user submissions. Thus, a project is configured once per course. All project data is stored in a single directory and its subdirectories with a configuration file `config.json` at the root. Configuration can be done manually, but some GUI assistance is planned.

1. Moodle downloader will save all submissions of the specified Moodle course into a certain subdirectory of the given project. Previously downloaded files will not be overwritten, so it is possible to run Moodle downloader to update local course submission files.

    Users and activities will be renamed according to `username_conversions` and `assignment_conversions` regular expressions. They can be empty if no conversion is necessary. The system analyzes the list sequentially and applies the first possible conversion. A dash sign in user names will be replaced with an underscore to avoid issues in further steps.

1. JPlag preprocessor will prepare files, related to an individual student activity, for further processing by JPlag. Technically it means ensuring `<root>/student/assignment` structure of directories and depacking of all archives. The preprocessor will also copy files from the archive of previous submissions. It is expected that the archive uses the same directory structure as prepared by Moodle downloader. Only files matching `assignment_regex` will be copied. We also plan "collate" functionality when all archive submissions will be represented as a result of a single virtual student.

1. JPlag runner will run a JPlag session for the given assignment. A log file with file pair similarity values and a full JPlag output directory will be created. 

## Project Config File Attributes

Here is a sample:

```json
{
    "username": "my_moodle_user", 
    "password": "my_moodle_password", 
    "server_url": "https://moodle.university.edu", 
    "course_shortname": "SA06_20154128",
    "moodle_submissions_dir": "moodle_submissions",
    "archive_dirs": ["s:\\Teaching\\DistrComp\\submissions\\2019", "s:\\Teaching\\DistrComp\\submissions\\2018"],
    "assignment_regex": ".+\\.zip",
    "username_conversions": [["(.+)@.+", "\\1"]],
    "assignment_conversions": [[".+(\\d\\d).+", "\\1"], [".+(\\d).+", "0\\1"]],
    "jplag_args": ["-s", "-l", "java19"]
}
```

TODO.
Sessions
 is a single plagiarism detection activity over a list of user submissions.

A session can be saved and resumed later, but it is expected that once grading is done, there will be no need to return to it. 
