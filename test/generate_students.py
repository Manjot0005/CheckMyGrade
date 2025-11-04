"""
Script to generate 1000 sample students for testing purposes
"""
import random
from student import Student
from login_user import LoginUser
from csv_handler import CSVHandler

def generate_sample_students(num_students=1000):
    """Generate sample students with random data"""
    
    csv_handler = CSVHandler('data')
    students = []
    users = []
    
    # Sample first names
    first_names = [
        'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
        'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
        'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
        'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
        'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
        'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
        'Nicholas', 'Angela', 'Eric', 'Shirley', 'Jonathan', 'Anna', 'Stephen', 'Brenda',
        'Larry', 'Pamela', 'Justin', 'Emma', 'Scott', 'Nicole', 'Brandon', 'Helen'
    ]
    
    # Sample last names
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
        'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
        'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
        'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
        'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
        'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson'
    ]
    
    # Sample courses
    courses = ['DATA200', 'CS146', 'CS149', 'MATH161', 'PHYS50', 'ENGL1A']
    
    print(f"Generating {num_students} sample students...")
    
    for i in range(num_students):
        # Generate random student data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@mycsu.edu"
        
        # Create student
        student = Student(email, first_name, last_name)
        
        # Add random courses (1-4 courses per student)
        num_courses = random.randint(1, 4)
        selected_courses = random.sample(courses, num_courses)
        
        for course in selected_courses:
            marks = random.randint(60, 100)  # Marks between 60-100
            student.add_course(course, marks)
        
        students.append(student)
        
        # Create login user
        default_password = "password123"
        encrypted_pass = LoginUser.encrypt_password(default_password)
        user = LoginUser(email, encrypted_pass, 'student')
        users.append(user)
        
        # Print progress
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_students} students...")
    
    print(f"\nSaving {len(students)} students to CSV...")
    csv_handler.save_students(students)
    
    print(f"Saving {len(users)} user accounts to CSV...")
    csv_handler.save_users(users)
    
    print("\n✓ Successfully generated and saved all sample data!")
    print(f"  - {len(students)} students")
    print(f"  - {len(users)} user accounts")
    print(f"  - Default password for all users: password123")
    
    # Print some statistics
    total_enrollments = sum(len(s.courses) for s in students)
    avg_enrollments = total_enrollments / len(students)
    
    all_marks = []
    for s in students:
        all_marks.extend(s.marks)
    
    if all_marks:
        avg_marks = sum(all_marks) / len(all_marks)
        print(f"\nStatistics:")
        print(f"  - Average courses per student: {avg_enrollments:.2f}")
        print(f"  - Average marks: {avg_marks:.2f}")
        print(f"  - Total course enrollments: {total_enrollments}")

if __name__ == "__main__":
    generate_sample_students(1000)