class Professor:
    """Class to manage professor information"""
    
    def __init__(self, professor_id, name, email_address, rank, course_ids=None):
        if not professor_id:
            raise ValueError("Professor ID cannot be null or empty")
        if not email_address:
            raise ValueError("Email address cannot be null or empty")
        
        self.professor_id = professor_id
        self.name = name
        self.email_address = email_address
        self.rank = rank
        self.course_ids = course_ids if course_ids else []
    
    def professors_details(self):
        """Display professor details"""
        print(f"\nProfessor ID: {self.professor_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email_address}")
        print(f"Rank: {self.rank}")
        print(f"Courses Teaching: {', '.join(self.course_ids) if self.course_ids else 'None'}")
    
    def add_course(self, course_id):
        """Add a course to professor's teaching list"""
        if course_id not in self.course_ids:
            self.course_ids.append(course_id)
            return True
        return False
    
    def to_dict(self):
        """Convert professor object to dictionary for CSV"""
        return {
            'professor_id': self.professor_id,
            'name': self.name,
            'email_address': self.email_address,
            'rank': self.rank,
            'course_ids': ','.join(self.course_ids)
        }