import sys
import json

def get_courses():
    # Simulate fetching data
    data = {
        "courses1": [
           {"id": "1", "category": "Core CS", "courses": [{"id": "1", "courseCode": "CSe00", "courseName": "Programming III"}]},
            {"id": "2", "category": "Basic Calculus", "courses": [{"id": "2", "courseCode": "CS400", "courseName": "Data Structures"}]} 
        ],
        "courses2": [
            {"id": "3", "category": "Core DS", "courses": [{"id": "3", "courseCode": "STAT 240", "courseName": "Data Science Modelling I"}]},
            {"id": "4", "category": "Probability/Statistics", "courses": [{"id": "4", "courseCode": "STAT 309", "courseName": "Intro to Probability"}]}
       ]
    }
    print(json.dumps(data))

if __name__ == "__main__":
    get_courses()