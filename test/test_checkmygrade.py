import unittest
import time
import os
import shutil
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.student import Student
from models.course import Course
from models.professor import Professor
from models.login_user import LoginUser
from models.grades import Grades
from utils.csv_handler import CSVHandler

class TestCheckMyGrade(unittest.TestCase):
    """Comprehensive unit tests for CheckMyGrade application"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.test_data_dir = 'test_data'
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)
        os.makedirs(cls.test_data_dir)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)
    
    def setUp(self):
        """Set up for each test"""
        self.csv_handler = CSVHandler(self.test_data_dir)
        self.students = []
        self.courses = []
        self.professors = []
    
    # ==================== STUDENT TESTS ====================
    
    def test_student_creation(self):
        """Test creating a student"""
        student = Student('test@test.com', 'Test', 'User')
        self.assertEqual(student.email_address, 'test@test.com')
        self.assertEqual(student.first_name, 'Test')
        self.assertEqual(student.last_name, 'User')
    
    def test_student_add_course(self):
        """Test adding a course to student"""
        student = Student('test@test.com', 'Test', 'User')
        result = student.add_course('DATA200', 85)
        self.assertTrue(result)
        self.assertIn('DATA200', student.courses)
        self.assertEqual(student.marks[0], 85)
        self.assertEqual(student.grades[0], 'B')
    
    def test_student_remove_course(self):
        """Test removing a course from student"""
        student = Student('test@test.com', 'Test', 'User')
        student.add_course('DATA200', 85)
        result = student.remove_course('DATA200')
        self.assertTrue(result)
        self.assertNotIn('DATA200', student.courses)
    
    def test_student_update_marks(self):
        """Test updating student marks"""
        student = Student('test@test.com', 'Test', 'User')
        student.add_course('DATA200', 85)
        result = student.update_marks('DATA200', 95)
        self.assertTrue(result)
        self.assertEqual(student.marks[0], 95)
        self.assertEqual(student.grades[0], 'A')
    
    def test_student_average_marks(self):
        """Test calculating average marks"""
        student = Student('test@test.com', 'Test', 'User')
        student.add_course('DATA200', 90)
        student.add_course('CS146', 80)
        student.add_course('CS149', 70)
        avg = student.get_average_marks()
        self.assertEqual(avg, 80.0)
    
    def test_student_gpa(self):
        """Test calculating GPA"""
        student = Student('test@test.com', 'Test', 'User')
        student.add_course('DATA200', 90)  # A = 4.0
        student.add_course('CS146', 80)    # B = 3.0
        gpa = student.get_gpa()
        self.assertEqual(gpa, 3.5)
    
    def test_add_1000_students(self):
        """Test adding 1000 students"""
        print("\n\n=== Testing with 1000 Students ===")
        start_time = time.time()
        
        for i in range(1000):
            email = f"student{i}@test.com"
            student = Student(email, f"First{i}", f"Last{i}")
            student.add_course('DATA200', 70 + (i % 30))  # Marks between 70-99
            self.students.append(student)
        
        end_time = time.time()
        creation_time = (end_time - start_time) * 1000
        
        print(f"Created 1000 students in {creation_time:.2f} ms")
        self.assertEqual(len(self.students), 1000)
    
    def test_search_1000_students(self):
        """Test searching in 1000 students"""
        # First add 1000 students
        for i in range(1000):
            email = f"student{i}@test.com"
            student = Student(email, f"First{i}", f"Last{i}")
            self.students.append(student)
        
        # Test search
        print("\n=== Testing Search Performance ===")
        search_term = "student500"
        
        start_time = time.time()
        results = [s for s in self.students if search_term in s.email_address]
        end_time = time.time()
        
        search_time = (end_time - start_time) * 1000
        print(f"Searched 1000 students in {search_time:.4f} ms")
        print(f"Found {len(results)} result(s)")
        
        self.assertGreater(len(results), 0)
        self.assertLess(search_time, 10)  # Should be very fast
    
    def test_sort_1000_students_by_email(self):
        """Test sorting 1000 students by email"""
        # Add 1000 students
        for i in range(1000):
            email = f"student{i}@test.com"
            student = Student(email, f"First{i}", f"Last{i}")
            self.students.append(student)
        
        # Test ascending sort
        print("\n=== Testing Sort Performance (Ascending) ===")
        start_time = time.time()
        self.students.sort(key=lambda s: s.email_address)
        end_time = time.time()
        
        sort_time_asc = (end_time - start_time) * 1000
        print(f"Sorted 1000 students (ascending) in {sort_time_asc:.4f} ms")
        
        # Verify sort
        for i in range(len(self.students) - 1):
            self.assertLessEqual(self.students[i].email_address, 
                               self.students[i + 1].email_address)
        
        # Test descending sort
        print("\n=== Testing Sort Performance (Descending) ===")
        start_time = time.time()
        self.students.sort(key=lambda s: s.email_address, reverse=True)
        end_time = time.time()
        
        sort_time_desc = (end_time - start_time) * 1000
        print(f"Sorted 1000 students (descending) in {sort_time_desc:.4f} ms")
    
    def test_sort_1000_students_by_marks(self):
        """Test sorting 1000 students by average marks"""
        # Add 1000 students with marks
        for i in range(1000):
            email = f"student{i}@test.com"
            student = Student(email, f"First{i}", f"Last{i}")
            student.add_course('DATA200', 60 + (i % 40))
            self.students.append(student)
        
        print("\n=== Testing Sort by Marks Performance ===")
        start_time = time.time()
        self.students.sort(key=lambda s: s.get_average_marks(), reverse=True)
        end_time = time.time()
        
        sort_time = (end_time - start_time) * 1000
        print(f"Sorted 1000 students by marks in {sort_time:.4f} ms")
        
        # Verify sort
        for i in range(len(self.students) - 1):
            self.assertGreaterEqual(self.students[i].get_average_marks(),
                                   self.students[i + 1].get_average_marks())
    
    def test_save_and_load_1000_students(self):
        """Test saving and loading 1000 students from CSV"""
        # Add 1000 students
        for i in range(1000):
            email = f"student{i}@test.com"
            student = Student(email, f"First{i}", f"Last{i}")
            student.add_course('DATA200', 70 + (i % 30))
            self.students.append(student)
        
        # Test save
        print("\n=== Testing Save Performance ===")
        start_time = time.time()
        result = self.csv_handler.save_students(self.students)
        end_time = time.time()
        
        save_time = (end_time - start_time) * 1000
        print(f"Saved 1000 students in {save_time:.2f} ms")
        self.assertTrue(result)
        
        # Test load
        print("\n=== Testing Load Performance ===")
        start_time = time.time()
        loaded_students = self.csv_handler.load_students()
        end_time = time.time()
        
        load_time = (end_time - start_time) * 1000
        print(f"Loaded {len(loaded_students)} students in {load_time:.2f} ms")
        
        self.assertEqual(len(loaded_students), 1000)
    
    # ==================== COURSE TESTS ====================
    
    def test_course_creation(self):
        """Test creating a course"""
        course = Course('DATA200', 'Data Science', 3, 'Test description')
        self.assertEqual(course.course_id, 'DATA200')
        self.assertEqual(course.course_name, 'Data Science')
    
    def test_course_null_id(self):
        """Test that course requires non-null ID"""
        with self.assertRaises(ValueError):
            Course('', 'Test Course')
    
    def test_add_course(self):
        """Test adding courses"""
        for i in range(10):
            course = Course(f'COURSE{i}', f'Course {i}', 3)
            self.courses.append(course)
        
        self.assertEqual(len(self.courses), 10)
    
    def test_delete_course(self):
        """Test deleting a course"""
        course = Course('TEST100', 'Test Course', 3)
        self.courses.append(course)
        
        self.courses = [c for c in self.courses if c.course_id != 'TEST100']
        self.assertEqual(len(self.courses), 0)
    
    def test_modify_course(self):
        """Test modifying a course"""
        course = Course('TEST100', 'Test Course', 3)
        self.courses.append(course)
        
        # Modify
        course.course_name = 'Modified Course'
        course.credits = 4
        
        self.assertEqual(course.course_name, 'Modified Course')
        self.assertEqual(course.credits, 4)
    
    def test_save_and_load_courses(self):
        """Test saving and loading courses"""
        # Add courses
        for i in range(10):
            course = Course(f'COURSE{i}', f'Course {i}', 3, f'Description {i}')
            self.courses.append(course)
        
        # Save
        result = self.csv_handler.save_courses(self.courses)
        self.assertTrue(result)
        
        # Load
        loaded_courses = self.csv_handler.load_courses()
        self.assertEqual(len(loaded_courses), 10)
    
    # ==================== PROFESSOR TESTS ====================
    
    def test_professor_creation(self):
        """Test creating a professor"""
        prof = Professor('prof1@test.com', 'Test Prof', 'prof1@test.com', 'Assistant Professor')
        self.assertEqual(prof.professor_id, 'prof1@test.com')
        self.assertEqual(prof.name, 'Test Prof')
    
    def test_professor_null_id(self):
        """Test that professor requires non-null ID"""
        with self.assertRaises(ValueError):
            Professor('', 'Test', 'test@test.com', 'Professor')
    
    def test_add_professor(self):
        """Test adding professors"""
        for i in range(5):
            prof = Professor(f'prof{i}@test.com', f'Professor {i}', 
                           f'prof{i}@test.com', 'Assistant Professor')
            self.professors.append(prof)
        
        self.assertEqual(len(self.professors), 5)
    
    def test_delete_professor(self):
        """Test deleting a professor"""
        prof = Professor('prof@test.com', 'Test Prof', 'prof@test.com', 'Professor')
        self.professors.append(prof)
        
        self.professors = [p for p in self.professors if p.professor_id != 'prof@test.com']
        self.assertEqual(len(self.professors), 0)
    
    def test_modify_professor(self):
        """Test modifying professor details"""
        prof = Professor('prof@test.com', 'Test Prof', 'prof@test.com', 'Assistant Professor')
        prof.rank = 'Associate Professor'
        prof.add_course('DATA200')
        
        self.assertEqual(prof.rank, 'Associate Professor')
        self.assertIn('DATA200', prof.course_ids)
    
    def test_save_and_load_professors(self):
        """Test saving and loading professors"""
        # Add professors
        for i in range(5):
            prof = Professor(f'prof{i}@test.com', f'Professor {i}', 
                           f'prof{i}@test.com', 'Assistant Professor', ['DATA200'])
            self.professors.append(prof)
        
        # Save
        result = self.csv_handler.save_professors(self.professors)
        self.assertTrue(result)
        
        # Load
        loaded_profs = self.csv_handler.load_professors()
        self.assertEqual(len(loaded_profs), 5)
    
    # ==================== AUTHENTICATION TESTS ====================
    
    def test_password_encryption(self):
        """Test password encryption"""
        password = "TestPassword123!"
        encrypted = LoginUser.encrypt_password(password)
        
        self.assertNotEqual(password, encrypted)
        self.assertTrue(len(encrypted) > 0)
    
    def test_password_verification(self):
        """Test password verification"""
        password = "TestPassword123!"
        encrypted = LoginUser.encrypt_password(password)
        
        self.assertTrue(LoginUser.verify_password(password, encrypted))
        self.assertFalse(LoginUser.verify_password("WrongPassword", encrypted))
    
    def test_login(self):
        """Test user login"""
        password = "TestPassword123!"
        encrypted = LoginUser.encrypt_password(password)
        user = LoginUser('test@test.com', encrypted, 'student')
        
        result = user.login(password)
        self.assertTrue(result)
        self.assertTrue(user.is_logged_in)
    
    def test_logout(self):
        """Test user logout"""
        user = LoginUser('test@test.com', 'encrypted_pass', 'student')
        user.is_logged_in = True
        
        result = user.logout()
        self.assertTrue(result)
        self.assertFalse(user.is_logged_in)
    
    def test_change_password(self):
        """Test changing password"""
        old_password = "OldPassword123!"
        new_password = "NewPassword123!"
        
        encrypted_old = LoginUser.encrypt_password(old_password)
        user = LoginUser('test@test.com', encrypted_old, 'student')
        
        result = user.change_password(old_password, new_password)
        self.assertTrue(result)
        
        # Verify new password works
        self.assertTrue(LoginUser.verify_password(new_password, user.password))
    
    # ==================== GRADES TESTS ====================
    
    def test_calculate_grade(self):
        """Test grade calculation"""
        self.assertEqual(Grades.calculate_grade(95), 'A')
        self.assertEqual(Grades.calculate_grade(85), 'B')
        self.assertEqual(Grades.calculate_grade(75), 'C')
        self.assertEqual(Grades.calculate_grade(65), 'D')
        self.assertEqual(Grades.calculate_grade(55), 'F')

def run_tests():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCheckMyGrade)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result

if __name__ == '__main__':
    run_tests()