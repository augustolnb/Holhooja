import bcrypt

def hash_password(password):
  """Hashes a password using bcrypt with random salting."""
  hashed_password = bcrypt.generate_password_hash(password.encode())
  return hashed_password

def verify_password(username, password):
  """Verifies a user's password during login."""
  # Replace with your logic to retrieve user information based on username/identifier
  user_data = get_user_by_username(username)
  if not user_data:
    return False  # User not found

  # Extract the stored hashed password from the retrieved user data
  stored_hashed_password = user_data["password"]  # Replace with actual field name

  # Verify password using bcrypt.checkpw
  is_password_correct = bcrypt.checkpw(password.encode(), stored_hashed_password)
  return is_password_correct

# This part needs to be replaced with your specific database access logic
def get_user_by_username(username):
  # ... (implementation to retrieve user data from database based on username)
  return user_data

# Login Logic (Example)
def login():
  username = request.form["username"]  # Replace with your form data access method
  password = request.form["password"]  # Replace with your form data access method

  if verify_password(username, password):
    print("senha verificada")
    # Login successful (grant access or display success message)
  else:
    print("senha não verificada")
    # Login failed (display error message)

# Example usage during registration
#new_password = request.form["password"]  # Replace with your form data access method
#hashed_password = hash_password(new_password)

# Store the hashed_password in your database's password field
# ... (your database interaction logic to store user data with hashed password)
