from less0n.models import *
from datetime import datetime


def init_db():
    # Create tables
    print('Creating all database tables...')
    db.create_all()

    # Create data
    print('Dumping all data...')

    # User
    users = {
        'zj2226': User(id='zj2226', avatar='', email='zj2226@columbia.edu', name='Zhijian Jiang', tokens=''),
    }
    for _, user in users.items():
        db.session.add(user)
    db.session.commit()


    # Roles
    role_student = Role(name='student')
    db.session.add(role_student)
    role_instructor = Role(name='instructor')
    db.session.add(role_instructor)
    db.session.commit()

    # Departments
    depts = {
        'AHAR': Department(id='AHAR', name='Art History and Archaeology',
                           url='http://www.columbia.edu/cu/arthistory/'),
        'COMS': Department(id='COMS', name='Computer Science',
                           url='https://www.cs.columbia.edu/'),
        'EALC': Department(id='EALC', name='East Asian Languages and Cultures',
                           url='http://ealac.columbia.edu/'),
        'ECON': Department(id='ECON', name='Economics',
                           url='http://econ.columbia.edu/'),
        'HSTB': Department(id='HSTB', name='History @Barnard',
                           url='https://history.barnard.edu/'),
        'HUMC': Department(id='HUMC', name='Humanities (College)'),
        'MATH': Department(id='MATH', name='Mathematics',
                           url='https://www.math.columbia.edu/'),
        'MUSI': Department(id='MUSI', name='Music',
                           url='https://music.columbia.edu/'),
        'STAT': Department(id='STAT', name='Statistics',
                           url='https://stat.columbia.edu/'),
    }
    for _, dept in depts.items():
        db.session.add(dept)
    db.session.commit()

    # Subjects
    subjs = {
        'ASCE': Subject(id='ASCE', name='Asian Civilization: East Asian'),
        'COMS': Subject(id='COMS', name='Computer Science'),
        'CSEE': Subject(id='CSEE', name='Computer Science and Electrical Engineering'),
        'ECON': Subject(id='ECON', name='Economics'),
        'HIST': Subject(id='HIST', name='History'),
        'HUMA': Subject(id='HUMA', name='Humanities'),
        'MATH': Subject(id='MATH', name='Mathematics'),
        'STAT': Subject(id='STAT', name='Statistics'),
    }
    for _, subj in subjs.items():
        db.session.add(subj)
    db.session.commit()

    # Courses
    courses = {
        'ASCE1359': Course(id='ASCE1359', subject=subjs['ASCE'], number='1359', department=depts['EALC'],
                           name='Introduction to East Asian Civilizations: China'),
        'ASCE1361': Course(id='ASCE1361', subject=subjs['ASCE'], number='1361', department=depts['EALC'],
                           name='Introduction to East Asian Civilizations: Japan'),
        'ASCE1363': Course(id='ASCE1363', subject=subjs['ASCE'], number='1363', department=depts['EALC'],
                           name='Introduction to East Asian Civilizations: Korea'),

        'COMS3157': Course(id='COMS3157', subject=subjs['COMS'], number='3157', department=depts['COMS'],
                           name='Advanced Programming'),
        'COMS3261': Course(id='COMS3261', subject=subjs['COMS'], number='3261', department=depts['COMS'],
                           name='Computer Science Theory'),
        'COMS4115': Course(id='COMS4115', subject=subjs['COMS'], number='4115', department=depts['COMS'],
                           name='Programming Languages and Translators'),
        'COMS4156': Course(id='COMS4156', subject=subjs['COMS'], number='4156', department=depts['COMS'],
                           name='Advanced Software Engineering'),
        'COMS4701': Course(id='COMS4701', subject=subjs['COMS'], number='4701', department=depts['COMS'],
                           name='Artificial Intelligence'),
        'COMS4705': Course(id='COMS4705', subject=subjs['COMS'], number='4705', department=depts['COMS'],
                           name='Natural Language Processing'),
        'COMS4771': Course(id='COMS4771', subject=subjs['COMS'], number='4771', department=depts['COMS'],
                           name='Machine Learning'),
        'CSEE3827': Course(id='CSEE3827', subject=subjs['CSEE'], number='3827', department=depts['COMS'],
                           name='Fundamentals of Computer Systems'),

        'ECON1105': Course(id='ECON1105', subject=subjs['ECON'], number='1105', department=depts['ECON'],
                           name='Principles of Economics'),

        'HIST1302': Course(id='HIST1302', subject=subjs['HIST'], number='1302', department=depts['HSTB'],
                           name='European History Since 1789'),

        'HUMA1001': Course(id='HUMA1001', subject=subjs['HUMA'], number='1001', department=depts['HUMC'],
                           name='Masterpieces of Western Literature and Philosophy I'),
        'HUMA1002': Course(id='HUMA1002', subject=subjs['HUMA'], number='1002', department=depts['HUMC'],
                           name='Masterpieces of Western Literature and Philosophy II'),
        'HUMA1121': Course(id='HUMA1121', subject=subjs['HUMA'], number='1121', department=depts['AHAR'],
                           name='Masterpieces of Western Art'),
        'HUMA1123': Course(id='HUMA1123', subject=subjs['HUMA'], number='1123', department=depts['MUSI'],
                           name='Masterpieces of Western Music'),

        'MATH1101': Course(id='MATH1101', subject=subjs['MATH'], number='1101', department=depts['MATH'],
                           name='Calculus I'),
        'MATH1102': Course(id='MATH1102', subject=subjs['MATH'], number='1102', department=depts['MATH'],
                           name='Calculus II'),
        'MATH1201': Course(id='MATH1201', subject=subjs['MATH'], number='1201', department=depts['MATH'],
                           name='Calculus III'),
        'MATH1202': Course(id='MATH1202', subject=subjs['MATH'], number='1202', department=depts['MATH'],
                           name='Calculus IV'),
        'MATH2010': Course(id='MATH2010', subject=subjs['MATH'], number='2010', department=depts['MATH'],
                           name='Linear Algebra'),

        'STAT4001': Course(id='STAT4001', subject=subjs['STAT'], number='4001', department=depts['STAT'],
                           name='Introduction to Probability and Statistics'),
    }
    for _, course in courses.items():
        db.session.add(course)
    db.session.commit()

    # Professors
    profs = {
        'dar27': Professor(uni='dar27', name='David Aaron Rios', department=depts['STAT'],
                           url='http://stat.columbia.edu/department-directory/name/david-rios/'),
        'db2711': Professor(uni='db2711', name='Daniel Bauer', department=depts['COMS'],
                            url='http://www.cs.columbia.edu/~bauer/',
                            avatar='https://www.cs.columbia.edu/wp-content/uploads/2017/02/cs_profile-225x225.jpg'),
        'etl2115': Professor(uni='etl2115', name='Ewan T. Lowe', department=depts['COMS'],
                             url=''),
        'jwl3': Professor(uni='jwl3', name='Jae Woo Lee', department=depts['COMS'],
                          url='http://www.cs.columbia.edu/~jae/',
                          avatar='http://www.cs.columbia.edu/~jae/images/jae-01.jpg'),
        'lt95': Professor(uni='lt95', name='Lisa S. Tiersten', department=depts['HSTB'],
                          url='https://barnard.edu/profiles/lisa-tiersten',
                          avatar='https://ma.europe.columbia.edu/sites/default/files/styles/cu_crop/public/content/images/Tiersten-Lisa.JPG'),
        'mak2191': Professor(uni='mak2191', name='Martha A. Kim', department=depts['COMS'],
                             url='http://www.cs.columbia.edu/~martha/',
                             avatar='http://engineering.columbia.edu/files/engineering/kim.jpg'),
        'mc3354': Professor(uni='mc3354', name='Michael John Collins', department=depts['COMS'],
                            url='http://www.cs.columbia.edu/~mcollins/',
                            avatar='http://engineering.columbia.edu/files/engineering/Collins.png'),
        'nv2274': Professor(uni='nv2274', name='Nakul Verma', department=depts['COMS'],
                            url='http://www.cs.columbia.edu/~verma/',
                            avatar='http://www.cs.columbia.edu/~verma/nakul_verma.png'),
        'rt2515': Professor(uni='rt2515', name='Richard Morse Townsend', department=depts['COMS'],
                            url='https://www.richardmtownsend.com/',
                            avatar='https://static.wixstatic.com/media/53f993_cc1ad3e6319d46ed929831fd9ffb98c0.jpg/v1/fill/w_414,h_496,al_c,q_80,usm_0.66_1.00_0.01/53f993_cc1ad3e6319d46ed929831fd9ffb98c0.jpg'),
        'tm2118': Professor(uni='tm2118', name='Tal G. Malkin', department=depts['COMS'],
                            url='http://www.cs.columbia.edu/~tal/',
                            avatar='https://industry.datascience.columbia.edu/sites/default/files/profiles/photos/Malkin_web.png'),
    }
    for _, prof in profs.items():
        db.session.add(prof)
    db.session.commit()

    # Teachings
    teachings = {
        1: Teaching(id=1, course=courses['CSEE3827'], professor=profs['mak2191']),
        2: Teaching(id=2, course=courses['COMS3157'], professor=profs['jwl3']),
        3: Teaching(id=3, course=courses['COMS3261'], professor=profs['tm2118']),
        4: Teaching(id=4, course=courses['STAT4001'], professor=profs['dar27']),
        5: Teaching(id=5, course=courses['COMS4701'], professor=profs['db2711']),
        6: Teaching(id=6, course=courses['COMS4705'], professor=profs['mc3354']),
        7: Teaching(id=7, course=courses['COMS4771'], professor=profs['nv2274']),
        8: Teaching(id=8, course=courses['COMS4115'], professor=profs['rt2515']),
        9: Teaching(id=9, course=courses['COMS4156'], professor=profs['etl2115']),
        10: Teaching(id=10, course=courses['HIST1302'], professor=profs['lt95']),
        11: Teaching(id=11, course=courses['COMS4156'], professor=profs['db2711']),
    }
    for _, teaching in teachings.items():
        db.session.add(teaching)
    db.session.commit()

    # Terms
    terms = {
        'Fall 2016': Term(id='Fall 2016'),
        'Spring 2017': Term(id='Spring 2017'),
        'Summer 2017': Term(id='Summer 2017'),
        'Fall 2017': Term(id='Fall 2017'),
        'Spring 2018': Term(id='Spring 2018'),
    }
    for _, term in terms.items():
        db.session.add(term)
    db.session.commit()

    # Tags
    tags = {
        1: Tag(id=1, text="Interesting"),
        2: Tag(id=2, text="Hot"),
        3: Tag(id=3, text="Ace Professor"),
    }
    for _, tag in tags.items():
        db.session.add(tag)
    db.session.commit()

    # Comments
    comments = {
        1: Comment(id=1, teaching=teachings[9], term=terms['Spring 2018'],
                   title='Great course',
                   content='A very good teacher!',
                   rating=5, workload=1, grade='A+', user=users['zj2226'], timestamp=datetime.now(),
                   tags=[tags[1], tags[2]]),
        2: Comment(id=2, teaching=teachings[11], term=terms['Spring 2018'],
                   title='Super excited',
                   content='Excited!',
                   rating=4, workload=2, grade='A', user=users['zj2226'], timestamp=datetime.now(),
                   tags=[tags[1], tags[3]]),
        3: Comment(id=3, teaching=teachings[11], term=terms['Spring 2018'],
                   title='Wow',
                   content='Excellent!',
                   rating=4, workload=1, grade='A+', user=users['zj2226'], timestamp=datetime.now(),
                   tags=[tags[1]]),
        4: Comment(id=4, teaching=teachings[9], term=terms['Spring 2018'],
                   title='Learned nothing',
                   content='A waste of time and money',
                   rating=1, workload=2, grade='B-', user=users['zj2226'], timestamp=datetime.now(),
                   tags=[]),
    }
    for _, comment in comments.items():
        db.session.add(comment)
    db.session.commit()

    print('Done!')


def drop_db():
    db.session.remove()
    db.drop_all()


if __name__ == '__main__':
    drop_db()
    init_db()
