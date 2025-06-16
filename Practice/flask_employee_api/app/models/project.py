class Project:

    def __init__(self,project_id,status,name):
        self.project_id = project_id
        self.status = status
        self.name = name

    def to_dict(self):
        return {
            "project_id" : self.project_id,
            "name" : self.name,
            "status" : self.status
        }