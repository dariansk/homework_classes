import random


# считает среднюю оценку по одному курсу для 1 человека (если оценок нет, то в ответе 0):
def average_grade_for_course(course, courses):
    average_course_grade = 0
    if course in courses.keys() and isinstance(courses[course], list):
        if len(courses[course]) != 0:
            average_course_grade = sum(courses[course]) / len(courses[course])
    return average_course_grade


# считает среднюю оценку по всем курсам для 1 человека:
def average_all_courses_grade(courses):
    average_grade_all = 0
    grades_sum = 0
    grades_quantity = 0
    if len(courses) != 0:
        for entry in courses.keys():
            grades_sum += sum(courses[entry])
            grades_quantity += len(courses[entry])
        average_grade_all = round(grades_sum / grades_quantity, 2)
    return average_grade_all


# считает среднюю оценку по 1 курсу для студентов:
def average_course_grade_for_students(course, list_of_persons):
    average_grade_num = 0
    sum_of_grades = 0
    if len(list_of_persons) != 0:
        quantity = 0
        for entry in list_of_persons:
            if course in entry.courses_in_progress.keys():
                sum_of_grades += average_grade_for_course(course, entry.courses_in_progress)
                quantity += 1
        if quantity > 0:
            average_grade_num = round(sum_of_grades / quantity, 2)
        else:
            average_grade_num = 0

    return average_grade_num


# считает среднюю оценку по 1 курсу для преподавателей:
def average_course_grade_for_lecturers(course, list_of_persons):
    average_grade_num = 0
    sum_of_grades = 0
    if len(list_of_persons) != 0:
        quantity = 0
        for entry in list_of_persons:
            if course in entry.courses_attached.keys():
                sum_of_grades += average_grade_for_course(course, entry.courses_attached)
                quantity += 1
        if quantity > 0:
            average_grade_num = round(sum_of_grades / quantity, 2)
        else:
            average_grade_num = 0

    return average_grade_num


class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = {}
        self.courses_in_progress = {}

    def __str__(self):
        if self.courses_in_progress != {}:
            str_of_progress_courses = ', '.join(list(self.courses_in_progress.keys()))
        else:
            str_of_progress_courses = 'Курсов нет'
        if self.finished_courses != {}:
            str_of_finished_courses = ', '.join(list(self.finished_courses.keys()))
        else:
            str_of_finished_courses = 'Курсов нет'
        return f'Имя: {self.name}\nФамилия: {self.surname}' + f'\nСредняя оценка за домашние задания:' f'{average_all_courses_grade(self.courses_in_progress)}' \
               f'\nКурсы в процессе изучения:' \
               f' {str_of_progress_courses}' \
               f'\nЗавершенные курсы:' \
               f' {str_of_finished_courses}'

    def __gt__(self, other):
        result = False
        if average_all_courses_grade(self.courses_in_progress) > average_all_courses_grade(other.courses_in_progress):
            result = True
        return result

# метод для оценки преподавателя
    def rate_lecturer(self, other, course, grade):
        if isinstance(other, Lecturer) and course in self.courses_in_progress.keys() and course in other.courses_attached.keys() and 1 <= grade <= 10:
            if other.courses_attached[course] is not None:
                other.courses_attached[course] += [grade]
            else:
                other.courses_attached[course] = [grade]
        else:
            return 'Нельзя поставить оценку'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = {}

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# класс лекторов, наследующий класс Mentor
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = {}

    def __str__(self):
        return super().__str__() + f'\nСредняя оценка от студентов:' \
                                   f' {average_all_courses_grade(self.courses_attached)}'

    def __gt__(self, other):
        result = False
        if average_all_courses_grade(self.courses_attached) > average_all_courses_grade(other.courses_attached):
            result = True
        return result


# класс проверяющих, наследующий класс Mentor
class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = {}

    def rate_student(self, other, course, grade):
        if isinstance(other, Student) and course in self.courses_attached.keys() and course in other.courses_in_progress.keys() and 1 <= grade <= 10:
            if other.courses_in_progress[course] is not None:
                other.courses_in_progress[course] += [grade]
            else:
                other.courses_in_progress[course] = [grade]
        else:
            return 'Нельзя поставить оценку'


# для проверки нужна функция для создания случайного набора курсов с оценками:
def random_courses():
    courses = ['Python', 'Git', 'Math', 'Physics']
    quantity = random.randint(1, len(courses))
    my_courses = {}
    for i in range(1, quantity+1):
        scores = []
        for ii in range(1, random.randint(2, 10)):
            scores += [random.randint(1, 10)]
        my_courses.setdefault(random.choice(courses), scores)
    return my_courses


# создадим по паре экземпляров каждого класса и присвоим им курсы.
# Законченные курсы у студентов и курсы у проверяющих - без оценок.
bob_dilan = Student('Bob', 'Dylan')
bob_dilan.courses_in_progress = random_courses()
bob_dilan.finished_courses = dict.fromkeys(random_courses(), [])

david_bowie = Student('David', 'Bowie')
david_bowie.courses_in_progress = random_courses()
david_bowie.finished_courses = dict.fromkeys(random_courses(), [])

katy_perry = Reviewer('Katy', 'Perry')
katy_perry.courses_attached = dict.fromkeys(random_courses(), [])

lady_gaga = Reviewer('Lady', 'Gaga')
lady_gaga.courses_attached = dict.fromkeys(random_courses(), [])

plasido_domingo = Lecturer('Plasido', 'Domingo')
plasido_domingo.courses_attached = random_courses()

luciano_pavrotti = Lecturer('Luciano', 'Pavarotti')
luciano_pavrotti.courses_attached = random_courses()

# испытания начинаются: выведем на печать всех героев:

print(bob_dilan)
print(david_bowie)
print(katy_perry)
print(lady_gaga)
print(plasido_domingo)
print(luciano_pavrotti)
print()

# сравним студентов
if bob_dilan > david_bowie:
    print(f'{bob_dilan.name} {bob_dilan.surname}' + ' учится лучше, чем ' + f'{david_bowie.name} {david_bowie.surname}')
else:
    print(f'{david_bowie.name} {david_bowie.surname}' + ' учится лучше, чем ' + f'{bob_dilan.name} {bob_dilan.surname}')
print()

# сравним лекторов
if plasido_domingo > luciano_pavrotti:
    print(f'{plasido_domingo.name} {plasido_domingo.surname}' + ' читает лекции лучше, чем ' + f'{luciano_pavrotti.name} {luciano_pavrotti.surname}')
else:
    print(f'{luciano_pavrotti.name} {luciano_pavrotti.surname}' + ' читает лекции лучше, чем ' + f'{plasido_domingo.name} {plasido_domingo.surname}')
print()

# посчитаем среднюю оценку по курсу для студентов
our_courses = ['Python', 'Git', 'Math', 'Physics']
list_of_students = [bob_dilan, david_bowie]
for course in our_courses:
    grade = average_course_grade_for_students(course, list_of_students)
    print(f'Средняя оценка студентов по курсу {course} : {grade}')
print()

# посчитаем среднюю оценку по курсу для лекторов:
list_of_lecturers = [plasido_domingo, luciano_pavrotti]
for course in our_courses:
    grade = average_course_grade_for_lecturers(course, list_of_lecturers)
    print(f'Средняя оценка лекторов по курсу {course} : {grade}')
print()

# поставим оценки всем студентам наугад, для кого-то да совпадет по прикрепленным курсам:
for key in katy_perry.courses_attached:
    katy_perry.rate_student(bob_dilan, key, random.randint(1, 10))
    katy_perry.rate_student(david_bowie, key, random.randint(1, 10))

for key in lady_gaga.courses_attached:
    lady_gaga.rate_student(bob_dilan, key, random.randint(1, 10))
    lady_gaga.rate_student(david_bowie, key, random.randint(1, 10))

# посмотрим как студенты выглядят теперь:
print(bob_dilan)
print(david_bowie)
print()

# поставим оценки лекторам
for key in david_bowie.courses_in_progress:
    david_bowie.rate_lecturer(plasido_domingo, key, random.randint(1, 10))
    david_bowie.rate_lecturer(luciano_pavrotti, key, random.randint(1, 10))

for key in bob_dilan.courses_in_progress:
    bob_dilan.rate_lecturer(plasido_domingo, key, random.randint(1, 10))
    bob_dilan.rate_lecturer(luciano_pavrotti, key, random.randint(1, 10))

# посмотрим как лекторы выглядят теперь:
print(plasido_domingo)
print(luciano_pavrotti)