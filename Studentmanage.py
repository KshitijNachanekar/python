# Student Record Management System

students = {}

def add_student():
    name = input("Enter student name: ")
    marks = input("Enter marks: ")
    students[name] = marks
    print("Student added successfully!\n")

def view_students():
    if not students:
        print("No student records found.\n")
    else:
        print("\nStudent Records:")
        for name, marks in students.items():
            print(f"{name} : {marks}")
        print()

def search_student():
    name = input("Enter student name to search: ")
    if name in students:
        print(f"{name}'s marks: {students[name]}\n")
    else:
        print("Student not found.\n")

def delete_student():
    name = input("Enter student name to delete: ")
    if name in students:
        del students[name]
        print("Student deleted successfully!\n")
    else:
        print("Student not found.\n")

while True:
    print("===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        print("Exiting program...")
        break
    else:
        print("Invalid choice!\n")
