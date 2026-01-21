# Dependency inversion principle example

# class MYSQLDataabase:

#     def save(self,data):
#         print(f"Saving {data} to MySQL Database")


# class UserService:

#     def __init__(self):
#         self.db=MYSQLDataabase()  # Direct dependency on a concrete class

#     def save_user(self,username):
#         self.db.save(username)


# def main():
#     user_service=UserService()
#     user_service.save_user("john_doe")

# if __name__ == "__main__":
#     main()

# Solution: We can introduce an abstraction for the database.



from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MYSQLDatabase(Database):

    def save(self,data):
        print(f"Saving {data} to MySQL Database")


class PostgreSQLDatabase(Database):

    def save(self,data):
        print(f"Saving {data} to PostgreSQL Database")


class UserService:

    def __init__(self,db:Database):
        self.db=db  # Depend on abstraction

    def save_user(self,username):
        self.db.save(username)


def main():
    user_service=UserService(MYSQLDatabase())
    user_service.save_user("john_doe")

    user_service_pg=UserService(PostgreSQLDatabase())
    user_service_pg.save_user("Rahul")

if __name__ == "__main__":
    main()

    