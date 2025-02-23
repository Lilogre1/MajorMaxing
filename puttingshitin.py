import argparse
import subprocess
import time

def main(major_one, major_two):
    #call scrape_courses.py with arguments
    subprocess.run(["python", "scrape_courses.py", major_one, major_two])

    #wait for 5 seconds
    time.sleep(5)

    #call jsonprint.py
    subprocess.run(["python", "jsonprint.py"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run scrape_courses.py and jsonprint.py with a delay')
    parser.add_argument('major_one', type=str, help='First major')
    parser.add_argument('major_two', type=str, help='Second major')

    args = parser.parse_args()
    main(args.major_one, args.major_two)
