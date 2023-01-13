# CHECK Jplag documentation: https://github.com/jplag/jplag
# Command line output can be used to generate a full similarity matrix.

# options to check:
# -t <n>          (Token) Tune the sensitivity of the comparison.
#                 A smaller <n> increases the sensitivity.
# -bc <dir>       Name of the directory which contains the basecode (common framework)
# -m  <p>         Matches with more than <p> percent similarity will be saved (default: 0).
# -l <lang>       Language to parse (default: java9)

import os
import subprocess
import ast


class JPlagReport:
    def __init__(self, java_path, basecode_dir, language, extra_args, assignment_name):
        in_dir = f"jpl_in_{assignment_name}"
        out_dir = f"jpl_out_{assignment_name}"

        jplag_dir = os.path.dirname(os.path.realpath(__file__))
        java_exe = os.path.expandvars(java_path)
        bc_arg = []  # BUG: bc argument is IGNORED in this version due to Jplag bug
        # bc_arg = ["-bc", basecode_dir] if basecode_dir else []
        lang_arg = ["-l", language]
        output_arg = ["-r", out_dir, in_dir]
        args = bc_arg + lang_arg + ast.literal_eval(extra_args) + output_arg
        jplag_runcmd = [java_exe, "-jar", os.path.join(jplag_dir, "jplag-3.0.0-al.jar")]
        cmd = jplag_runcmd + args
        print(f"Running: {cmd}")
        output = subprocess.run(cmd, capture_output=True)

        # RFE: maybe in the future we will only keep the best archive matches
        # RFE: process errors found in output
        # print(output.stderr) # do something about error log
        self.report_data = self._filtered_output(output)

    def _filtered_output(self, output):
        # take only "Comparing... " lines but without "comparing" prefix
        match_prefix = b"Comparing "

        return [
            line[len(match_prefix) :]
            for line in output.stdout.splitlines(True)
            if line.startswith(match_prefix)
        ]

    def report_lines(self):
        return self.report_data


# NOTE: we should be inside the project dir here
def run(java_path, language, extra_args, assignment_name):
    report = JPlagReport(java_path, "templates", language, extra_args, assignment_name)

    out_log = f"jpl_out_{assignment_name}.log"
    with open(out_log, "wb") as f:
        f.writelines(report.report_lines())
