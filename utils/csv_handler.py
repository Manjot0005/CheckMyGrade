import csv
import os
from models.student import Student
from models.course import Course
from models.professor import Professor
from models.login_user import LoginUser
from models.grades import Grades

class CSVHandler:
    """Utility class to handle CSV file operations"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, 'students.csv')
        self.courses_file = os.path.join(data_dir, 'courses.csv')
        self.professors_file = os.path.join(data_dir, 'professors.csv')
        self.login_file = os.path.join(data_dir, 'login.csv')
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    # ==================== STUDENT OPERATIONS ====================
    
    def load_students(self):
        """Load students from CSV file"""
        students = []
        if not os.path.exists(self.students_file):
            return students
        
        try:
            with open(self.students_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    courses = row['courses'].split(',') if row['courses'] else []
                    grades = row['grades'].split(',') if row['grades'] else []
                    marks = [int(m) for m in row['marks'].split(',') if m] if row['marks'] else []
                    
                    student = Student(
                        email_address=row['email_address'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        courses=courses,
                        grades=grades,
                        marks=marks
                    )
                    students.append(student)
        except Exception as e:
            print(f"Error loading students: {e}")
        
        return students
    
    def save_students(self, students):
        """Save students to CSV file"""
        try:
            with open(self.students_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['email_address', 'first_name', 'last_name', 'courses', 'grades', 'marks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for student in students:
                    writer.writerow(student.to_dict())
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False
    
    # ==================== COURSE OPERATIONS ====================
    
    def load_courses(self):
        """Load courses from CSV file"""
        courses = []
        if not os.path.exists(self.courses_file):
            return courses
        
        try:
            with open(self.courses_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course = Course(
                        course_id=row['course_id'],
                        course_name=row['course_name'],
                        credits=int(row.get('credits', 3)),
                        description=row.get('description', '')
                    )
                    courses.append(course)
        except Exception as e:
            print(f"Error loading courses: {e}")
        
        return courses
    
    def save_courses(self, courses):
        """Save courses to CSV file"""
        try:
            with open(self.courses_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['course_id', 'course_name', 'credits', 'description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in courses:
                    writer.writerow(course.to_dict())
            return True
        except Exception as e:
            print(f"Error saving courses: {e}")
            return False
    
    # ==================== PROFESSOR OPERATIONS ====================
    
    def load_professors(self):
        """Load professors from CSV file"""
        professors = []
        if not os.path.exists(self.professors_file):
            return professors
        
        try:
            with open(self.professors_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course_ids = row.get('course_ids', '').split(',') if row.get('course_ids') else []
                    course_ids = [c.strip() for c in course_ids if c.strip()]
                    
                    professor = Professor(
                        professor_id=row['professor_id'],
                        name=row['name'],
                        email_address=row['email_address'],
                        rank=row['rank'],
                        course_ids=course_ids
                    )
                    professors.append(professor)
        except Exception as e:
            print(f"Error loading professors: {e}")
        
        return professors
    
    def save_professors(self, professors):
        """Save professors to CSV file"""
        try:
            with open(self.professors_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['professor_id', 'name', 'email_address', 'rank', 'course_ids']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for professor in professors:
                    writer.writerow(professor.to_dict())
            return True
        except Exception as e:
            print(f"Error saving professors: {e}")
            return False
    
    # ==================== LOGIN OPERATIONS ====================
    
    def load_users(self):
        """Load users from CSV file"""
        users = []
        if not os.path.exists(self.login_file):
            return users
        
        try:
            with open(self.login_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = LoginUser(
                        email_id=row['email_id'],
                        password=row['password'],  # Already encrypted
                        role=row.get('role', 'student')
                    )
                    users.append(user)
        except Exception as e:
            print(f"Error loading users: {e}")
        
        return users
    
    def save_users(self, users):
        """Save users to CSV file"""
        try:
            with open(self.login_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['email_id', 'password', 'role']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for user in users:
                    writer.writerow(user.to_dict())
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False