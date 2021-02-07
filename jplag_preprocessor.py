import sys
import re
import os
import zipfile

if len(sys.argv) != 4:
	print("Usage: jplag_preprocessor <week-dir> <task-zip-regex> <output-dir>")
	sys.exit(1)

# We presume that each subdir in <week-dir> corresponds to an individual student.
# We get all files matching the regex filter and depack them to a dir constructed as <output-dir>/<user-dir>
# Run, e.g., as jplag_preprocessor.py "DC_submissions\Upload Solutions for Exercises 6.x" .+6.4.+zip c:\Projects-Hg\GradingCat\out-w6.4
# then java  -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -s -l java19 c:\Projects-Hg\GradingCat\out-w6.4

week_dir = sys.argv[1]
re_pattern = sys.argv[2]
output_dir = sys.argv[3]

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
		with zipfile.ZipFile(os.path.join(input_user_dir, file), "r") as zip_ref:
			names_filtered = [name for name in zip_ref.namelist() if not name.startswith("__")] # skip "__MACOSX"
			zip_ref.extractall(output_user_dir, members=names_filtered)

