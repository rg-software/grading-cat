#https://docs.moodle.org/dev/Web_service_API_functions#Core_web_service_functions

#The api documentation that provides more extensive documentation on not only what the required parameters are for all the available webservice functions but also the expected response and their structures in both REST and XML-RPC is accessible from the moodle site.
# For access to these docs you must have admin access as they are found in admin submenu located at:
# site administration > Plugins > Web services > API Documentation

import requests
import os
import sys
import json
import re
import ast


class StubProgressObject():
	def setMaximum(self, _):
		pass
	
	def setValue(self, _):
		pass

	def processAppEvents(self, _):
		pass

	def wasCanceled(self):
		return False


def regex_rename(conv_list, str):
	for pattern, repl in conv_list:
		if re.fullmatch(pattern, str):
			return re.sub(pattern, repl, str)
	return str

def get_token(username, password, server_url):
	response = requests.get(server_url + '/login/token.php', params={'username': username, 'password': password, 'service': 'moodle_mobile_app'})
	return response.json()['token']

def call_service(server_url, token, function, params):
	params.update({'wstoken': token, 'wsfunction': function, 'moodlewsrestformat': 'json'})
	response = requests.get(server_url + '/webservice/rest/server.php', params=params)
	return response.json()

def process_file(f, working_dir, token):
	filename = f['filename']
	download_url = f['fileurl'] + "?token=" + token
	
	if not os.path.exists(working_dir):
		os.makedirs(working_dir)

	# TODO: checksum testing (?) -- no need to redownload already downloaded files
	# TODO: perhaps, this script should 'sync' rather than download files: so we download new files and delete extra files
	if not os.path.exists(os.path.join(working_dir, filename)):
		print(f"\t\tDownloading file: {filename}")
		r = requests.get(download_url)
		if r.status_code == 200:
			with open(os.path.join(working_dir, filename), 'wb') as f:
				f.write(r.content)

def process_submission(submission, working_dir, users, token):
	user_id = submission['userid']
	user_email = users[user_id]
	print(f"\tProcessing user: {user_email}")
	
	dir = os.path.join(working_dir, user_email)

	for plugin in submission['plugins']:    # need to find attached files
		if 'fileareas' in plugin:
			areas = plugin['fileareas']     # perhaps, can be several areas, let's take the first one
			for f in areas[0]['files']:
				process_file(f, dir, token)

def process_assignment(server_url, assignment, working_dir, users, token, progressObject):
	print(f"Saving assignment '{assignment['name']}' data") # such as "Exercises for Week 1"
	submissions_full = call_service(server_url, token, 'mod_assign_get_submissions', {'assignmentids[0]': assignment['id']}) # matching submissions with ext info
	submissions = submissions_full['assignments'][0]['submissions']  # submissions only
	
	for submission in submissions:
		progressObject.processAppEvents()
		if progressObject.wasCanceled():
			raise RuntimeError()
		process_submission(submission, os.path.join(working_dir, assignment['name']), users, token)

# NOTE: we should be inside the project dir here
def download(config, progressObject=StubProgressObject()):
	token = get_token(config['username'], config['password'], config['server_url'])
	courses = call_service(config['server_url'], token, 'core_course_get_courses_by_field', {'field': 'shortname', 'value': config['course_shortname']}) # list of all matching courses
	course_id = courses['courses'][0]['id'] # we presume that only one course matches the given shortname
	users_data = call_service(config['server_url'], token, 'core_enrol_get_enrolled_users', {'courseid': course_id})

	users = {} # id -> email-based username
	for user in users_data:
		new_uname = regex_rename(ast.literal_eval(config['username_conversions']), user['email']).replace('-', '_') # '-' is bad for JPlag files
		print(f"Renaming user: {user['email']} -> {new_uname}")
		users[user['id']] = new_uname

	assignments_full = call_service(config['server_url'], token, 'mod_assign_get_assignments', params={'courseids[0]': course_id}) # matching assignments with ext info
	assignments = assignments_full['courses'][0]['assignments'] # assignments only

	progressObject.setMaximum(len(assignments) - 1)
	
	try:
		for i, assignment in enumerate(assignments):
			progressObject.setValue(i)
			new_aname = regex_rename(ast.literal_eval(config['assignment_conversions']), assignment['name'])
			print(f"Renaming asignment: {assignment['name']} -> {new_aname}")
			assignment['name'] = new_aname
			process_assignment(config['server_url'], assignment, config['moodle_submissions_dir'], users, token, progressObject)
	except RuntimeError:
		print("Download process canceled")
