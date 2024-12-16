from main import MongoDBHandler

# Initialize the MongoDB handler
db_handler = MongoDBHandler()

# Initialize collections
collections = ["departments", "professors", "courses", "students"]

# 1. Insert data into the 'departments' collection
departments = [
    {"_id": "department_id_1", "name": "Computer Science", "head": "Dr. Smith"},
    {"_id": "department_id_2", "name": "Mathematics", "head": "Dr. Taylor"},
]

for department in departments:
    db_handler.create("departments", department)
print("Departments initialized!")

# 2. Insert data into the 'professors' collection
professors = [
    {"_id": "professor_id_1", "name": "Dr. John Doe", "email": "johndoe@example.com", "department_id": "department_id_1"},
    {"_id": "professor_id_2", "name": "Dr. Jane Roe", "email": "janeroe@example.com", "department_id": "department_id_2"},
]

for professor in professors:
    db_handler.create("professors", professor)
print("Professors initialized!")

# 3. Insert data into the 'courses' collection
courses = [
    {"_id": "course_id_1", "title": "Introduction to Programming", "department_id": "department_id_1", "professor_id": "professor_id_1"},
    {"_id": "course_id_2", "title": "Advanced Mathematics", "department_id": "department_id_2", "professor_id": "professor_id_2"},
]

for course in courses:
    db_handler.create("courses", course)
print("Courses initialized!")

# 4. Insert data into the 'students' collection
students = [
    {"_id": "student_id_1", "name": "Alice Johnson", "email": "alice@example.com", "enrolled_date": "2024-12-16", "enrolled_courses": ["course_id_1"]},
    {"_id": "student_id_2", "name": "Bob Smith", "email": "bob@example.com", "enrolled_date": "2024-12-16", "enrolled_courses": ["course_id_1", "course_id_2"]},
]

for student in students:
    db_handler.create("students", student)
print("Students initialized!")

# Example Queries
print("\n--- Example Queries ---")

# 1. Retrieve all courses offered by a specific department
department_id = "department_id_1"
courses = db_handler.read("courses", {"department_id": department_id})
print(f"Courses offered by department {department_id}:")
for course in courses:
    print(course)

# 2. Find all students enrolled in a specific course
course_id = "course_id_1"
students = db_handler.read("students", {"enrolled_courses": course_id})
print(f"\nStudents enrolled in course {course_id}:")
for student in students:
    print(student)

# 3. Find all professors in a specific department
professors = db_handler.read("professors", {"department_id": "department_id_1"})
print(f"\nProfessors in department {department_id}:")
for professor in professors:
    print(professor)
