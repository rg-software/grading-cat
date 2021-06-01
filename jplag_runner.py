# CHECK Jplag documentation: https://github.com/jplag/jplag
# Command line output can be used to generate a full similarity matrix.
# Matches can be ranked according to average or max similarity (the latter is useful if programs are different in size)

# options to check:
# -t <n>          (Token) Tune the sensitivity of the comparison. A smaller <n> increases the sensitivity. ("min_token_match", default 10)
# -bc <dir>       Name of the directory which contains the basecode (common framework)
# -m  <p>%         All matches with more than <p>% similarity will be saved.

# -m might be needed to analyze specific file/file similarity reports

import sys
import os
import json
import subprocess
import ast

# NOTE: we should be inside the project dir here
def run(java_path, jplag_args, assignment_name):
	in_dir = 'jpl_in_' + assignment_name
	out_dir = 'jpl_out_' + assignment_name
	out_log = 'jpl_out_' + assignment_name + '.log'

	jplag_dir = os.path.dirname(os.path.realpath(__file__))
	java_exe = os.path.expandvars(java_path)
	jplag_runcmd = [java_exe, '-jar', os.path.join(jplag_dir, 'jplag-2.12.1.jar')]
	cmd = jplag_runcmd + ast.literal_eval(jplag_args) + ['-r', out_dir, in_dir]
	output = subprocess.run(cmd, capture_output=True)
	# TODO: process errors found in output
	cmp_prefix = b'Comparing ' # will strip it
	output_lines_filtered = [line[len(cmp_prefix):] for line in output.stdout.splitlines(True) if line.startswith(cmp_prefix)]

	with open(out_log, 'wb') as f:
		f.writelines(output_lines_filtered)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: jplag_runner <project-dir> <assignment-name>")
		sys.exit(1)
	dir = os.getcwd()
	os.chdir(sys.argv[1])
	with open('config.json') as f:
		config = json.load(f)
	run(config['java_path'], config['jplag_args'], sys.argv[2])
	os.chdir(dir)