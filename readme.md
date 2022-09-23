# Grading Cat

## Summary

Grading Cat is a source code plagiarism detection system, heavily emphasizing user convenience in specific, well-defined scenarios. Grading Cat is created to check student-submitted exercises within software engineering courses. The core detection functionality is provided by [JPlag](https://github.com/jplag/JPlag), while the rest of the system strives to provide smooth user experience. Note that Grading Cat is a work in progress.

## Setup

Make sure you have [Java](https://adoptium.net) and [Python](https://www.python.org) installed. Install [Poetry](https://python-poetry.org), then run

```shell
poetry install
```

Run Grading Cat with the command

```shell
poetry run python main.py
```

## Target Course Environment

Grading Cat is designed for a quite specific course setup, were it works reasonably well. Other setups might require more user effort. The "ideal" workflow is based on several presumptions:

1. A course has a [Moodle](https://moodle.org) page. This page contains a number of "Assignment" activities, allowing the students to upload their homeworks.

1. Each assignment presumes that the student has to upload one or more files, such as technical reports and zipped source code.

1. Assignments are uniformly organized, so the students are able to plagiarize within the same assignment only (i.e, we don't have to compare student A's homework 1 with the student B's homework 2).

1. We only need to search for "borrowings" in the given offline document collection (containing the homeworks of past and current students of the course).

1. The students might be given a code template for reuse: it should not be detected as plagiarism.

1. The same programming language is used throughout the course.

1. A separate system or technique is used to assess the quality rather than originality of student homeworks.

## Setting Up a Project

A project corresponds to an individual course, where Grading Cat is used. Setting up a project allows to deal with incoming student submissions gradually as they arrive, which is especially convenient if using Moodle.

Select the `File`, `New Project` menu item and choose or create an empty directory for the project. Next, edit project settings in the following dialog box. If you don't use Moodle, you can ignore Moodle-specific items. For the settings involving regular expressions (regexes), some useful presets are available.

### Moodle Settings

The following information must be specified:

* Your Moodle username and password.

* Moodle server URL (such as `https://moodle.my-uni.edu`; _not_ the course page).

* Course _shortname_ (shown, e.g, on the course page right under the course title next to `Dashboard / My courses`).

* Assignment regexes: a list of regexes used to identify relevant submission files. For example, you might want to download attached zip archives only, and skip PDF reports.

* Username conversions: a list of regex-based rules for extracting Moodle user names. Currently, Grading Cat identifies users by their email addresses, but you can, for example, make them shorter by keeping usernames only.

* Assignment conversions: a list of regex-based rules for giving assignments short and consistent names. For example, you might want to store all the submissions of a Moodle activity "Upload exercise 1 solutions" simply as "Ex-01".

All rename/conversion capabilities are optional. If no conversion rules can be applied to a certain string, it is left intact.

### Plagiarism Detection Settings

* Archive directories: a list of paths to "external" potential sources of plagiarism, such as past submissions.

* Template directory: a path to the teacher-provided code template, excluded from plagiarism detection.

* Language parser: the "CLI name" of the programming language used in assignments (must be supported by JPlag).

* Java path: a path to the main Java executable.

## Downloading and Managing Submissions

If Moodle is set up correctly, use the `Project`, `Sync with Data Source` menu item to download all available user submissions into the project directory. Previously downloaded files will not be overwritten, so this capability can be used to update the local collection of submissions.

**Note**: the downloader relies on [moodle_mobile_app](https://docs.moodle.org/dev/Web_service_API_functions#Core_web_service_functions) service, which might be turned off by the administrator or require additional user rights.

Downloaded submissions are stored inside the project directory as follows:

```text
<project-dir>
|-- submissions
    |-- <assignment-1>
        |-- <student-1>
        |   |-- <file-1>
        |   |-- <file-2>
        |       ...
        |-- <student-2>
        |   |-- <file-1>
        |   |-- <file-2>
        |       ...
        |   ...
        <assignment-2>
        ...
```

Thus, if Moodle is not used, you can simply copy your files into `submissions` subdirectory of the project, respecting these conventions.

Archive directories should be organized in a similar manner: each archive directory is essentially a renamed `submissions` directory, presumably containing submissions of a certain past course. Archives can be stored anywhere in the system.

## Detecting Plagiarism

Select `Project`, `Detect` menu item to prepare a plagiarism detection report for the given assignment. Grading Cat will copy input files into a temporary location, rearrange them as required by JPlag, unpack all archives, and invoke JPlag. Next, report data will be used to show a detection diagram. Subsequent `Detect` calls will reuse this existing report.

Currently it is not possible to force the system to re-download files or re-generate reports. As a workaround, you can manually delete them before running detection.

The diagram will show all student submissions and connect similar items according to a user-specified threshold. Each archive directory will be shown as a single pseudo-submission (with `arc` prefix) rather than a collection of real submissions. The rationale is to avoid clutter by removing redundant links: we are typically interested to reveal similarities between current submissions and our archive, but similarities _within_ the archive are not important anymore.

By right-clicking on a submission, you can access `Compare with` menu item and open a detailed comparison with similar submissions. Once a certain submission is processed, it can be hidden or even removed from the report. When comparing with an archive pseudo-submission, the top match is chosen.

## Command-line Interface


1. Prepare a project directory `<ProjectDir>` and place there a configuration file `config.json`.

1. Download/sync student submissions:

    ```shell
    poetry run python cli.py moodle_downloader <ProjectDir>
    ```

1. To work with a specific assignment, prepare it for JPlag processing:

    ```shell
    poetry run python jplag_preprocessor.py <ProjectDir> <AssignmentName>
    ```

1. Then process it with JPlag:

    ```shell
    poetry run python jplag_runner.py <ProjectDir> <AssignmentName>
    ```



## Notes

Granularity: weekly tasks