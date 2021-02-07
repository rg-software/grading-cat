# config.py MUST define:
# username, password, server_url, course_shortname, working_dir

# NOTE: JPLAG needs the following folder structure: ROOT/user1/*.java, ROOT/user2/*.java, ...
# It can also handle ROOT/*/user1/*.java, ROOT/*/user2/*.java (with -S flag)
# By default, it doesn't check subdirectories, but it can be turned on (-r)
# CHECK Jplag documentation: https://github.com/jplag/jplag
# basic run: java  -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -s -l java19 docs
# (use recursive mode; for some reason -s needs also another switch such as -l)
# it will recurse as deeply as necessary


#https://docs.moodle.org/dev/Web_service_API_functions#Core_web_service_functions

#The api documentation that provides more extensive documentation on not only what the required parameters are for all the available webservice functions but also the expected response and their structures in both REST and XML-RPC is accessible from the moodle site.
# For access to these docs you must have admin access as they are found in admin submenu located at :
# site administration > Plugins > Web services > API Documentation

import requests
import os
import config

def get_token(username, password, server_url):
	response = requests.get(server_url + '/login/token.php', params={'username': username, 'password': password, 'service': 'moodle_mobile_app'})
	return response.json()['token']

def call_service(server_url, token, function, params):
	p = params
	p.update({'wstoken': token, 'wsfunction': function, 'moodlewsrestformat': 'json'})
	response = requests.get(server_url + '/webservice/rest/server.php', params=p)
	return response.json()

def process_file(f, working_dir, token):
	filename = f['filename']
	download_url = f['fileurl'] + "?token=" + token
	
	if not os.path.exists(working_dir):
		os.makedirs(working_dir)

	# TODO: checksum testing (?)
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

def process_assignment(server_url, assignment, working_dir, users, token):
	print(f"Processing assignment: {assignment['name']}") # such as "Exercises for Week 1"
	submissions_full = call_service(server_url, token, 'mod_assign_get_submissions', {'assignmentids[0]': assignment['id']}) # matching submissions with ext info
	submissions = submissions_full['assignments'][0]['submissions']  # submissions only
	
	for submission in submissions:
		process_submission(submission, os.path.join(working_dir, assignment['name']), users, token)


#############################################################################

token = get_token(config.username, config.password, config.server_url)

courses = call_service(config.server_url, token, 'core_course_get_courses_by_field', {'field': 'shortname', 'value': config.course_shortname}) # list of all matching courses
course_id = courses['courses'][0]['id'] # we presume that only one course matches the given shortname

users_data = call_service(config.server_url, token, 'core_enrol_get_enrolled_users', {'courseid': course_id})
users = {} # id -> email
for user in users_data:
	users[user['id']] = user['email']

assignments_full = call_service(config.server_url, token, 'mod_assign_get_assignments', params={'courseids[0]': course_id}) # matching assignments with ext info
assignments = assignments_full['courses'][0]['assignments'] # assignments only

for assignment in assignments:
	process_assignment(config.server_url, assignment, config.working_dir, users, token)
