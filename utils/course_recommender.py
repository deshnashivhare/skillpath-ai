def recommend_courses(missing_skills):

    course_db = {

        "react": {
            "Beginner": ("React Basics (YouTube)", "https://www.youtube.com/watch?v=bMknfKXIFA8"),
            "Intermediate": ("React Project", "https://www.youtube.com/watch?v=w7ejDZ8SWv8"),
            "Advanced": ("React Docs", "https://react.dev")
        },

        "javascript": {
            "Beginner": ("JS Full Course", "https://www.youtube.com/watch?v=W6NZfCO5SIk"),
            "Intermediate": ("JS Projects", "https://www.youtube.com/watch?v=jS4aFq5-91M"),
            "Advanced": ("MDN JS Docs", "https://developer.mozilla.org/en-US/docs/Web/JavaScript")
        },

        "node": {
            "Beginner": ("Node.js Basics", "https://www.youtube.com/watch?v=TlB_eWDSMt4"),
            "Intermediate": ("Node API Project", "https://www.youtube.com/watch?v=Oe421EPjeBE"),
            "Advanced": ("Node Docs", "https://nodejs.org/en/docs")
        },

        "mongodb": {
            "Beginner": ("MongoDB Course", "https://www.youtube.com/watch?v=ofme2o29ngU"),
            "Intermediate": ("MongoDB Project", "https://www.youtube.com/watch?v=-56x56UppqQ"),
            "Advanced": ("MongoDB Docs", "https://www.mongodb.com/docs")
        },

        "python": {
            "Beginner": ("Python Full Course", "https://www.youtube.com/watch?v=_uQrJ0TkZlc"),
            "Intermediate": ("Python Projects", "https://www.youtube.com/watch?v=8ext9G7xspg"),
            "Advanced": ("Python Docs", "https://docs.python.org/3/")
        },

        "android": {
            "Beginner": ("Android Dev Course", "https://www.youtube.com/watch?v=fis26HvvDII"),
            "Intermediate": ("Android Project", "https://www.youtube.com/watch?v=BBWyXo-3JGQ"),
            "Advanced": ("Android Docs", "https://developer.android.com/docs")
        },

        "kotlin": {
            "Beginner": ("Kotlin Basics", "https://www.youtube.com/watch?v=F9UC9DY-vIU"),
            "Intermediate": ("Kotlin Project", "https://www.youtube.com/watch?v=EExSSotojVI"),
            "Advanced": ("Kotlin Docs", "https://kotlinlang.org/docs")
        },

        "firebase": {
            "Beginner": ("Firebase Tutorial", "https://www.youtube.com/watch?v=9kRgVxULbag"),
            "Intermediate": ("Firebase Project", "https://www.youtube.com/watch?v=m_u6P5k0vP0"),
            "Advanced": ("Firebase Docs", "https://firebase.google.com/docs")
        },

        "mysql": {
            "Beginner": ("MySQL Course", "https://www.youtube.com/watch?v=7S_tz1z_5bA"),
            "Intermediate": ("SQL Practice", "https://www.hackerrank.com/domains/sql"),
            "Advanced": ("MySQL Docs", "https://dev.mysql.com/doc/")
        }
    }

    def normalize(skill):
        return skill.lower().replace(".", "").replace(" ", "")

    recommendations = {}

    for skill in missing_skills:
        skill_clean = normalize(skill)

        for key in course_db:
            if normalize(key) in skill_clean:
                recommendations[skill] = course_db[key]

    return recommendations
