import time
import statistics
from models.student import Student
from models.course import Course
from models.professor import Professor
from models.login_user import LoginUser
from models.grades import Grades
from utils.csv_handler import CSVHandler

class CheckMyGradeApp:
    """Main application class for CheckMyGrade system"""
    
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.students = []
        self.courses = []
        self.professors = []
        self.users = []
        self.current_user = None
        
        # Load data from CSV files
        self.load_all_data()
    
    def load_all_data(self):
        """Load all data from CSV files"""
        print("Loading data from CSV files...")
        self.students = self.csv_handler.load_students()
        self.courses = self.csv_handler.load_courses()
        self.professors = self.csv_handler.load_professors()
        self.users = self.csv_handler.load_users()
        print(f"Loaded: {len(self.students)} students, {len(self.courses)} courses, "
              f"{len(self.professors)} professors, {len(self.users)} users")
    
    def save_all_data(self):
        """Save all data to CSV files"""
        print("Saving data to CSV files...")
        self.csv_handler.save_students(self.students)
        self.csv_handler.save_courses(self.courses)
        self.csv_handler.save_professors(self.professors)
        self.csv_handler.save_users(self.users)
        print("Data saved successfully!")
    
    # ==================== STUDENT OPERATIONS ====================
    
    def add_new_student(self):
        """Add a new student"""
        print("\n=== Add New Student ===")
        email = input("Enter student email: ").strip()
        
        # Check if student already exists
        if any(s.email_address == email for s in self.students):
            print("Error: Student with this email already exists!")
            return
        
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        
        student = Student(email, first_name, last_name)
        self.students.append(student)
        
        # Also create login user
        password = input("Enter password for this student: ").strip()
        encrypted_pass = LoginUser.encrypt_password(password)
        user = LoginUser(email, encrypted_pass, 'student')
        self.users.append(user)
        
        self.save_all_data()
        print(f"Student {first_name} {last_name} added successfully!")
    
    def delete_student(self):
        """Delete a student"""
        print("\n=== Delete Student ===")
        email = input("Enter student email to delete: ").strip()
        
        # Find and remove student
        original_count = len(self.students)
        self.students = [s for s in self.students if s.email_address != email]
        
        if len(self.students) < original_count:
            # Also remove from users
            self.users = [u for u in self.users if u.email_id != email]
            self.save_all_data()
            print(f"Student {email} deleted successfully!")
        else:
            print(f"Student {email} not found!")
    
    def update_student_record(self):
        """Update student record"""
        print("\n=== Update Student Record ===")
        email = input("Enter student email: ").strip()
        
        student = self.find_student(email)
        if not student:
            print(f"Student {email} not found!")
            return
        
        print("\nWhat would you like to update?")
        print("1. Add course")
        print("2. Remove course")
        print("3. Update marks")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            course_id = input("Enter course ID: ").strip()
            if self.find_course(course_id):
                marks = int(input("Enter marks: "))
                student.add_course(course_id, marks)
                self.save_all_data()
                print("Course added successfully!")
            else:
                print("Course not found!")
        
        elif choice == '2':
            course_id = input("Enter course ID to remove: ").strip()
            if student.remove_course(course_id):
                self.save_all_data()
                print("Course removed successfully!")
            else:
                print("Course not found in student's record!")
        
        elif choice == '3':
            course_id = input("Enter course ID: ").strip()
            marks = int(input("Enter new marks: "))
            if student.update_marks(course_id, marks):
                self.save_all_data()
                print("Marks updated successfully!")
            else:
                print("Course not found in student's record!")
    
    def search_student(self):
        """Search for students"""
        print("\n=== Search Students ===")
        search_term = input("Enter email or name to search: ").strip().lower()
        
        start_time = time.time()
        
        results = []
        for student in self.students:
            if (search_term in student.email_address.lower() or
                search_term in student.first_name.lower() or
                search_term in student.last_name.lower()):
                results.append(student)
        
        end_time = time.time()
        search_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"\nFound {len(results)} student(s) in {search_time:.4f} ms:")
        for student in results:
            student.display_records()
        
        return search_time
    
    def sort_students(self):
        """Sort students by name or marks"""
        print("\n=== Sort Students ===")
        print("1. Sort by email")
        print("2. Sort by first name")
        print("3. Sort by average marks")
        choice = input("Enter choice: ").strip()
        
        order = input("Ascending (a) or Descending (d)? ").strip().lower()
        reverse = (order == 'd')
        
        start_time = time.time()
        
        if choice == '1':
            self.students.sort(key=lambda s: s.email_address, reverse=reverse)
        elif choice == '2':
            self.students.sort(key=lambda s: s.first_name, reverse=reverse)
        elif choice == '3':
            self.students.sort(key=lambda s: s.get_average_marks(), reverse=reverse)
        else:
            print("Invalid choice!")
            return
        
        end_time = time.time()
        sort_time = (end_time - start_time) * 1000
        
        print(f"\nStudents sorted in {sort_time:.4f} ms")
        print("\nFirst 10 students:")
        for student in self.students[:10]:
            print(f"{student.email_address}: {student.first_name} {student.last_name} "
                  f"(Avg: {student.get_average_marks():.2f})")
        
        return sort_time
    
    def display_student_statistics(self):
        """Display statistics for all students"""
        print("\n=== Student Statistics ===")
        
        if not self.students:
            print("No students in the system!")
            return
        
        # Calculate statistics
        all_marks = []
        for student in self.students:
            all_marks.extend(student.marks)
        
        if all_marks:
            avg_marks = statistics.mean(all_marks)
            median_marks = statistics.median(all_marks)
            
            print(f"Total Students: {len(self.students)}")
            print(f"Average Marks (All Courses): {avg_marks:.2f}")
            print(f"Median Marks (All Courses): {median_marks:.2f}")
            print(f"Highest Marks: {max(all_marks)}")
            print(f"Lowest Marks: {min(all_marks)}")
        else:
            print("No marks data available!")
    
    # ==================== COURSE OPERATIONS ====================
    
    def add_new_course(self):
        """Add a new course"""
        print("\n=== Add New Course ===")
        course_id = input("Enter course ID: ").strip()
        
        if self.find_course(course_id):
            print("Error: Course with this ID already exists!")
            return
        
        course_name = input("Enter course name: ").strip()
        credits = int(input("Enter credits (default 3): ") or "3")
        description = input("Enter description: ").strip()
        
        course = Course(course_id, course_name, credits, description)
        self.courses.append(course)
        self.save_all_data()
        print(f"Course {course_name} added successfully!")
    
    def delete_course(self):
        """Delete a course"""
        print("\n=== Delete Course ===")
        course_id = input("Enter course ID to delete: ").strip()
        
        original_count = len(self.courses)
        self.courses = [c for c in self.courses if c.course_id != course_id]
        
        if len(self.courses) < original_count:
            self.save_all_data()
            print(f"Course {course_id} deleted successfully!")
        else:
            print(f"Course {course_id} not found!")
    
    def display_courses(self):
        """Display all courses"""
        print("\n=== All Courses ===")
        if not self.courses:
            print("No courses in the system!")
            return
        
        for course in self.courses:
            course.display_courses()
    
    # ==================== PROFESSOR OPERATIONS ====================
    
    def add_new_professor(self):
        """Add a new professor"""
        print("\n=== Add New Professor ===")
        prof_id = input("Enter professor ID (email): ").strip()
        
        if any(p.professor_id == prof_id for p in self.professors):
            print("Error: Professor with this ID already exists!")
            return
        
        name = input("Enter professor name: ").strip()
        email = input("Enter email address: ").strip()
        rank = input("Enter rank: ").strip()
        
        professor = Professor(prof_id, name, email, rank)
        self.professors.append(professor)
        
        # Also create login user
        password = input("Enter password for this professor: ").strip()
        encrypted_pass = LoginUser.encrypt_password(password)
        user = LoginUser(email, encrypted_pass, 'professor')
        self.users.append(user)
        
        self.save_all_data()
        print(f"Professor {name} added successfully!")
    
    def delete_professor(self):
        """Delete a professor"""
        print("\n=== Delete Professor ===")
        prof_id = input("Enter professor ID to delete: ").strip()
        
        original_count = len(self.professors)
        self.professors = [p for p in self.professors if p.professor_id != prof_id]
        
        if len(self.professors) < original_count:
            self.save_all_data()
            print(f"Professor {prof_id} deleted successfully!")
        else:
            print(f"Professor {prof_id} not found!")
    
    def display_professors(self):
        """Display all professors"""
        print("\n=== All Professors ===")
        if not self.professors:
            print("No professors in the system!")
            return
        
        for professor in self.professors:
            professor.professors_details()
    
    # ==================== REPORTS ====================
    
    def generate_reports(self):
        """Generate various reports"""
        print("\n=== Generate Reports ===")
        print("1. Course-wise report")
        print("2. Professor-wise report")
        print("3. Student-wise report")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.course_wise_report()
        elif choice == '2':
            self.professor_wise_report()
        elif choice == '3':
            self.student_wise_report()
    
    def course_wise_report(self):
        """Generate course-wise report"""
        print("\n=== Course-wise Report ===")
        course_id = input("Enter course ID: ").strip()
        
        course = self.find_course(course_id)
        if not course:
            print("Course not found!")
            return
        
        course.display_courses()
        
        # Find students enrolled in this course
        enrolled_students = [s for s in self.students if course_id in s.courses]
        print(f"\nStudents enrolled: {len(enrolled_students)}")
        
        for student in enrolled_students:
            idx = student.courses.index(course_id)
            marks = student.marks[idx] if idx < len(student.marks) else 'N/A'
            grade = student.grades[idx] if idx < len(student.grades) else 'N/A'
            print(f"  {student.first_name} {student.last_name}: Marks {marks}, Grade {grade}")
        
        # Calculate course statistics
        course_marks = [s.marks[s.courses.index(course_id)] 
                       for s in enrolled_students 
                       if course_id in s.courses and s.marks]
        
        if course_marks:
            print(f"\nCourse Statistics:")
            print(f"  Average Marks: {statistics.mean(course_marks):.2f}")
            print(f"  Median Marks: {statistics.median(course_marks):.2f}")
    
    def professor_wise_report(self):
        """Generate professor-wise report"""
        print("\n=== Professor-wise Report ===")
        prof_id = input("Enter professor ID: ").strip()
        
        professor = self.find_professor(prof_id)
        if not professor:
            print("Professor not found!")
            return
        
        professor.professors_details()
        professor.show_course_details_by_professor(self.courses)
    
    def student_wise_report(self):
        """Generate student-wise report"""
        print("\n=== Student-wise Report ===")
        email = input("Enter student email: ").strip()
        
        student = self.find_student(email)
        if not student:
            print("Student not found!")
            return
        
        student.display_records()
        print(f"\nAverage Marks: {student.get_average_marks():.2f}")
        print(f"GPA: {student.get_gpa():.2f}")
    
    # ==================== HELPER METHODS ====================
    
    def find_student(self, email):
        """Find student by email"""
        for student in self.students:
            if student.email_address == email:
                return student
        return None
    
    def find_course(self, course_id):
        """Find course by ID"""
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
    
    def find_professor(self, prof_id):
        """Find professor by ID"""
        for professor in self.professors:
            if professor.professor_id == prof_id:
                return professor
        return None
    
    # ==================== MAIN MENU ====================
    
    def main_menu(self):
        """Display and handle main menu"""
        while True:
            print("\n" + "="*50)
            print("CheckMyGrade Application")
            print("="*50)
            print("1. Student Management")
            print("2. Course Management")
            print("3. Professor Management")
            print("4. Search & Sort")
            print("5. Reports & Statistics")
            print("6. Save & Exit")
            print("="*50)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                self.course_menu()
            elif choice == '3':
                self.professor_menu()
            elif choice == '4':
                self.search_sort_menu()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                self.save_all_data()
                print("Thank you for using CheckMyGrade!")
                break
            else:
                print("Invalid choice! Please try again.")
    
    def student_menu(self):
        """Student management menu"""
        print("\n=== Student Management ===")
        print("1. Add new student")
        print("2. Delete student")
        print("3. Update student record")
        print("4. Display all students")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.add_new_student()
        elif choice == '2':
            self.delete_student()
        elif choice == '3':
            self.update_student_record()
        elif choice == '4':
            for student in self.students[:10]:  # Display first 10
                student.display_records()
    
    def course_menu(self):
        """Course management menu"""
        print("\n=== Course Management ===")
        print("1. Add new course")
        print("2. Delete course")
        print("3. Display all courses")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.add_new_course()
        elif choice == '2':
            self.delete_course()
        elif choice == '3':
            self.display_courses()
    
    def professor_menu(self):
        """Professor management menu"""
        print("\n=== Professor Management ===")
        print("1. Add new professor")
        print("2. Delete professor")
        print("3. Display all professors")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.add_new_professor()
        elif choice == '2':
            self.delete_professor()
        elif choice == '3':
            self.display_professors()
    
    def search_sort_menu(self):
        """Search and sort menu"""
        print("\n=== Search & Sort ===")
        print("1. Search students")
        print("2. Sort students")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.search_student()
        elif choice == '2':
            self.sort_students()
    
    def reports_menu(self):
        """Reports and statistics menu"""
        print("\n=== Reports & Statistics ===")
        print("1. Generate reports")
        print("2. Display student statistics")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self.generate_reports()
        elif choice == '2':
            self.display_student_statistics()

def main():
    """Main entry point"""
    app = CheckMyGradeApp()
    app.main_menu()

if __name__ == "__main__":
    main()