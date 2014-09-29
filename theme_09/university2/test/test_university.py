import theme_09.university2.const as const
import theme_09.university2.other as other
import theme_09.university2.person as person
import theme_09.university2.unit as unit


Person = person.Person
Employee = person.Employee
Rector = person.Rector
ViceRector = person.ViceRector
Dean = person.Dean
Teacher = person.Teacher
Student = person.Student

Unit = unit.Unit
Rectorate = unit.Rectorate
Department = unit.Department
Faculty = unit.Faculty
Group = unit.Group

Consultation = other.Consultation
Exam = other.Exam
today = other.today
timedelta = other.timedelta


if __name__ == '__main__':
    import doctest
    gl = globals()
    doctest.testmod(m=person, globs=gl)
    doctest.testmod(m=unit, globs=gl)
    doctest.testmod(m=other, globs=gl)
