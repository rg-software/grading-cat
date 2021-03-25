# Grading Cat

## Setup

```shell
poetry install
```

## Working Process

1. Prepare a project directory `<ProjectDir>` and place there a configuration file `config.json`.

1. Download student submissions:

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



## Project Config File Attributes

Here is a sample:

```json
{
    "username": "my_moodle_user", 
    "password": "my_moodle_password", 
    "server_url": "https://moodle.university.edu", 
    "course_shortname": "SA06_20154128",
    "working_dir": "moodle_submissions",
    "assignment_regex": ".+\\.zip",
    "jplag_runcmd": ["java", "-jar", "../jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar"],
    "jplag_args": ["-s", "-l", "java19"]
}
```