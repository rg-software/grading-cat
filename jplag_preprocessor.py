# JPLAG needs the following folder structure: ROOT/user1/*.java, ROOT/user2/*.java, ...
# We presume that each subdir in <week-dir> corresponds to an individual student.
# We get all files matching the regex filter and depack them to a dir constructed as <output-dir>/<user-dir>

# TODO: archive dirs should be handled separately; we need a special "collate" setting to combine all older students into a single cluster
# TODO: skip depacking if a file is NOT archive (just plain Java, e.g.)

import sys
import re
import os
import json
import pathlib
import shutil
from pyunpack import Archive


# NOTE: we should be inside the project dir here
def preprocess_dirs(dirs, re_pattern, assignment_name):
	output_dir = 'jpl_in_' + assignment_name
	if os.path.exists(output_dir):
		shutil.rmtree(output_dir)
	os.makedirs(output_dir)
	
	for base_input_dir in dirs:
		week_dir = os.path.join(base_input_dir, assignment_name)
		print(f"Processing assignments from {week_dir}")
		preprocess(re_pattern, week_dir, output_dir)


def preprocess(re_pattern, week_dir, output_dir):
	user_dirs = [name for name in os.listdir(week_dir)]

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
	dirs = [config["moodle_submissions_dir"]] + config["archive_dirs"]
	preprocess_dirs(dirs, config['assignment_regex'], sys.argv[2])
	os.chdir(dir)
