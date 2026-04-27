def recommend_companies(skills):

    company_db = {

        # FRONTEND
        "html": ["Wipro", "Capgemini"],
        "css": ["TCS", "Infosys"],
        "javascript": ["Adobe", "PayPal"],
        "react": ["Meta", "Google"],
        "bootstrap": ["Accenture"],
        "tailwind": ["Razorpay"],

        # BACKEND
        "node": ["Flipkart", "Paytm"],
        "nodejs": ["Flipkart", "Paytm"],
        "express": ["Swiggy", "Zomato"],
        "mongodb": ["Uber", "Airbnb"],
        "mysql": ["Oracle", "Amazon"],

        # 🔥 APP DEVELOPMENT (IMPORTANT FIX)
        "android": ["Google", "Samsung", "PhonePe"],
        "kotlin": ["Google", "Zomato"],
        "java": ["Infosys", "TCS"],
        "firebase": ["Google", "Swiggy"],
        "xml": ["Samsung", "Paytm"],

        # DATA / AI
        "python": ["Google", "Amazon", "Microsoft", "Flipkart"],
        "machinelearning": ["Google AI", "Meta AI", "OpenAI"],
        "dataanalysis": ["Deloitte", "KPMG", "EY"],

        # GENERAL
        "git": ["Microsoft"],
        "github": ["GitHub", "Microsoft"]
    }

    # 🔥 NORMALIZE FUNCTION (VERY IMPORTANT)
    def normalize(skill):
        return skill.lower().replace(".", "").replace(" ", "")

    companies = []

    for skill in skills:
        skill_clean = normalize(skill)

        for key in company_db:
            if normalize(key) in skill_clean:
                companies.extend(company_db[key])

    return list(set(companies))
