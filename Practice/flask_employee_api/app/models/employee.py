from datetime import datetime
from app.models.project import Project


class Employee:

    def __init__(self,emp_id,name,department,salary,designation,location,dob,projects):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary=salary
        self.designation = designation
        self.location = location
        self.dob=dob
        self.projects= [ Project(**p) for p in projects]
    
    def to_dict(self):
        return {
            "emp_id":self.emp_id,
            "name":self.name,
            "department":self.department,
            "salary":self.salary,
            "designation":self.designation,
            "location":self.location,
            "dob":self.dob,
            "projects":[p.to_dict() for p in self.projects]
        }
    
    def is_on_bench(self):

        return len(self.projects)==0
    
    def has_active_projects(self,status):

        return any(p.status==status for p in self.projects)
    
   
    
    