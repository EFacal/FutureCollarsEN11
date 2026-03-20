# ===================== CLASSES =====================

class Student:
    def __init__(self, firstname, lastname, classname):
        self.firstname = firstname
        self.lastname = lastname
        self.classname = classname


class Teacher:
    def __init__(self, firstname, lastname, subject, classes):
        self.firstname = firstname
        self.lastname = lastname
        self.subject = subject
        self.classes = classes


class HomeroomTeacher:
    def __init__(self, firstname, lastname, classname):
        self.firstname = firstname
        self.lastname = lastname
        self.classname = classname


# ===================== DATA STORAGE =====================

students = []
teachers = []
homeroom_teachers = []


# ===================== SEARCH FUNCTIONS =====================

def find_student(firstname, lastname):
    for s in students:
        if s.firstname == firstname and s.lastname == lastname:
            return s
    return None


def find_teacher(firstname, lastname):
    for t in teachers:
        if t.firstname == firstname and t.lastname == lastname:
            return t
    return None


def find_homeroom_teacher(firstname, lastname):
    for h in homeroom_teachers:
        if h.firstname == firstname and h.lastname == lastname:
            return h
    return None


# ===================== CREATE MENU =====================

def create_menu():
    while True:
        print("\nCreate: student | teacher | homeroom teacher | end")
        choice = input()

        if choice == "student":
            firstname = input("First name: ")
            lastname = input("Last name: ")
            classname = input("Class name: ")
            students.append(Student(firstname, lastname, classname))
            print("Student created")

        elif choice == "teacher":
            firstname = input("First name: ")
            lastname = input("Last name: ")
            subject = input("Subject: ")

            classes = []
            print("Enter classes (empty line to finish)")
            while True:
                c = input()
                if c == "":
                    break
                classes.append(c)

            teachers.append(Teacher(firstname, lastname, subject, classes))
            print("Teacher created")

        elif choice == "homeroom teacher":
            firstname = input("First name: ")
            lastname = input("Last name: ")
            classname = input("Class name: ")
            homeroom_teachers.append(HomeroomTeacher(firstname, lastname, classname))
            print("Homeroom teacher created")

        elif choice == "end":
            break

        else:
            print("Invalid option")


# ===================== MANAGE MENU =====================

def manage_menu():
    while True:
        print("\nManage: class | student | teacher | homeroom teacher | end")
        choice = input()

        if choice == "class":
            classname = input("Class name: ")

            print("Students:")
            for s in students:
                if s.classname == classname:
                    print(s.firstname, s.lastname)

            print("Homeroom teacher:")
            found = False
            for h in homeroom_teachers:
                if h.classname == classname:
                    print(h.firstname, h.lastname)
                    found = True
            if not found:
                print("None")

        elif choice == "student":
            firstname = input("First name: ")
            lastname = input("Last name: ")

            s = find_student(firstname, lastname)
            if s is None:
                print("Student not found")
            else:
                print("Class:", s.classname)
                print("Teachers:")
                for t in teachers:
                    if s.classname in t.classes:
                        print(t.firstname, t.lastname)

        elif choice == "teacher":
            firstname = input("First name: ")
            lastname = input("Last name: ")

            t = find_teacher(firstname, lastname)
            if t is None:
                print("Teacher not found")
            else:
                print("Classes:")
                for c in t.classes:
                    print(c)

        elif choice == "homeroom teacher":
            firstname = input("First name: ")
            lastname = input("Last name: ")

            h = find_homeroom_teacher(firstname, lastname)
            if h is None:
                print("Homeroom teacher not found")
            else:
                print("Students:")
                for s in students:
                    if s.classname == h.classname:
                        print(s.firstname, s.lastname)

        elif choice == "end":
            break

        else:
            print("Invalid option")


# ===================== MAIN PROGRAM =====================

while True:
    print("\nCommands: create | manage | end")
    command = input()

    if command == "create":
        create_menu()

    elif command == "manage":
        manage_menu()

    elif command == "end":
        print("Program terminated")
        break

    else:
        print("Invalid command")