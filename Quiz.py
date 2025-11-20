import random
import os

students = {}
logged_user = ''
logged = False

SCORE_FILE = "Scores.txt"
QUESTION_FILES = {
    "1": "Dsa.txt",
    "2": "DBMS.txt",
    "3": "Python.txt"
}

def register():
    username = input("Username: ")

    if username in students:
        print("User already exists!")
        return main()

    password = input("Password: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    email = input("Email: ")
    phone = input("Phone: ")
    course = input("Course: ")
    roll_no = input("Roll No: ")
    
    students[username] = {
        "password": password,
        "name": name,
        "age": age,
        "gender": gender,
        "email": email,
        "phone": phone,
        "course": course,
        "roll_no": roll_no,
    }

    print("Registration successful!")
    main()

def login():
    global logged_user, logged
    username = input("Username: ")
    password = input("Password: ")

    if username in students and students[username]["password"] == password:
        logged_user = username
        logged = True
        print(f" Welcome, {students[username]['name']}!")
    else:
        print("Invalid username or password!")
    main()

def show_profile():
    if not logged:
        print("Please login first!")
        return main()

    print("PROFILE")
    for key, value in students[logged_user].items():
        if key != "password":
            print(f"{key}: {value}")
  
    main()

def update_profile():
    if not logged:
        print("Please login first!")
        return main()

    for field in students[logged_user]:
        if field == "password":
            continue
        new_value = input(f"{field} ({students[logged_user][field]}): ")
        if new_value.strip():
            students[logged_user][field] = new_value
    print("Profile updated!")
    main()

def attempt_quiz():
    if not logged:
        print("Please login first!")
        return main()

    print("QUIZ CATEGORIES")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    choice = input("Enter choice (1-3): ")

    if choice not in QUESTION_FILES:
        print("Invalid category!\n")
        return main()

    file_name = QUESTION_FILES[choice]
    category = file_name[:-4].upper()

    if not os.path.exists(file_name):
        print(f"No question file found for {category}!\n")
        return main()

    with open(file_name, "r") as f:
        lines = f.readlines()

    questions = []
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) == 6:
            questions.append(parts)
        else:
            print(f"⚠️ Skipping invalid question line: {line.strip()}")

    if not questions:
        print("No valid questions found in this category file!\n")
        return main()

    random.shuffle(questions)
    score = 0
    total = min(10, len(questions))

    print(f"Starting {category} Quiz ({total} questions)")

    for i, q in enumerate(questions[:total], start=1):
        print(f"\nQ{i}. {q[0]}")
        print(f"a) {q[1]}\nb) {q[2]}\nc) {q[3]}\nd) {q[4]}")
        ans = input("Your answer (a/b/c/d): ").lower()
        if ans == q[5].lower():
            print(" Correct!")
            score += 1
        else:
            print(f"Wrong! Correct: {q[5]}\n")

    print(f"You scored {score}/{total}\n")
    save_score(category, score, total)
    main()

def save_score(category, score, total):
    with open(SCORE_FILE, "a") as f:
        f.write(f"{logged_user},{category},{score}/{total}\n")

def view_score():
    if not logged:
        print("Please login first!")
        return main()

    print("YOUR SCORES:")
    found = False

    if not os.path.exists(SCORE_FILE):
        print("No scores found yet!\n")
        return main()

    with open(SCORE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                user, category, marks = parts[:3]
                if user == logged_user:
                    print(f"{category} | {marks}")
                    found = True

    if not found:
        print("No quiz attempted yet!")
    main()

def logout():
    global logged_user, logged
    logged_user = ''
    logged = False
    print("Logged out!")
    main()

def main():
    response = input('''
 MAIN MENU 
1. Register
2. Login
3. Profile
4. Update Profile
5. Attempt Quiz
6. View Score
7. Logout
Select option: ''')

    if response == '1':
        register()
    elif response == '2':
        login()
    elif response == '3':
        show_profile()
    elif response == '4':
        update_profile()
    elif response == '5':
        attempt_quiz()
    elif response == '6':
        view_score()
    elif response == '7':
        logout()
    else:
        print("Invalid choice!")
        main()

main()
