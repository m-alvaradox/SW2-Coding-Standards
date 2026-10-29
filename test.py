"""Student grade management system."""

class Student:
    """Represent a student and their academic grades."""

    def __init__(self, student_id, name):
        """Initialize a student with a valid ID and name."""
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")

        self.student_id = student_id.strip()
        self.name = name.strip()
        self.grades = []
        self.is_passed = False
        self.honor = False

    def add_grades(self, grade):
        """Add a valid numeric grade between 0 and 100."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a numeric value.")

        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")

        self.grades.append(grade)

    def calc_average(self):
        """Calculate the student's average grade."""
        if not self.grades:
            return 0.0

        return sum(self.grades) / len(self.grades)

    def check_honor(self):
        """Determine whether the student qualifies for Honor Roll."""
        self.honor = bool(self.grades) and self.calc_average() >= 90
        return self.honor


    def delete_grade_by_index(self, index):
        """Remove a grade by its zero-based index."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("Index must be an integer.")

        if index < 0 or index >= len(self.grades):
            raise IndexError("Grade index is out of range.")

        removed_grade = self.grades.pop(index)
        return removed_grade

    def delete_grade_by_value(self, grade):
        """Remove the first occurrence of a grade by its value."""
        if grade not in self.grades:
            raise ValueError("Grade value not found.")

        self.grades.remove(grade)
        return grade


    def get_letter_grade(self):
        """Determine the letter grade based on the average."""
        average = self.calc_average()

        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= 60:
            return "D"
        return "F"


    def check_pass_status(self):
        """Determine whether the student has passed."""
        self.is_passed = bool(self.grades) and self.calc_average() >= 60
        return self.is_passed


    def report(self):
        """Display a formatted academic report for the student."""
        average = self.calc_average()
        letter = self.get_letter_grade()
        status = "Passed" if self.check_pass_status() else "Failed"
        honor = "Yes" if self.check_honor() else "No"

        print("\n========== STUDENT REPORT ==========")
        print(f"Student ID: {self.student_id}")
        print(f"Student Name: {self.name}")
        print(f"Number of Grades: {len(self.grades)}")
        print(f"Average Grade: {average:.2f}")
        print(f"Letter Grade: {letter}")
        print(f"Status: {status}")
        print(f"Honor Roll: {honor}")
        print("====================================")



def start_run():
    """Demonstrate student grade management operations."""
    try:
        student = Student("001", "Carlos")

        student.add_grades(95.0)
        student.add_grades(85.0)
        student.add_grades(90.0)

        print("INITIAL GRADES:", student.grades)

        removed = student.delete_grade_by_value(85.0)
        print(f"Removed by value: {removed}")

        removed = student.delete_grade_by_index(0)
        print(f"Removed by index: {removed}")

        print("FINAL GRADES:", student.grades)

        student.report()

    except (ValueError, IndexError) as error:
        print(f"Error: {error}")

def test_invalid_inputs():
    """Test invalid inputs and display validation messages."""
    student = Student("001", "Carlos")
    student.add_grades(95.0)

    test_cases = [
        ("Empty name", lambda: Student("002", "")),
        ("Empty ID", lambda: Student("", "Ana")),
        ("Non-numeric grade", lambda: student.add_grades("Fifty")),
        ("Grade above 100", lambda: student.add_grades(120)),
        ("Negative grade", lambda: student.add_grades(-10)),
        ("Invalid index", lambda: student.delete_grade_by_index(10)),
        ("Negative index", lambda: student.delete_grade_by_index(-1)),
        ("Missing grade", lambda: student.delete_grade_by_value(50)),
    ]

    print("\n========== VALIDATION TESTS ==========")

    for description, action in test_cases:
        try:
            action()
            print(f"[FAIL] {description}: No error detected")
        except (ValueError, IndexError) as error:
            print(f"[PASS] {description}: {error}")


if __name__ == "__main__":
    start_run()
    test_invalid_inputs()
