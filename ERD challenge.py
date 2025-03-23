import sqlite3 as sql
import random
import pandas as pd
import pathlib as path
file_path = path.Path(__file__).parent / "ERD challenge.db"

data = sql.connect("ERD challenge.db") #makes a new database


def clear_db():
    data = sql.connect("ERD challenge.db") #makes a new database
    try:
        data.execute("DROP TABLE IF EXISTS Professors;")
        data.execute("DROP TABLE IF EXISTS Courses;")
        data.execute("DROP TABLE IF EXISTS Students;")
        data.execute("DROP TABLE IF EXISTS Enrollments;")
        data.execute("DROP TABLE IF EXISTS StudentID;")
        data.execute("DROP TABLE IF EXISTS ProffeserID;")


        data.commit()
    except:
        print("Unable to clear")
    data.close()



def build_table():
    data = sql.connect("ERD challenge.db") #makes a new database

    #make the primary key6 integer, so when new stuffs is added it increments by 1


        
    try:
        data.execute("""create table Professors
                        (professor_id INTEGER PRIMARY KEY,
                        last_name CHAR(50),
                        first_name CHAR(50),
                        email char(128));""")
        
        data.execute("""Create table Courses
                        (course_id INTEGER primary key,
                        course_name CHAR(50),
                        course_desc CHAR(128),
                        professor_id INTEGER,
                        FOREIGN KEY (professor_id) REFERENCES Professors(professor_id));""")
        
        data.execute("""CREATE TABLE Students (
                        student_id INTEGER PRIMARY KEY,
                        first_name CHAR(50),
                        last_name CHAR(50),
                        email CHAR(128),
                        date_of_birth DATE);""")
        
        data.execute("""CREATE TABLE Enrollments (
                        enrollment_id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        course_id INTEGER,
                        enrollment_date DATE,
                        FOREIGN KEY (student_id) REFERENCES Students(student_id),
                        FOREIGN KEY (course_id) REFERENCES Courses(course_id));""")
        
        #data.execute("""CREATE TABLE StudentID (
        #                student_id INTEGER PRIMARY KEY,
        #                FOREIGN KEY (student_id) REFERENCES Students(student_id),
        #                username CHAR(50),
        #                password CHAR(50))
        #                grades CHAR(1);""")
        
        #data.execute("""CREATE TABLE ProffeserID (
        #                professor_id INTEGER PRIMARY KEY,
        #                FOREIGN KEY (professor_id) REFERENCES Professers(professor_id),
        #                username CHAR(50),
        #                password CHAR(50));""")
        #"""
        print("Table created successfully")
    except:
        print("Database already made")
    data.close()

def insert_data():
    data = sql.connect("ERD challenge.db") #makes a new database
    first_names = ('Jack', 'Brandon', 'James', "Archie", "Lewis", "Kavan")
    last_names = ("Mortimer", "Dyton", "Townsend",
                  "Calverley", "Caverly", "Hart")
    professors = [('Oliver', 'Mills', 'oliver.mills@cirencester.ac.uk'),
                  ('Tyler', 'Hyde', 'TylerHydes@cirencester.ac.uk'),
                  ('Simon', 'Jones', 'Simon.Jones@cirencester.ac.uk'),
                  ('Ian', 'Slater', 'Ian.Slater@cirencester.ac.uk')]
    courses = [('coding', 'coding course', 1),
               ('Business', 'Business course', 2),
               ('Planning', 'Planning course', 3),
               ('Maths', 'Maths course', 4)]
    try:
        for _ in range(25):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()
                                            }@cirencester.ac.uk"
            date_of_birth = f"{random.randint(
                2002, 2007)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

            sql_statement = """INSERT INTO Students(first_name, last_name, email, date_of_birth)
                               VALUES (?, ?, ?, ?);"""
            data.execute(sql_statement, (first_name,last_name, email, date_of_birth))
        for professor in professors:
            sql_statement = """INSERT INTO Professors(first_name, last_name, email)
                               VALUES (?, ?, ?);"""
            data.execute(sql_statement, professor)

        # Insert courses
        for course in courses:
            sql_statement = """INSERT INTO Courses(course_name, course_desc, professor_id)
                               VALUES (?, ?, ?);"""
            data.execute(sql_statement, course)

        # Insert enrollments
        for student_id in range(1, 26):
            for course_id in range(1, 5):
                enrollment_date = f"{random.randint(2022, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                sql_statement = """INSERT INTO Enrollments(student_id, course_id, enrollment_date)
                                   VALUES (?, ?, ?);"""
                data.execute(sql_statement, (student_id, course_id, enrollment_date))

            
        data.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
    data.close()

def select_professor_by_email():
    data = sql.connect("ERD challenge.db") #makes a new database
    for row in (data.execute("select email from Professors")):
        print(*row)
    email = input("Enter the email")
    try:
        select_str = """
            SELECT Courses.course_name
            FROM Courses
            JOIN Professors ON Courses.professor_id = Professors.professor_id
            WHERE Professors.email = ?
        """
        cursor = data.execute(select_str, (email,))

        # Print the course names
        print("Courses taught by the professor with the given email:")
        for row in cursor:
            print(row[0])
    except:
        print("Invalid email and too bad theres no loop")
    data.close()
    
    
def select_student_by_course():
    data = sql.connect("ERD challenge.db") #makes a new database
    for row in (data.execute("select course_name from Courses")):
        print(*row)
    email = input("Enter the Course Name: ")

    try:
        select_str = """
            SELECT Students.first_name || ' ' || Students.last_name
            FROM Students
            JOIN Enrollments ON Students.student_id = Enrollments.student_id
            JOIN Courses ON Enrollments.course_id = Courses.course_id
            WHERE Courses.course_name = ?
        """
        cursor = data.execute(select_str, (email,))

        # Print the course names
        print("Students on that course: ")
        for row in cursor:
            print(row[0])
    except:
        print("Invalid course and too bad theres no loop")
    data.close()
    
#
"""
5. create a login system for both professors and students, logins need to be stored safely within the database, research how to store that safely, I recommend looking up hashing
You will need to alter your database structure to accommodate all the new additions
6. Add an interface to allow a professor once logged in to be able to enter student grades into the database
7. Add an interface to allow students to see all of their grades, like a report card
"""


clear_db()
build_table()
insert_data()
#select_professor_by_email()
select_student_by_course()
