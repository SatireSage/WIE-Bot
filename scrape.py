import pandas as pd


def member_info():
    Member = pd.read_csv('DEEDhacks 2021 Registration!.csv',
                         usecols=['University/Institution Email:', 'First Name:', 'Last Name:'],
                         dtype={"col1": str, "col2": str})
    Member.to_json('Members.json')


def mentor_info():
    Mentor = pd.read_csv('DEEDhacks 2021 Mentor Registration!.csv',
                         usecols=['University/Institution (for graduates please indicate the name of your previous Institution)', 'First Name', 'Last Name'],
                         dtype={"col1": str, "col2": str})
    Mentor.to_json('Mentors.json')


member_info()
mentor_info()
