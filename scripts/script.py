import sys
import json

def main():
    # Simulate fetching data
    data = {
        "courses": [
            {"id": "1", "courseCode": "CS 300", "courseName": "Introduction to Computer Science"},
            {"id": "2", "courseCode": "NUT 9000", "courseName": "Graduate studies in Nutritional Science"}
        ]
    }
    print(json.dumps(data))

if __name__ == "__main__":
    main()