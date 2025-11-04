class Course:
    """Class to manage course information"""
    
    def __init__(self, course_id, course_name, credits=3, description=""):
        if not course_id:
            raise ValueError("Course ID cannot be null or empty")
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description
        self.enrolled_students = []
    
    def display_courses(self):
        """Display course information"""
        print(f"\nCourse ID: {self.course_id}")
        print(f"Course Name: {self.course_name}")
        print(f"Credits: {self.credits}")
        print(f"Description: {self.description}")
    
    def to_dict(self):
        """Convert course object to dictionary for CSV"""
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'credits': self.credits,
            'description': self.description
        }