# Reference:
# - http://bitwiser.in/2015/09/09/add-google-login-in-flask.html
# - https://stackoverflow.com/questions/34235590/how-do-you-restrict-google-login-oauth2-to-emails-from-a-specific-google-apps

from less0n import app, helpers
from less0n.models import *
import json
import logging
import re
from collections import defaultdict
from flask import url_for, redirect, render_template, session, request, flash, jsonify, abort
from flask_login import login_required, login_user, logout_user, current_user
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from werkzeug.routing import BaseConverter
from config import Auth


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=app.config['GOOGLE_OAUTH_REDIRECT_URI'])
    oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri=app.config['GOOGLE_OAUTH_REDIRECT_URI'], scope=Auth.SCOPE)
    return oauth


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    session['oauth_redirect'] = request.args.get('redirect') or url_for('index')
    if current_user.is_authenticated:
        return redirect(session['oauth_redirect'])

    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline', prompt='select_account')
    session['oauth_state'] = state
    return redirect(auth_url)


@app.route('/oauth')
def oauth2callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(session.get('oauth_redirect', url_for('index')))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            uni, hd = email.split('@')
            if (hd != 'columbia.edu' and hd != 'barnard.edu') or not re.compile(r'([a-z]{2,3}\d{1,4})').match(uni):
                flash('You cannot login using this email. Please use Lionmail instead.', 'error')
                return redirect(session.get('oauth_redirect', url_for('index')))

            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.id = user_data['id']
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(session.get('oauth_redirect', url_for('index')))
        return 'Could not fetch your information.'


@app.route('/logout')
@login_required
def logout():
    redirect_url = request.args.get('redirect') or url_for('index')
    logout_user()
    session.clear()
    return redirect(redirect_url)


@app.route('/department', methods=["GET", "POST"])
def department():
    """
    Render the template with all departments if it is the "GET" request.
    Render the template with departments having keywords if it is the "POST" request.
    :return: rendered template
    """
    if request.method == "GET":
        all_depts = Department.query.all()
        context = {'depts': all_depts}
        return render_template('department.html', **context)

    elif request.method == "POST":
        dept_keyword = request.form['dept_keyword']
        depts = Department.query.filter(Department.name.contains(dept_keyword)).all()
        context = {'depts': depts}
        return render_template('department.html', **context)


@app.route('/dept/<regex("[A-Za-z]{4}"):dept_arg>/')
def department_course(dept_arg):
    dept = Department.query.filter_by(id=dept_arg.upper()).first()
    if dept is None:
        return redirect(url_for('department'))

    statistics = {}
    all_courses = Course.query.filter_by(department=dept).all()
    for c in all_courses:
        sum_rating = sum_workload = sum_grade = 0
        count_all_comments = count_nonempty_comments = 0
        statistics[c] = {}

        all_teachings = Teaching.query.filter_by(course=c).all()
        if len(all_teachings) == 0:  # If there is no teaching, return -1 for rating, workload and grade
            statistics[c]['rating'] = statistics[c]['workload'] = statistics[c]['grade'] = -1
            statistics[c]['comment'] = 0
        else:  # Otherwise, iterate each teaching
            for teaching in all_teachings:
                all_comments = teaching.comments
                for comment in all_comments:  # Iterate each comment
                    count_all_comments += 1
                    sum_rating += comment.rating
                    sum_workload += comment.workload
                    sum_grade += helpers.letter_grade_to_numeric(comment.grade)
                    if not (not comment.title.strip()) and not (not comment.content.strip()):
                        count_nonempty_comments += 1

            if count_all_comments == 0:  # If there is no comment, return -1 for rating, workload and grade
                statistics[c]['rating'] = statistics[c]['workload'] = statistics[c]['grade'] = -1
                statistics[c]['comment'] = 0
            else:
                statistics[c]['rating'] = sum_rating / count_all_comments
                statistics[c]['workload'] = sum_workload / count_all_comments
                statistics[c]['grade'] = sum_grade / count_all_comments
                statistics[c]['comment'] = count_nonempty_comments

    context = {
        'dept': dept,
        'courses': statistics,
    }
    return render_template('department-course.html', **context)


@app.route('/course/<regex("[A-Za-z]{4}[A-Za-z0-9]{4,5}"):course_arg>/')
def course(course_arg):
    c = Course.query.filter_by(id=course_arg.upper()).first()
    if c is None:
        return redirect(url_for('department'))
    context = {
        'course': c,
    }
    return render_template('course-detail.html', **context)


@app.route('/course/<regex("[A-Za-z]{4}[A-Za-z0-9]{4,5}"):course_arg>/json/')
def course_json(course_arg):
    c = Course.query.filter_by(id=course_arg.upper()).first()
    if c is None:
        abort(404)

    all_teachings = Teaching.query.filter_by(course=c).all()
    all_statistics = {}

    # Statistics of all professors
    all_profs_sum_rating = all_profs_sum_workload = all_profs_sum_grade = 0
    all_profs_tags_count = {}
    all_profs_count_all_comments = 0
    all_profs_nonempty_comments = []

    for teaching in all_teachings:
        # Statistics of the current professor in the current teaching
        # Each professor in all_teachings is unique
        cur_prof = teaching.professor
        cur_prof_sum_rating = cur_prof_sum_workload = cur_prof_sum_grade = 0
        cur_prof_tags_count = {}
        cur_prof_count_all_comments = 0
        cur_prof_nonempty_comments = []

        # Accumulate each ratings
        all_comments = teaching.comments
        for comment in all_comments:
            cur_prof_sum_rating += comment.rating
            cur_prof_sum_workload += comment.workload
            cur_prof_sum_grade += helpers.letter_grade_to_numeric(comment.grade)
            cur_prof_count_all_comments += 1
            all_profs_sum_rating += comment.rating
            all_profs_sum_workload += comment.workload
            all_profs_sum_grade += helpers.letter_grade_to_numeric(comment.grade)
            all_profs_count_all_comments += 1

            # Count the frequency of all tags
            for tag in comment.tags:
                cur_prof_tags_count[tag] = cur_prof_tags_count.get(tag, 0) + 1
                all_profs_tags_count[tag] = all_profs_tags_count.get(tag, 0) + 1

            # Only show comments that have titles or contents
            if not (not comment.title.strip()) and not (not comment.content.strip()):
                json_comment = {
                    'title': comment.title,
                    'content': comment.content,
                    'term': comment.term.id,
                    'rating': comment.rating,
                    'workload': comment.workload,
                    'grade': comment.grade,
                    'timestamp': comment.timestamp,
                }
                cur_prof_nonempty_comments.append(json_comment)
                all_profs_nonempty_comments.append(json_comment)

        # Store ratings of the current professor
        all_statistics[cur_prof] = {
            'sum_rating': cur_prof_sum_rating,
            'sum_workload': cur_prof_sum_workload,
            'sum_grade': cur_prof_sum_grade,
            'tags_count': cur_prof_tags_count,
            'count_all_comments': cur_prof_count_all_comments,
            'nonempty_comments': cur_prof_nonempty_comments,
        }

    # Return JSON
    ret = []
    # Return statistics of all professors
    all_profs_tags = [tag.text for tag in sorted(all_profs_tags_count, key=all_profs_tags_count.get, reverse=True)][:10]
    ret.append({
        'name': 'All Instructors',
        'uni': None,
        'avatar': '',
        'rating': -1 if all_profs_count_all_comments == 0 else all_profs_sum_rating / all_profs_count_all_comments,
        'workload': -1 if all_profs_count_all_comments == 0 else all_profs_sum_workload / all_profs_count_all_comments,
        'grade': -1 if all_profs_count_all_comments == 0 else all_profs_sum_grade / all_profs_count_all_comments,
        'tags': all_profs_tags,
        'comments': all_profs_nonempty_comments,
    })
    # Return statistics of each professor
    for cur_prof, cur_prof_statistics in all_statistics.items():
        # Sort and find the most frequent tags
        cur_prof_tags_count = cur_prof_statistics['tags_count']
        cur_prof_tags = [tag.text for tag in sorted(cur_prof_tags_count, key=cur_prof_tags_count.get, reverse=True)][:10]
        cur_prof_count_all_comments = cur_prof_statistics['count_all_comments']

        ret.append({
            'name': cur_prof.name,
            'uni': cur_prof.uni,
            'avatar': cur_prof.avatar,
            'rating': -1 if cur_prof_count_all_comments == 0 else cur_prof_statistics['sum_rating'] / cur_prof_count_all_comments,
            'workload': -1 if cur_prof_count_all_comments == 0 else cur_prof_statistics['sum_workload'] / cur_prof_count_all_comments,
            'grade': -1 if cur_prof_count_all_comments == 0 else cur_prof_statistics['sum_grade'] / cur_prof_count_all_comments,
            'tags': cur_prof_tags,
            'comments': cur_prof_statistics['nonempty_comments'],
        })
    return jsonify(ret)




@app.route('/search/', methods=['GET'])
def search():
    """
    Search department, subject, professor and course
    :param
        request example
            {'dept': 'COMS', 'subj': 'COMS', 'prof': 'daniel', course: 'COMS4156', }
    :return: rendered template

    Examples:
        /search/?prof=daniel
    """
    context = {}
    context['count'] = 0

    # get keywords
    dept = request.args.get('dept')
    subj = request.args.get('subj')
    prof = request.args.get('prof')
    course = request.args.get('course')

    if dept != None:
        depts = re.split(',\s*|\s+', dept)  # split keywords by , |\s
        results = []
        for dept in depts:
            for result in Department.query.filter((Department.id.like("%%" + dept + "%")) |
                                                  (Department.name.like("%%" + dept + "%"))).all():
                results.append(result)
        context['depts'] = results
        context['count'] += len(results)

    if subj != None:
        subjs = re.split(',\s*|\s+', subj)
        results = []
        for subj in subjs:
            for result in Subject.query.filter((Subject.id.like("%%" + subj + "%")) |
                                               (Subject.name.like("%%" + subj + "%"))).all():
                results.append(result)
        context['subjs'] = results
        context['count'] += len(results)

    if prof != None:
        profs = re.split(',\s*|\s+', prof)
        results = []
        for prof in profs:
            for result in Professor.query.filter((Professor.uni.like("%%" + prof + "%")) |
                                                 (Professor.name.like("%%" + prof + "%"))).all():
                results.append(result)
        context['profs'] = results
        context['count'] += len(results)

    if course != None:
        courses = re.split(',\s*|\s+', course)
        results = []
        for course in courses:
            for result in Course.query.filter((Course.id.like("%%" + course + "%")) |
                                              (Course.name.like("%%" + course + "%"))).all():
                results.append(result)
        context['courses'] = results
        context['count'] += len(results)
    return render_template('search-result.html', **context)


@app.route('/prof/<regex("[A-Za-z]{2,3}[0-9]{1,4}"):prof_arg>/')
def prof(prof_arg):
    prof = Professor.query.filter_by(uni=prof_arg.lower()).first()
    if prof is None:
        abort(404)

    all_teachings = Teaching.query.filter_by(professor=prof).all()
    statistics = {}  # Statistics of each course
    # Statistics of all courses
    all_courses_sum_rating = all_courses_sum_workload = all_courses_sum_grade = all_courses_count_all_comments = 0
    all_courses_tags_count = {}
    all_statistics = {}

    # Statistics of all courses (i.e. all teachings)
    for teaching in all_teachings:
        c = teaching.course
        cur_course_sum_rating = cur_course_sum_workload = cur_course_sum_grade = 0
        cur_course_count_all_comments = cur_course_count_nonempty_comments = 0
        statistics[c] = {}

        all_comments = teaching.comments
        for comment in all_comments:  # Iterate each comment
            cur_course_count_all_comments += 1
            cur_course_sum_rating += comment.rating
            cur_course_sum_workload += comment.workload
            cur_course_sum_grade += helpers.letter_grade_to_numeric(comment.grade)
            if not (not comment.title.strip()) and not (not comment.content.strip()):
                cur_course_count_nonempty_comments += 1

            all_courses_count_all_comments += 1
            all_courses_sum_rating += comment.rating
            all_courses_sum_workload += comment.workload
            all_courses_sum_grade += helpers.letter_grade_to_numeric(comment.grade)
            # Count the frequency of all tags
            for tag in comment.tags:
                all_courses_tags_count[tag] = all_courses_tags_count.get(tag, 0) + 1

        # Calculate ratings for the current course
        if cur_course_count_all_comments == 0:  # If there is no comment, return N/A for rating, workload and grade
            statistics[c]['rating'] = statistics[c]['workload'] = statistics[c]['grade'] = -1
            statistics[c]['comment'] = 0
        else:
            statistics[c]['rating'] = cur_course_sum_rating / cur_course_count_all_comments
            statistics[c]['workload'] = cur_course_sum_workload / cur_course_count_all_comments
            statistics[c]['grade'] = cur_course_sum_grade / cur_course_count_all_comments
            statistics[c]['comment'] = cur_course_count_nonempty_comments

    # Calculate ratings for the professor
    all_statistics['tags'] = [tag.text for tag in sorted(all_courses_tags_count, key=all_courses_tags_count.get, reverse=True)][:10]
    if all_courses_count_all_comments == 0:  # If there is no comment, return N/A for rating, workload and grade
        all_statistics['rating'] = all_statistics['workload'] = all_statistics['grade'] = -1
    else:
        all_statistics['rating'] = all_courses_sum_rating / all_courses_count_all_comments
        all_statistics['workload'] = all_courses_sum_workload / all_courses_count_all_comments
        all_statistics['grade'] = all_courses_sum_grade / all_courses_count_all_comments

    context = {
        'prof': prof,
        'courses': statistics,
        'prof_stats': all_statistics,
    }
    return render_template('faculty-page.html', **context)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.errorhandler(404)
def page_not_found_error(e):
    logging.exception('Page not found.')
    return render_template('404.html'), 404
