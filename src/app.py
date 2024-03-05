import json
import re
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone

class Project:
    def __init__(self, title, details, target_amount, start_date, end_date):
        self.title = title
        self.details = details
        self.target_amount = target_amount
        self.start_date = start_date
        self.end_date = end_date

class CrowdFundingApp:
    def __init__(self):
        self.users = []
        self.projects = []
        self.logged_in_user = None
        self.load_data()

    def register_user(self):
        print("Registration")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        phone = input("Enter your phone number: ")
        
        if not self.validate_email(email):
            print("Invalid email format.")
            return
        if not self.validate_password(password, confirm_password):
            print("Invalid password or password mismatch.")
            return
        if not self.validate_phone(phone):
            print("Invalid phone number format.")
            return
        
        user = User(first_name, last_name, email, password, phone)
        self.users.append(user)
        print("Registration successful.")
        self.save_data()

    def login_user(self):
        print("Login")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        for user in self.users:
            if user.email == email and user.password == password:
                self.logged_in_user = user
                print("Login successful.")
                return
        print("Invalid email or password.")

    def create_project(self):
        if not self.logged_in_user:
            print("Please login first.")
            return

        print("Create Project")
        title = input("Enter project title: ")
        details = input("Enter project details: ")
        target_amount = input("Enter target amount: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        if not self.validate_date(start_date) or not self.validate_date(end_date):
            print("Invalid date format.")
            return

        project = Project(title, details, target_amount, start_date, end_date)
        self.projects.append(project)
        print("Project created successfully.")
        self.save_data()

    def view_projects(self):
        print("Projects")
        for project in self.projects:
            print(f"Title: {project.title}, Details: {project.details}, Target Amount: {project.target_amount}, Start Date: {project.start_date}, End Date: {project.end_date}")

    def save_data(self):
        with open('users.json', 'w') as f:
            json.dump([vars(user) for user in self.users], f)
        with open('projects.json', 'w') as f:
            json.dump([vars(project) for project in self.projects], f)

    def load_data(self):
        try:
            with open('users.json', 'r') as f:
                user_data = json.load(f)
                self.users = [User(**user) for user in user_data]
        except FileNotFoundError:
            pass
        try:
            with open('projects.json', 'r') as f:
                project_data = json.load(f)
                self.projects = [Project(**project) for project in project_data]
        except FileNotFoundError:
            pass

    def validate_email(self, email):
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    def validate_password(self, password, confirm_password):
        return password == confirm_password and len(password) >= 6

    def validate_phone(self, phone):
        return re.match(r'^01[0-2]\d{8}$', phone)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

# Main function
def main():
    app = CrowdFundingApp()

    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Create Project")
        print("4. View Projects")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            app.register_user()
        elif choice == "2":
            app.login_user()
        elif choice == "3":
            app.create_project()
        elif choice == "4":
            app.view_projects()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
