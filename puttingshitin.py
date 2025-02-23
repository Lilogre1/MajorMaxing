import argparse
import subprocess
import json

def main(major_one, major_two):
    # Call scrape_courses.py with arguments
    subprocess.run(["python", "./scrape_courses.py", major_one, major_two])

    # Call jsonprint.py and capture its output
    subprocess.run(["python", "./jsonprint.py"])

    # Print the response data
    print(json.dumps({"response": "Majors have been processed"}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run scrape_courses.py and jsonprint.py with a delay')
    parser.add_argument('major_one', type=str, help='First major')
    parser.add_argument('major_two', type=str, help='Second major')

    args = parser.parse_args()
    main(args.major_one, args.major_two)
