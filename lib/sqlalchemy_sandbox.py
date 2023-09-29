#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime())
    default = datetime.now()   
     
    def __repr__(self):
      return f"Student {self.id}:" \
            + f"{self.name}," \
            + f"Grade {self.grade}"

if __name__ == '__main__':
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        albert_einstein = Student(
            name= "Albert Einstein",
            email = "albert.einstain@zurich.edu",
            grade = 6,
            birthday = datetime(
                year =1879,
                month=3,
                day=14
                )
            )
            
        alan_turing = Student(
            name = "Alan Turing",
            email = "alan.turing@sherborne.edu",
            grade = 11,
            birthday = datetime(
                year=1912,
                month=6,
                day=23
                )  
            )
        


        session.bulk_save_objects([albert_einstein, alan_turing])
        session.commit()

            #print(f"New student ID is {albert_einstein.id}.")
            #print(f"New student ID is {alan_turing.id}.")
            
            #Read Records
        students = session.query(Student)
        print([student for student in students])
            

            #using all() instance method
        #students = session.query(Student).all()

        #print(students)

        #Selecting Only Certain Columns   
        names = session.query(Student.name).all()
        print(names)

        #Ordering
        student_by_name = session.query(Student.name).order_by(Student.name).all()
        print(student_by_name)

        #To sort results in descending order, we need to use the desc() function from the sqlalchemy module:
        students_by_grade_desc = session.query(Student.name, Student.grade).order_by(desc(Student.grade)).all()
        print(students_by_grade_desc)

        #Limiting
        oldest_student = session.query(Student.name, Student.birthday).order_by(Student.birthday).limit(1).all()
        print(oldest_student)

        #func
        student_count = session.query(func.count(Student.id)).first()
        print(student_count)

        #Filtering
        query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11).all()
        for record in query:
             print(record.name)

        #Updating Data
        for student in session.query(Student):
             student.grade +=1
             session.commit()

        print([(student.name, student.grade) for student in session.query(Student)])
        
        #using update() method
        session.query(Student).update({Student.grade: Student.grade +1})
        print([(student.name, student.grade) for student in session.query(Student)])
                  
        #Deleting Data
        query = session.query(Student).filter(Student.name =="Albert Einstein")
        
        #retrieve first matching record as object
        albert_einstein =query.first()
        session.delete(albert_einstein)
        session.commit()

         # try to retrieve deleted record
        albert_einstein = query.first()
        print(albert_einstein)
        
        #it prints none beacause it has been deleted


  