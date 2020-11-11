#https://docs.moodle.org/dev/Web_service_API_functions#Core_web_service_functions

#The api documentation that provides more extensive documentation on not only what the required parameters are for all the available webservice functions but also the expected response and their structures in both REST and XML-RPC is accessible from the moodle site.
# For access to these docs you must have admin access as they are found in admin submenu located at :
# site administration > Plugins > Web services > API Documentation

import requests

def get_token(username, password, server_url):
    response = requests.get(server_url + '/login/token.php', params={'username': username, 'password': password, 'service': 'moodle_mobile_app'})
    return response.json()['token']

def call_service(token, function, params):
    p = params
    p.update({'wstoken': token, 'wsfunction': function, 'moodlewsrestformat': 'json'})
    response = requests.get(server_url + '/webservice/rest/server.php', params=p)
    return response.json()

def download_file(url, filename):
    r = requests.get(url)
#     if r.status_code != 200:
#         return False
    with open(filename, 'wb') as f:
        f.write(r.content)
#     return True

username = 'mozgovoy'
password = 'p******28'
server_url = 'https://elms.u-aizu.ac.jp'
course_shortname = 'SE06_19114148'

token = get_token(username, password, server_url)
#print(token)
r = call_service(token, 'core_course_get_courses_by_field', {'field': 'shortname', 'value': course_shortname})
# returns a list of all matching courses
course_id = r['courses'][0]['id'] # we presume that only one course matches the given shortname

#print(course_id)
r = call_service(token, 'mod_assign_get_assignments', params={'courseids[0]': course_id})

# also returns a list of all matching courses, so let's take the first item and then 'assignments' dictionary
assignments = r['courses'][0]['assignments']
#print(len(a)) # number of assignments (~15 for my course)
# a = 
#print(a[0])
# a[0] = {'id': 8, 'name': 'Upload Solutions for Exercises 1.x' ...}

assignment_id = assignments[0]['id'] # for example, let's take Assignment 0 (there are many assignments)
#print(assignment_id)
submission = call_service(token, 'mod_assign_get_submissions', {'assignmentids[0]': assignment_id})
# print(jr)
# here we have a list of submissions

sb = submission['assignments'][0]['submissions']  # okay, the "real" submissions list (~ 37, e.g.)
# each element (such as sb[0])
# has important fields:
# userid, gradingstatus (such as 'notgraded')
# also: id, attemptnumber, timecreated, timemodified, status (such as 'new'), 

# here I need to get 'plugins' and find a plugin called 'fileareas'

my_sb = sb[4] # let's consider just one submission 4

for plugin in my_sb['plugins']:
    if 'fileareas' in plugin:       # it means there is a file attached
        areas = plugin['fileareas']
        #for area in areas:         # perhaps, can be several areas, let's take the first one
        files = areas[0]['files']

        for f in files:
            #print(f['fileurl']) # prints https://elms.u-aizu.ac.jp/webservice/pluginfile.php/15026/assignsubmission_file/submission_files/159/s1220187-e1.zip
            filename = f['filename']
            download_url = f['fileurl'] + "?token=" + token
            print(download_url)
            download_file(download_url, filename)

#            response = requests.get(server_url + '/webservice/pluginfile.php', params={'token': token})


#print(course_id)
#print(r['id'])

# jr = call_service(token, 'core_enrol_get_enrolled_users', {'courseid': 3701})

# jr = call_service(token, 'core_enrol_get_users_courses', {})
#{'id':3701})


#print(jr)

# print(jr) #enrolled users
# mod_assign_get_submissions	2.5	Returns the submissions for assignments
# mod_assign_get_assignments
# core_course_get_contents

#, headers={'Content-Type': 'application/json'})

#https://docs.moodle.org/dev/Web_service_API_functions
 
# arguments?

#https://www.yourmoodle.com/login/token.php?username=USERNAME&password=PASSWORD&service=SERVICESHORTNAME

#https://elms.u-aizu.ac.jp/login/token.php?username=mozgovoy&password=pursitie9c28&service=moodle_mobile_app
# {"token":"9ce32a0ab06898b03b4e0ea05405f205","privatetoken":"QT3p6pXcL4LVgEfjXqnh5R3bbjPsRTU4UaAmljNxYptEEDfapDjdhTkH6Pc5Mv2o"}



#            requests.get(ServerUrl + '/update_agents', params={'devicename': DeviceName}, headers={'Content-Type': 'application/json'})
# username
# password
# service shortname - The service shortname is usually hardcoded in the pre-build service (db/service.php files). Moodle administrator will be able to edit shortnames for service created on the fly: MDL-29807. If you want to use the Mobile service, its shortname is moodle_mobile_app. Also useful to know, the database shortname field can be found in the table named external_services.

# 1) Login - get user token; use "moodle_mobile_app"


#
        # try:
        #     Logger.info(f"Requesting next task from {server_url} for {device_name}")
        #     response = requests.get(server_url + '/provide_next_task', params={'devicename': device_name}, headers={'Content-Type': 'application/json'})

        #     jr = response.json()
        #     if not jr['empty']:
        #         process_task(jr)

        #     Logger.info(f"Sleeping for {config.SleepTime} sec")
        #     time.sleep(config.SleepTime)
        # except:
        #     Logger.error(f"Cannot connect to the server {server_url}, exiting main thread")
        #     break

