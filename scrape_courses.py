import argparse
import requests
from bs4 import BeautifulSoup
import re
import sqlite3

def determine_urls(major_one, major_two):
    url_dict = {
        'Computer Science': 'https://guide.wisc.edu/undergraduate/letters-science/computer-sciences/computer-sciences-bs/',
        'Data Science': 'https://guide.wisc.edu/undergraduate/letters-science/statistics/data-science-bs/',
        'Statistics': 'https://guide.wisc.edu/undergraduate/letters-science/statistics/statistics-bs/',
        'Information Science': 'https://guide.wisc.edu/undergraduate/letters-science/information/information-science-bs/index.html',
        'Math': 'https://guide.wisc.edu/undergraduate/letters-science/mathematics/mathematics-bs/'
    }
    url1 = url_dict.get(major_one, 'https://guide.wisc.edu/undergraduate/letters-science/computer-sciences/computer-sciences-bs/')
    url2 = url_dict.get(major_two, 'https://guide.wisc.edu/undergraduate/letters-science/statistics/data-science-bs/')
    return url1, url2

# Function to clear out "or declared" to make it easier/less cluttered
def remove_after_declared(prereq_text):
    match = re.search(r', or declared', prereq_text, re.IGNORECASE)
    if match:
        prereq_text = prereq_text[:match.start()].strip()
        
    match = re.search(r'or declared', prereq_text, re.IGNORECASE)
    if match:
        prereq_text = prereq_text[:match.start()].strip()    
    return prereq_text

# Function to clean basic text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s,./\-()\[\]&]', '', text)
    return text

# Function to fix course codes
def format_course_codes(text):
    def replace_code_pairs(match):
        code1, code2 = match.groups()
        full_code = f'{code1.split()[0]} {code2}'
        return f'{code1} and {full_code}'
    
    text = re.sub(r'(\b[A-Z]{2,}\s\d{3})\s?and\s(\d{3}\b)', replace_code_pairs, text)
    text = re.sub(r'(\b[A-Z]{2,}\s\d{3})\s?or\s(\d{3}\b)', replace_code_pairs, text)
    return text

# Function to scrape courses from the major pages
def scrape_courses(url):
    course_list = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find('div', id='requirementstextcontainer')
        if container:
            courses = container.find_all('a', class_='bubblelink code')
            for course in courses:
                course_name = format_course_codes(clean_text(course.text.strip().replace(u'\xa0', ' ').replace('\u200b', '')))
                course_list.append(course_name)
        else:
            print(f"No course container found in {url}")
    else:
        print(f"Failed to retrieve data from {url}")
    return course_list

# Function to scrape the department course lists
def scrape_courses_and_prerequisites(url):
    courses_data = {}
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('span', class_='courseblockcode')
        for course in courses:
            course_name = clean_text(course.text.strip().replace(u'\xa0', ' '))
            prereq = 'None mentioned'
            exclusive = 'None'
            credits = 'Unknown'  # Default values
            description = 'No description available'  # Default value
            container = course.find_next('div', class_='cb-extras')
            if container:
                prereq_label = container.find('span', class_='cbextra-label')
                prereq_data = container.find('span', class_='cbextra-data')
                credits_data = container.find_previous('p', class_='courseblockcredits')
                description_data = container.find_previous('p', class_='courseblocktitle noindent')
                if prereq_label and prereq_data:
                    prereq_text = prereq_data.text.strip().replace(u'\xa0', ' ')
                    
                    weirdcharacters = "​"
                    prereq_text = prereq_text.replace(weirdcharacters, '').strip()
                    
                    cs400 = "(COMP SCI 367 or 400)"
                    prereq_text = prereq_text.replace(cs400, 'COMP SCI 400').strip()
                    
                    prereq_text = remove_after_declared(prereq_text)
                    
                    grandstanding = ', g'
                    prereq_text = prereq_text.replace(grandstanding, ', or g').strip()
                    
                    # Format course codes
                    prereq_text = format_course_codes(prereq_text)
                    
                    # Parts of prerequisites
                    prereq_parts = prereq_text.split('. ')
                    prereq_list = [p.strip() for p in prereq_parts if 'Not open to students' not in p and p]
                    exclusive_list = [p.replace('Not open to students with credit for ', '').strip() for p in prereq_parts if 'Not open to students' in p]
                    prereq = ', '.join(prereq_list) if prereq_list else 'None mentioned'
                    exclusive = ', '.join(exclusive_list) if exclusive_list else 'None'

                    exclusive = exclusive.rstrip('.')
            
                if credits_data:
                    credits = clean_text(credits_data.text.strip().replace(u'\xa0', ' '))
                if description_data:
                    description_text = description_data.text.strip()
                    description = description_text.split('—', 1)[1].strip() if '—' in description_text else 'No description available'
            courses_data[course_name] = {
                'Prerequisites': prereq,
                'Exclusive': exclusive,
                'Credits': credits,
                'Description': description
            }
            
    else:
        print(f"Failed to retrieve data from {url}")
    return courses_data

def store_courses_in_db(courses, detailed_courses):
    conn = sqlite3.connect('university_courses.db')
    cursor = conn.cursor()

    # Clear the existing table or create it if it doesn't exist
    cursor.execute('DROP TABLE IF EXISTS cross_listed_courses')
    cursor.execute('''
    CREATE TABLE cross_listed_courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        prerequisites TEXT,
        exclusive TEXT,
        credits TEXT,
        description TEXT
    )
    ''')

    for course in courses:
        details = detailed_courses.get(course, {'Prerequisites': 'None', 'Exclusive': 'None', 'Credits': 'Unknown', 'Description': 'No description available'})
        cursor.execute('''
        INSERT INTO cross_listed_courses (course_name, prerequisites, exclusive, credits, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (course, details['Prerequisites'], details['Exclusive'], details['Credits'], details['Description']))

    conn.commit()
    conn.close()

# All course info
detailed_course_urls = [
    'https://guide.wisc.edu/courses/comp_sci/',
    'https://guide.wisc.edu/courses/stat/',
    'https://guide.wisc.edu/courses/math/',
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape course data for two majors')
    parser.add_argument('major_one', type=str, help='First major')
    parser.add_argument('major_two', type=str, help='Second major')

    args = parser.parse_args()
    major_one = args.major_one
    major_two = args.major_two

    url1, url2 = determine_urls(major_one, major_two)

    # Proceed with the scraping and processing
    course_lists = [set(scrape_courses(url)) for url in [url1, url2]]
    common_courses = set.intersection(*course_lists)

    detailed_courses = {}
    for url in detailed_course_urls:
        detailed_courses.update(scrape_courses_and_prerequisites(url))

    store_courses_in_db(common_courses, detailed_courses)

    
