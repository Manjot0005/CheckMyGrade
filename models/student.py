from models.grades import Grades

class Student:
    """Class to manage student information"""
    
    def __init__(self, email_address, first_name, last_name, courses=None, grades=None, marks=None):
        if not email_address:
            raise ValueError("Email address cannot be null or empty")
        
        self.email_address = email_address  # Using as unique ID
        self.first_name = first_name
        self.last_name = last_name
        self.courses = courses if courses else []  # HAS-A relationship with courses
        self.grades = grades if grades else []
        self.marks = marks if marks else []
    
    def display_records(self):
        """Display student record"""
        print(f"\n{'='*50}")
        print(f"Student Email: {self.email_address}")
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Courses Enrolled: {len(self.courses)}")
        if self.courses:
            for i, course in enumerate(self.courses):
                grade = self.grades[i] if i < len(self.grades) else 'N/A'
                mark = self.marks[i] if i < len(self.marks) else 'N/A'
                print(f"  {course}: Grade {grade}, Marks {mark}")
        print(f"{'='*50}")
    
    def check_my_grades(self):
        """Display student grades"""
        print(f"\nGrades for {self.first_name} {self.last_name}:")
        if self.courses:
            for i, course in enumerate(self.courses):
                grade = self.grades[i] if i < len(self.grades) else 'N/A'
                print(f"  {course}: {grade}")
        else:
            print("  No courses enrolled")
    
    def check_my_marks(self):
        """Display student marks"""
        print(f"\nMarks for {self.first_name} {self.last_name}:")
        if self.courses:
            for i, course in enumerate(self.courses):
                mark = self.marks[i] if i < len(self.marks) else 'N/A'
                print(f"  {course}: {mark}")
        else:
            print("  No courses enrolled")
    
    def add_course(self, course_id, marks=0):
        """Add a course to student's record"""
        if course_id not in self.courses:
            self.courses.append(course_id)
            self.marks.append(marks)
            grade = Grades.calculate_grade(marks)
            self.grades.append(grade)
            return True
        return False
    
    def remove_course(self, course_id):
        """Remove a course from student's record"""
        if course_id in self.courses:
            idx = self.courses.index(course_id)
            self.courses.pop(idx)
            self.marks.pop(idx)
            self.grades.pop(idx)
            return True
        return False
    
    def update_marks(self, course_id, new_marks):
        """Update marks for a specific course"""
        if course_id in self.courses:
            idx = self.courses.index(course_id)
            self.marks[idx] = new_marks
            self.grades[idx] = Grades.calculate_grade(new_marks)
            return True
        return False
    
    def get_average_marks(self):
        """Calculate average marks across all courses"""
        if self.marks:
            return sum(self.marks) / len(self.marks)
        return 0
    
    def get_gpa(self):
        """Calculate GPA based on grades"""
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        if self.grades:
            total_points = sum(grade_points.get(g, 0) for g in self.grades)
            return total_points / len(self.grades)
        return 0.0
    
    def to_dict(self):
        """Convert student object to dictionary for CSV"""
        return {
            'email_address': self.email_address,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'courses': ','.join(self.courses),  # Store as comma-separated
            'grades': ','.join(self.grades),
            'marks': ','.join(map(str, self.marks))
        }
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_address})"
    
    def __repr__(self):
        return f"Student('{self.email_address}', '{self.first_name}', '{self.last_name}')"