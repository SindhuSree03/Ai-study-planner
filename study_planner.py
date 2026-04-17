subjects = []

FILE_NAME = "subjects.txt"



# ---- Add Subject ----
def add_subject():
    name = input("Enter subject name: ")
    deadline = int(input("Enter deadline (days): "))
    difficulty = int(input("Enter difficulty (1-5): "))
    hours = float(input("Enter total hours required: "))

    # Priority logic
    priority = (difficulty * 2) + (10 - deadline)

    subjects.append({
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "hours": hours,
        "priority": priority
    })

    print("✅ Subject added successfully!")
    save_subjects()

def save_subjects():
    with open(FILE_NAME, "w") as file:
        for sub in subjects:
            file.write(f"{sub['name']},{sub['deadline']},{sub['difficulty']},{sub['hours']},{sub['priority']}\n")

def load_subjects():
    subjects.clear()
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                name, deadline, difficulty, hours, priority = line.strip().split(",")

                subjects.append({
                    "name": name,
                    "deadline": int(deadline),
                    "difficulty": int(difficulty),
                    "hours": float(hours),
                    "priority": int(priority)
                })
    except FileNotFoundError:
        pass


# ---- Format Time ----
def format_time(time):
    hours = int(time)
    minutes = int((time - hours) * 60)
    return f"{hours}:{minutes:02d}"


# ---- Generate Smart Plan ----
def generate_plan():
    timetable = ""   # ✅ string to store data

    if len(subjects) < 3:
        print("Please add at least 3 subjects.")
        return

    print("\n========== 📅 SMART STUDY TIMETABLE ==========\n")

    timetable += "📅 Smart Study Timetable\n\n"

    # Sort subjects by priority
    sorted_subjects = sorted(subjects, key=lambda x: x["priority"], reverse=True)

    morning_subjects = sorted_subjects[:2]
    evening_subjects = sorted_subjects[2:5]

    # ---- MORNING SESSION ----
    print("🌅 Morning Session (2 hrs):\n")
    timetable += "Morning Session (2 hrs)\n"

    header = "--------------------------------------------------\n"
    header += "| Time        | Subject        | Duration        |\n"
    header += "--------------------------------------------------\n"

    print(header)
    timetable += header

    start_time = 6.0
    time_per_subject = 1

    for sub in morning_subjects:
        end_time = start_time + time_per_subject

        line = f"| {format_time(start_time)}-{format_time(end_time)} | {sub['name']:<14} | 1 hr          |\n"
        print(line, end="")
        timetable += line

        start_time = end_time

        break_line = f"| {format_time(start_time)}-{format_time(start_time+0.5)} | {'Break':<14} | 0.5 hr        |\n"
        print(break_line, end="")
        timetable += break_line

        start_time += 0.5

    footer = "--------------------------------------------------\n"
    print(footer, end="")
    timetable += footer

    # ---- EVENING SESSION ----
    print("\n🌙 Evening Session (5 hrs):\n")
    timetable += "\nEvening Session (5 hrs)\n"

    print(header, end="")
    timetable += header

    start_time = 18.0
    time_per_subject = round(5/3, 2)

    for sub in evening_subjects:
        end_time = start_time + time_per_subject

        line = f"| {format_time(start_time)}-{format_time(end_time)} | {sub['name']:<14} | {time_per_subject} hrs |\n"
        print(line)
        timetable += line

        start_time = end_time

        break_line = f"| {format_time(start_time)}-{format_time(start_time+0.5)} | {'Break':<14} | 0.5 hr        |\n"
        print(break_line)
        timetable += break_line

        start_time += 0.5

    print(footer)
    timetable += footer

    # ---- SAVE TO FILE ----
    with open("timetable.txt", "w", encoding="utf-8") as file:
        file.write(timetable)

    print("\n✅ Timetable saved to timetable.txt")


def suggest_now():
    if not subjects:
        print("No subjects available.")
        return

    best = max(subjects, key=lambda x: x["priority"])

    print("\n🔥 Study this NOW:")
    print(f"{best['name']} (Priority: {best['priority']})")

load_subjects()


# ---- Main Menu ----
while True:
    print("\n====== AI Study Planner ======")
    print("1. Add Subject")
    print("2. Generate Study Plan")
    print("3. Suggest what to study now")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_subject()
    elif choice == "2":
        generate_plan()
    elif choice == "3":
        suggest_now()
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice! Try again.")