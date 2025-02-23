import sys
import json

def get_courses():
    # Simulate fetching data
    data = {
        "courses1": [
            {"id": "1", "category": "Category 1", "courses": [{"id": "1", "courseCode": "CS101", "courseName": "Intro to Computer Science"}]},
            {"id": "2", "category": "Category 2", "courses": [{"id": "2", "courseCode": "CS102", "courseName": "Data Structures"}]}
        ],
        "courses2": [
            {"id": "3", "category": "Category 3", "courses": [{"id": "3", "courseCode": "CS201", "courseName": "Algorithms"}]},
            {"id": "4", "category": "Category 4", "courses": [{"id": "4", "courseCode": "CS202", "courseName": "Operating Systems"}]}
        ]
    }
    print(json.dumps(data))

if __name__ == "__main__":
    get_courses()