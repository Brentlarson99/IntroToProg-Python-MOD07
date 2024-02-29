# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   Brent Larson, 02/25/2024, A06
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"



# File Processor Class and Functions
class Person:
    """Represents a person by first and last name.

    ChangeLog:
        Brent Larson, 02/25/2024, Created Person class for basic personal information handling.
    """

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value):
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError("First name must be alphanumeric")

    @property
    def last_name(self):
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError("Last name must be a alphanumeric")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    """Extends Person class to include course enrollment for a student.

    ChangeLog:
        Brent Larson, 02/25/2024, Added Student class to handle student-specific data.
    """

    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self._course_name = course_name

    @property
    def course_name(self):
        return self._course_name

    @course_name.setter
    def course_name(self, value):
        self._course_name = value

    def __str__(self):
        return f"{super().__str__()}, {self.course_name}"


class FileProcessor:
    """Handles file operations for reading and writing student data in JSON format.

      ChangeLog: (Who, When, What)
      Brent Larson, 2/11/2024, Created FileProcessor class to manage file read and write operations.
      """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[Student]):
        """Reads student data from a specified file and returns the updated student data list.

                ChangeLog: (Who, When, What)
                Brent Larson, 2/11/2024, read student data from JSON file.

                :return: list - The updated list of student data.
                """
        file_data = []
        file = None
        try:
            file = open(FILE_NAME, "r")
            file_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message= "The file cannot be read correctly", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()
        for row in file_data:
            student_data.append(Student(row["first_name"], row["last_name"], row["course_name"]))
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[Student]):
        """Writes the current list of student data to a specified file in JSON format.

                ChangeLog: (Who, When, What)
                Brent Larson, 2/11/2024,  write student data to JSON file.

                :return: None
                """
        file_data = []
        for student in student_data:
            file_data.append({"first_name": student.first_name, "last_name": student.last_name, "course_name": student.course_name})
        file = None
        try:
            file = open(FILE_NAME, "w")
            json.dump(file_data, file)
            file.close()
            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            IO.output_error_messages(message= "There was an error writing to the file", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

class IO:
    """Provides static methods for input/output operations related to student course registration.

        ChangeLog: (Who, When, What)
        Brent Larson, 2/11/2024, Created IO class to handle input and output operations.
        """
    @staticmethod
    def output_error_messages(message: str, error: Exception= None):
        """Displays error messages and technical details of the exception.

               ChangeLog: (Who, When, What)
               Brent Larson, 2/11/2024, display error messages.

               :return: None
               """
        print(message, end="\n")
        if error is not None:
            print("--Technical Error--")
            print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def output_menu(menu: str):
        """Prints the user menu.

                ChangeLog: (Who, When, What)
                Brent Larson, 2/11/2024, Added method to display the menu.

                :return: None
                """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """Prompts the user to enter a choice from the menu and returns it.

               ChangeLog: (Who, When, What)
               Brent Larson, 2/11/2024, Added method to input menu choice.

               :return: str - The user's menu choice.
               """
        choice = None
        try:
            choice = input("Enter your menu choice:  ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Invalid choice")
        except Exception as e:
            IO.output_error_messages(e. __str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list[Student]) -> None:
        """Prints out the courses for each student in the student data list.

                ChangeLog: (Who, When, What)
                Brent Larson, 2/11/2024,  display student courses.

                :return: None
                """
        print("-" * 50)
        for student in student_data:
            print(f'Student: {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list[Student]):
        """Prompts the user for student details, updates the student data list, and returns it.

               ChangeLog: (Who, When, What)
               Brent Larson, 2/11/2024, o input student data.

               :return: list - The updated list of student data.
               """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name is invalid")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name is invalid")
            course_name = input("Enter the student's course: ")
            if not course_name.isalpha():
                raise ValueError("The course name is invalid")
            student = Student(student_first_name,
                            student_last_name,
                            course_name)
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}")
        except Exception as e:
            IO.output_error_messages(e. __str__())

        return student_data

# Define the Data Variables
students: list[Student] = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

students = FileProcessor.read_data_from_file(file_name = FILE_NAME, student_data = students)


# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()



    # Present the current data
    if menu_choice == "1":
        students = IO.input_student_data(student_data = students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name = FILE_NAME, student_data = students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
