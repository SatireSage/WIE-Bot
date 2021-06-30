import pandas as pd


def member_info():
    Member = pd.read_csv('DEEDhacks 2021 Registration!.csv',
                         usecols=['University/Institution Email:', 'First Name:', 'Last Name:'],
                         dtype={"col1": str, "col2": str})
    Member.to_json('Members.json')


def mentor_info():
    Mentor = pd.read_csv('DEEDhacks 2021 Mentor Registration!.csv',
                         usecols=['University/Institution Email (for post-secondary students only) If you have already graduated please provide an email we can best reach you at', 'First Name', 'Last Name'],
                         dtype={"col1": str, "col2": str})
    Mentor.to_json('Mentors.json')


member_info()
mentor_info()
