import json
import csv
import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name):
        self.name = name
        self.attendance_count = 0

    def attend_class(self):
        self.attendance_count += 1

class AttendanceSystem:
    def __init__(self):
        self.students = {}
        self.load_students()

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = Student(name)
            self.save_students()
            return True
        return False

    def record_attendance(self, name):
        if name in self.students:
            self.students[name].attend_class()
            self.save_students()
            return True
        return False

    def get_attendance(self):
        return {student.name: student.attendance_count for student in self.students.values()}

    def save_students(self):
        with open('students.json', 'w') as outfile:
            json.dump({name: student.__dict__ for name, student in self.students.items()}, outfile)

    def load_students(self):
        try:
            with open('students.json', 'r') as infile:
                data = json.load(infile)
                for name, details in data.items():
                    student = Student(name)
                    student.attendance_count = details['attendance_count']
                    self.students[name] = student
        except FileNotFoundError:
            pass

    def save_to_csv(self):
        with open('attendance.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Attendance Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for student in self.students.values():
                writer.writerow({'Name': student.name, 'Attendance Count': student.attendance_count})

# GUI Implementation
class AttendanceApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Attendance System")

        self.name_label = tk.Label(root, text="Student Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.add_button = tk.Button(root, text="Add Student", command=self.add_student)
        self.add_button.pack()

        self.attend_button = tk.Button(root, text="Record Attendance", command=self.record_attendance)
        self.attend_button.pack()

        self.view_button = tk.Button(root, text="View Attendance", command=self.view_attendance)
        self.view_button.pack()

        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack()

    def add_student(self):
        name = self.name_entry.get()
        if self.system.add_student(name):
            messagebox.showinfo("Success", f"Student {name} added successfully.")
        else:
            messagebox.showwarning("Warning", "Student already exists.")

    def record_attendance(self):
        name = self.name_entry.get()
        if self.system.record_attendance(name):
            messagebox.showinfo("Success", f"Attendance recorded for {name}.")
        else:
            messagebox.showwarning("Warning", "Student not found.")

    def view_attendance(self):
        attendance = self.system.get_attendance()
        attendance_str = "\n".join([f"{name}: {count}" for name, count in attendance.items()])
        messagebox.showinfo("Attendance", attendance_str)

    def save_to_csv(self):
        self.system.save_to_csv()
        messagebox.showinfo("Success", "Data saved to CSV file successfully.")

if __name__ == "__main__":
    system = AttendanceSystem()
    root = tk.Tk()
    app = AttendanceApp(root, system)
    root.mainloop()
