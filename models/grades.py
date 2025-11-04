class Grades:
    """Class to manage grade mappings and grade reports"""
    
    def __init__(self, grade_id=None, grade=None, min_marks=None, max_marks=None):
        self.grade_id = grade_id
        self.grade = grade
        self.min_marks = min_marks
        self.max_marks = max_marks
    
    @staticmethod
    def calculate_grade(marks):
        """Calculate letter grade based on marks"""
        if marks >= 90:
            return 'A'
        elif marks >= 80:
            return 'B'
        elif marks >= 70:
            return 'C'
        elif marks >= 60:
            return 'D'
        else:
            return 'F'
    
    def display_grade_report(self):
        """Display grade information"""
        print(f"Grade ID: {self.grade_id}")
        print(f"Grade: {self.grade}")
        print(f"Marks Range: {self.min_marks} - {self.max_marks}")