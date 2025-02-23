import json

def pop_and_output_top_two_courses(file_path):
    """
    Pops the top two courses (or the lone course if only one remains)
    from the 'cross_listed_courses' array in a JSON file and outputs them.
    """
    try:
        with open(file_path, "r+") as f:
            data = json.load(f)

            courses = data.get("cross_listed_courses", [])

            if not isinstance(courses, list):
                print("Error: 'cross_listed_courses' is not a list.")
                return

            if not courses:  # Check if the list is empty
                print([])
                return

            if len(courses) == 1:
                lone_course = [courses.pop(0)]  # Pop the lone course
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
                print(json.dumps(lone_course, indent=4))
                return

            top_two_courses = [courses.pop(0), courses.pop(0)]

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

            print(json.dumps(top_two_courses, indent=4))

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


pop_and_output_top_two_courses("output.json")