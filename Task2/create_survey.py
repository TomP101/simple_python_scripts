#!/usr/bin/env python3.13

import json
import requests
import argparse
import http.client

def create_survey(api_token, questions_file,email_file):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")

    with open(questions_file, "r") as f:
            questions_data = json.load(f)

    survey_name = list(questions_data.keys())[0]
    pages = []

    for page_name, questions in questions_data[survey_name].items():
            page_questions = []
            for question_name, question_data in questions.items():
                page_questions.append( { 
                    "headings" : [{"heading": question_name}],
                    "family": "single_choice",
                    "subtype": "vertical",
                    "answers": {"choices": [{"text": answer} for answer in question_data["Answers"]]}
                })
                pages.append({
                    "title": page_name, 
                    "questions": page_questions
                    })


    payload = {
            "title": survey_name,
            "pages": pages
        }

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {api_token}"
        }

    conn.request("POST", "/v3/surveys", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    dane = json.loads(data)

    print(dane)

    print(dane["id"])
    #####################################
    #utworzenie collectora
    conn = http.client.HTTPSConnection("api.surveymonkey.com")

    payload = "{\"type\":\"weblink\"}"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {api_token}"
        }

    conn.request("POST", f"/v3/surveys/{dane["id"]}/collectors", payload, headers)

    res = conn.getresponse()
    data = res.read()

    dane = json.loads(data)

    print(dane)

    print(dane['id'])
    collector_id = dane['id']
    ##################################
    #utworzenie messages

    conn = http.client.HTTPSConnection("api.surveymonkey.com")

    payload = "{\"type\":\"thank_you\"}"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {api_token}"
        }

    conn.request("POST", f"/v3/collectors/{collector_id}/messages", payload, headers)

    res = conn.getresponse()
    data = res.read()

    dane = json.loads(data)

    print(dane)

    message_id = dane['id']

    ##################################
    # dodanie odbiorcow(recipments)
    with open(email_file) as f:
        emails = [line.strip() for line in f.readlines() if line.strip()]

    for email in emails:
        recipient_payload = {
            "email": email
        }
        conn.request("POST", f"/v3/collectors/{collector_id}/messages/{message_id}/recipients",
                     json.dumps(recipient_payload), headers)
        res = conn.getresponse()
        data = res.read()
        dane = json.loads(data)
        print(dane)

    print(dane)

    

    
        




parser = argparse.ArgumentParser(description="Create a survey")
parser.add_argument("-t", "--token", required=True, help="SurveyMonkey API access token")
parser.add_argument("-q","--questions", required=True, help="path to JSON file")
parser.add_argument("-e", "--emails", required=True, help="path to file with emails")

args = parser.parse_args()

api_token = args.token
questions_file = args.questions
email_file = args.emails

create_survey(api_token,questions_file,email_file)


with open(email_file) as f:
      emails = [line.strip() for line in f.readlines() if line.strip()]

print(emails)
