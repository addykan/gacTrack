# ALL CODE CREDIT GOES TO THE ORIGINAL CREATOR apozharski
# original github: https://github.com/apozharski/gradescope-api/blob/master/pyscope/pyscope.py

import requests
from enum import Enum
from bs4 import BeautifulSoup

class ConnState(Enum):
    INIT = 0
    LOGGED_IN = 1

class LoadedCapabilities(Enum):
    ASSIGNMENTS = 0
    ROSTER = 1

class GSAssignment():

    def __init__(self, name, aid, points, percent_graded, complete, regrades_on, course):
        '''Create a assignment object'''
        self.name = name
        self.aid = aid
        self.points = points
        self.percent_graded = percent_graded
        self.complete = complete
        self.regrades_on = regrades_on
        self.course = course
        self.questions = []

class GSCourse():

    def __init__(self, cid, name, shortname, year, session):
        '''Create a course object that has lazy eval'd assignments'''
        self.cid = cid
        self.name = name
        self.shortname = shortname
        self.year = year
        self.session = session
        self.assignments = {}
        self.roster = {} # TODO: Maybe shouldn't dict. 
        self.state = set()

    def _lazy_load_assignments(self):
            '''
            Load the assignment dictionary from assignments. This is done lazily to avoid slowdown caused by getting
            all the assignments for all classes. Also makes us less vulnerable to blocking.
            '''
            assignment_resp = self.session.get('https://www.gradescope.com/courses/'+self.cid)
            parsed_assignment_resp = BeautifulSoup(assignment_resp.text, 'html.parser')
            
            assignment_table = []
            for assignment_row in parsed_assignment_resp.findAll('tr')[1:]:
                # print(assignment_row)
                # use aria-label to get name of assignment
                # use submissionTimeChart--dueDate
                # use submissionStatus-

                td = assignment_row.find('td')
                # print(td)

                submissionStatus = td['class']
                # print(submissionStatus)

                if len(submissionStatus) < 2 or submissionStatus[1] == 'submissionStatus-complete':
                    continue
                
                button = assignment_row.find('button')
                a = assignment_row.find('a')

                if button and not a:
                    assignmentName = button['data-assignment-title']
                else:
                    assignmentName = a.string
                
                # print(assignmentName)
                timeRemaining = assignment_row.find('span')
                # print()
                self.assignments[assignmentName] = timeRemaining.string

            # print("-----------------------DONE WITH ONE CLASS-----------------------")
            return

class GSAccount():
    '''A class designed to track the account details (instructor and student courses'''

    def __init__(self, email, session):
        self.email = email
        self.session = session
        self.instructor_courses = {}
        self.student_courses = {}
        self.output = dict()

    def get_courses(self):
        pageContent = self.session.get('https://www.gradescope.com/')
        soup = str(BeautifulSoup(pageContent.text, 'html.parser'))
        studentCoursesIndex = soup.find('<h1 class="pageHeading">Student Courses</h1>')
        soup = soup[studentCoursesIndex:]
        start = soup.find('<h2 class="courseList--term pageSubheading"')
        end = soup.find('</a><button class="courseBox courseBox-new js-enrollInCourse" type="button">')
        soup = soup[start:end]
        bsoup = BeautifulSoup(soup, 'html.parser')
        courses = bsoup.find_all('a')
        for course in courses:
            cid = course['href'][9:]
            name = course.find('h4').string
            shortname = course.find('h3').string
            self.student_courses[shortname] = [(GSCourse(cid, name, shortname, '2021', self.session)), 'https://www.gradescope.com/courses/' + cid]
        self.get_assignments()
        
    def get_assignments(self):
        for course in self.student_courses:
            courseObj = self.student_courses[course]
            courseObj[0]._lazy_load_assignments()
            print(courseObj[0].assignments)


class GradeScopeScraper(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.state = ConnState.INIT
        self.account = None

    def automateLogIn(self):
        # search for the input tags to input email and password in "name" field
        # look in console to see if it's a POST request and view params
        init_resp = self.session.get("https://www.gradescope.com/")
        parsed_init_resp = BeautifulSoup(init_resp.text, 'html.parser')
        for form in parsed_init_resp.find_all('form'):
            if form.get("action") == "/login":
                for inp in form.find_all('input'):
                    if inp.get('name') == "authenticity_token":
                        auth_token = inp.get('value')
        login_data = {
            "utf8": "✓",
            "session[email]": self.email,
            "session[password]": self.password,
            "session[remember_me]": 0,
            "commit": "Log In",
            "session[remember_me_sso]": 0,
            "authenticity_token": auth_token,
        }
        login_resp = self.session.post("https://www.gradescope.com/login", params=login_data)
        if len(login_resp.history) != 0:
            if login_resp.history[0].status_code == requests.codes.found:
                self.state = ConnState.LOGGED_IN
                self.account = GSAccount(self.email, self.session)
                self.account.get_courses()
                return True
        else:
            return False

def main():
    # 1. scrape gradescope -> get a userid, check user database for 
    # 2. call autolab api -> might require token refresh
    # 3. call canvas api -> might require token refresh
    # 4. perform sorting
    # call the API -> if 401, then refresh token (take access and refresh) and call it again - 
    # if expiration time has exceed since login, then just get new access token

    # dict (course code:)
    email = "kerenh@andrew.cmu.edu"
    password = "anudaisc00l!"
    GSS = GradeScopeScraper(email, password)
    GSS.automateLogIn()

if __name__ == '__main__':
    main()
    