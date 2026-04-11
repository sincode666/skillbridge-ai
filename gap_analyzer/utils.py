def find_missing_skills(user_skills, company_skills):

    # break all user skills into individual words
    user_words = []
    for skill in user_skills:
        words = skill.lower().strip().split()
        for word in words:
            if len(word) > 1:
                user_words.append(word)

    company = [s.lower().strip() for s in company_skills]

    missing = []
    for skill in company:
        # check if the skill word exists anywhere in user words
        skill_words = skill.split()   # handles multi word like "machine learning"
        match_found = all(word in user_words for word in skill_words)
        if not match_found:
            missing.append(skill)

    if len(missing) == 0:
        verdict = "GOOD TO APPLY"
        message = "Your skills match all requirements. Go ahead and apply!"
    elif len(missing) == len(company):
        verdict = "NOT READY YET"
        message = "Your skills do not match this job. Build more skills first."
    elif len(missing) <= 2:
        verdict = "ALMOST READY"
        message = "Learn " + str(missing) + " and you are good to go!"
    else:
        verdict = "SKILL GAP EXISTS"
        message = "You are missing " + str(len(missing)) + " skills."

    return {
        "missing": missing,
        "verdict": verdict,
        "message": message
    }