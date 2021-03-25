# CHECK Jplag documentation: https://github.com/jplag/jplag
# basic run: java  -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -s -l java19 docs
# (use recursive mode; for some reason -s needs also another switch such as -l)
# it will recurse as deeply as necessary

# then java  -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -m 2% -s -l java19 c:\Projects-Hg\GradingCat\out-w6.4

import sys
import os
import json
import subprocess

# NOTE: we should be inside the project dir here
def run(config, assignment_name):
	in_dir = 'jpl_in_' + assignment_name # sys.argv[3]
	out_dir = 'jpl_out_' + assignment_name # sys.argv[3]
	cmd = config['jplag_runcmd'] + config['jplag_args'] + ['-r', out_dir, in_dir]

	print("will run as")
	print(cmd)
	subprocess.run(cmd)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: jplag_runner <project-dir> <assignment-name>")
		sys.exit(1)
	dir = os.getcwd()
	os.chdir(sys.argv[1])
	with open('config.json') as f:
		config = json.load(f)
	run(config, sys.argv[2])
	os.chdir(dir)