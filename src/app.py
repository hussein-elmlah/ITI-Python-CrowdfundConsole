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
    def __init__(self, title, details, target_amount, start_date, end_date, owner):
        self.title = title
        self.details = details
        self.target_amount = target_amount
        self.start_date = start_date
        self.end_date = end_date
        self.owner = owner

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
        if not self.validate_email(email):
            print("Invalid email format.")
            return
        if self.is_email_unique(email):
            print("Email already exists. Please choose a different email.")
            return
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        if not self.validate_password(password, confirm_password):
            print("Invalid password or password mismatch.")
            return
        phone = input("Enter your phone number: ")
        if not self.validate_phone(phone):
            print("Invalid phone number format.")
            return       
        
        user = User(first_name, last_name, email, password, phone)
        self.users.append(user)
        self.save_data()
        print("Registration successful.")

    def login_user(self):
        print("Login")
        email = input("Enter your email: ")
        if not self.validate_email(email):
            print("Invalid email format.")
            return
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
        if not self.is_title_unique(title):
            print("Project with the same title already exists. Please choose a different title.")
            return
        details = input("Enter project details: ")
        target_amount = input("Enter target amount: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        if not self.validate_date(start_date):
            print("Invalid date format.")
            return
        end_date = input("Enter end date (YYYY-MM-DD): ")
        if not self.validate_date(end_date):
            print("Invalid date format.")
            return

        project = Project(title, details, target_amount, start_date, end_date, self.logged_in_user.email)
        self.projects.append(project)
        self.save_data()
        print("Project created successfully.")

    def edit_project(self):
        if not self.logged_in_user:
            print("Please login first.")
            return

        print("Edit Project")
        title = input("Enter project title to edit: ")
        found_project = self.find_project(title)
        if found_project is None:
            print("Project not found.")
            return

        if found_project.owner != self.logged_in_user.email:
            print("You are not authorized to edit this project.")
            return

        new_title = input("Enter new project title: ")
        if new_title != title and not self.is_title_unique(new_title):
            print("Project with the same title already exists. Please choose a different title.")
            return

        details = input("Enter new project details: ")
        target_amount = input("Enter new target amount: ")
        start_date = input("Enter new start date (YYYY-MM-DD): ")
        if not self.validate_date(start_date):
            print("Invalid date format.")
            return
        end_date = input("Enter new end date (YYYY-MM-DD): ")
        if not self.validate_date(end_date):
            print("Invalid date format.")
            return

        found_project.title = new_title
        found_project.details = details
        found_project.target_amount = target_amount
        found_project.start_date = start_date
        found_project.end_date = end_date
        self.save_data()
        print("Project edited successfully.")

    def delete_project(self):
        if not self.logged_in_user:
            print("Please login first.")
            return

        print("Delete Project")
        title = input("Enter project title to delete: ")
        found_project = self.find_project(title)
        if found_project is None:
            print("Project not found.")
            return

        if found_project.owner != self.logged_in_user.email:
            print("You are not authorized to delete this project.")
            return

        self.projects.remove(found_project)
        print("Project deleted successfully.")
        self.save_data()

    def view_projects(self):
        print("\nProjects")
        print("========")
        for project in self.projects:
            print(f"Title: {project.title}, Details: {project.details}, Target Amount: {project.target_amount}, Start Date: {project.start_date}, End Date: {project.end_date}")

    def search_projects_by_date(self, date):
        found_projects = [project for project in self.projects if project.start_date <= date and project.end_date >= date]
        if found_projects:
            print("\nFound projects:")
            print("==============")
            for project in found_projects:
                print(f"Title: {project.title}, Details: {project.details}, Target Amount: {project.target_amount}, Start Date: {project.start_date}, End Date: {project.end_date}")
        else:
            print("No projects found for the specified date.")

    def search_projects_by_title(self, title):
        found_projects = [project for project in self.projects if project.title.lower() == title.lower()]
        if found_projects:
            print("\nFound projects:")
            print("==============")
            for project in found_projects:
                print(f"Title: {project.title}, Details: {project.details}, Target Amount: {project.target_amount}, Start Date: {project.start_date}, End Date: {project.end_date}")
        else:
            print("No projects found with the specified title.")

    def find_project(self, title):
        for project in self.projects:
            if project.title.lower() == title.lower():
                return project
        return None

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

    # Validation functions
    def validate_email(self, email):
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
    
    def is_email_unique(self, email):
        for user in self.users:
            if user.email == email:
                return True
        return False

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

    def is_title_unique(self, title):
        for project in self.projects:
            if project.title.lower() == title.lower():
                return False
        return True

# Main function
def main():
    app = CrowdFundingApp()

    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Create Project")
        print("4. Edit Project")
        print("5. Delete Project")
        print("6. View Projects")
        print("7. Search Projects by Date")
        print("8. Search Projects by Title")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            app.register_user()
        elif choice == "2":
            app.login_user()
        elif choice == "3":
            app.create_project()
        elif choice == "4":
            app.edit_project()
        elif choice == "5":
            app.delete_project()
        elif choice == "6":
            app.view_projects()
        elif choice == "7":
            date = input("Enter date (YYYY-MM-DD): ")
            app.search_projects_by_date(date)
        elif choice == "8":
            title = input("Enter project title: ")
            app.search_projects_by_title(title)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
