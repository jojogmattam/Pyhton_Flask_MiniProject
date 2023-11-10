#!/usr/bin/env python3
import requests
from pprint import pprint
import os

def main():
    quiz_api_url="http://localhost:5000/api/quiz"
    response = requests.get(quiz_api_url)
    if response.status_code != 200:
        print("Error: {}".format(response.status_code))
        return
    else:
        print("Success: {}".format(response.status_code))
        print("Quiz data:")
        pprint(response.json())

if __name__=="__main__":
    main()
