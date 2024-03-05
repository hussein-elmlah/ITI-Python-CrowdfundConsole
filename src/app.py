import json

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
        print("init called.")

    def register_user(self):
        print("Registration")

    def login_user(self):
        print("Login")

    def create_project(self):
        if not self.logged_in_user:
            print("Please login first.")
            return
        
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
