def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "Fail"

# Input marks
name = input("Enter student name: ")

m1 = int(input("Enter marks for Subject 1: "))
m2 = int(input("Enter marks for Subject 2: "))
m3 = int(input("Enter marks for Subject 3: "))

# Calculations
total = m1 + m2 + m3
average = total / 3

grade = calculate_grade(average)

# Output
print("\n----- Result -----")
print("Student Name:", name)
print("Total Marks:", total)
print("Average:", average)
print("Grade:", grade)

if grade == "Fail":
    print("Status: Failed")
else:
    print("Status: Passed")
