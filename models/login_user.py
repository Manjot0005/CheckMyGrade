import hashlib
import base64

class LoginUser:
    """Class to manage user authentication"""
    
    def __init__(self, email_id, password, role='student'):
        if not email_id:
            raise ValueError("Email ID cannot be null or empty")
        
        self.email_id = email_id
        self.password = password  # Store encrypted password
        self.role = role  # 'student', 'professor', 'admin'
        self.is_logged_in = False
    
    @staticmethod
    def encrypt_password(plain_password):
        """Encrypt password using SHA256 and base64 encoding"""
        # Using SHA256 hash
        hash_obj = hashlib.sha256(plain_password.encode())
        # Convert to base64 for storage
        encrypted = base64.b64encode(hash_obj.digest()).decode()
        return encrypted
    
    @staticmethod
    def decrypt_password(encrypted_password):
        """
        Note: SHA256 is one-way hash, so we can't truly decrypt.
        Instead, we verify by comparing hashed versions.
        This method is kept for interface compatibility.
        """
        # Can't decrypt SHA256, so return the encrypted version
        # Verification is done by comparing hashed passwords
        return encrypted_password
    
    @staticmethod
    def verify_password(plain_password, encrypted_password):
        """Verify if plain password matches encrypted password"""
        return LoginUser.encrypt_password(plain_password) == encrypted_password
    
    def login(self, entered_password):
        """Attempt to login with provided password"""
        if self.verify_password(entered_password, self.password):
            self.is_logged_in = True
            print(f"Login successful! Welcome {self.email_id}")
            return True
        else:
            print("Login failed! Incorrect password.")
            return False
    
    def logout(self):
        """Logout the current user"""
        if self.is_logged_in:
            self.is_logged_in = False
            print(f"User {self.email_id} logged out successfully.")
            return True
        else:
            print("No user is currently logged in.")
            return False
    
    def change_password(self, old_password, new_password):
        """Change user password"""
        if self.verify_password(old_password, self.password):
            self.password = self.encrypt_password(new_password)
            print("Password changed successfully!")
            return True
        else:
            print("Failed to change password. Old password is incorrect.")
            return False
    
    def to_dict(self):
        """Convert login user object to dictionary for CSV"""
        return {
            'email_id': self.email_id,
            'password': self.password,  # Already encrypted
            'role': self.role
        }
    
    def __str__(self):
        return f"User: {self.email_id} (Role: {self.role})"
    
    def __repr__(self):
        return f"LoginUser('{self.email_id}', role='{self.role}')"