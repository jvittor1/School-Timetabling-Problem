class Discipline:
    def __init__(self, index, name, teacher, code, semester, ch, course):
        self.index = index
        self.name = name
        self.teacher = teacher
        self.code = code
        self.semester = semester
        self.ch = ch
        self.course = course
        self.weight = 0
        self.schedule = []

    def __str__(self):
        return f"Name: {self.name} - Semester {self.semester} - Course {self.course} - Teacher: {self.teacher} - Code: {self.code} CH - {self.ch} - Schedule: {self.schedule} - Index: {self.index}"

    def add_schedule(self, schedule):
        self.schedule.append(schedule)

    def set_weight(self, weight):
        self.weight = weight
