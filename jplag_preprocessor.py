# JPLAG needs the following folder structure: ROOT/user1/*.java, ROOT/user2/*.java, ...
# We presume that each subdir in <week-dir> corresponds to an individual student.
# We get all files matching the regex filter and depack them to a dir constructed as <output-dir>/<user-dir>

import sys
import re
import os
import json
import pathlib
import shutil
from pyunpack import Archive

# NOTE: we should be inside the project dir here
def preprocess(config, assignment_name):
	week_dir = os.path.join(config['working_dir'], assignment_name) # sys.argv[1]
	re_pattern = config['assignment_regex'] # sys.argv[2]
	output_dir = 'jpl_in_' + assignment_name # sys.argv[3]

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	user_dirs = [name for name in os.listdir(week_dir)] # if os.path.isdir(os.path.join(week_dir, name))]

	for user_dir in user_dirs:
		input_user_dir = os.path.join(week_dir, user_dir)
		output_user_dir = os.path.join(output_dir, user_dir)

		if not os.path.exists(output_user_dir):
			os.makedirs(output_user_dir)

		files = [name for name in os.listdir(input_user_dir) if re.fullmatch(re_pattern, name)]
		
		for file in files:
			print(f"Depacking {file} of user {user_dir}")
			Archive(os.path.join(input_user_dir, file)).extractall(output_user_dir)

	# note: seems like a necessary cleanup
	for p in pathlib.Path(output_dir).rglob('__macosx'):
		shutil.rmtree(p)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: jplag_preprocessor <project-dir> <assignment-name>")
		sys.exit(1)
	dir = os.getcwd()
	os.chdir(sys.argv[1])
	with open('config.json') as f:
		config = json.load(f)
	preprocess(config, sys.argv[2])
	os.chdir(dir)