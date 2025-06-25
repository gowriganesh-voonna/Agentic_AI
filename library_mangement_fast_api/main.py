from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
from app.service.library_service import (
    add_book,
    update_book,
    delete_book,
    view_all_books,
    search_book,
    generate_report
)

from app.service.student_service import (
    add_student,
    view_all_students,
    update_student,
    search_student,
    remove_student
)
from app.service.book_issue_service import (
    issue_book,
    return_book,
    view_issued_books
)

from fastapi import FastAPI
#from app.service.library_service import router
from app.service.student_service import router
from app.utiles.logger import get_logger


logger = get_logger(__name__)

app = FastAPI (title = "Library Mangement API", version="1.0.0")

app.include_router(router,prefix="/api", tags=["LibraryMangement"])


# def quit_program():
#     print("Exiting the program. Goodbye!")
#     exit()


# def main():
       
#         while True:
#             print("--------------------Library CLI --------------------")
#             print("1.Add Book")
#             print("2.Update Book")
#             print("3.Delete Book")
#             print("4.View all books")
#             print("5.Search Book")
#             print("6.Generate Report")
#             print("7.Add Student")
#             print("8.Upate student")
#             print("9. View all students")
#             print("10.Search Student")
#             print("11.Remove Student")
#             print("12. Issue Book")
#             print("13. Return Book")
#             print("14. View Issued Book")
#             print("0.Exit program")
        
#             choice = int(input("Enter Choice"))

#             if choice == 1:
#                 add_book()
            
#             elif choice == 2:
#                 update_book()

#             elif choice ==3:
#                 delete_book()
            
#             elif choice == 4:
#                 view_all_books()
#             elif choice ==5:
#                 search_book()
#             elif choice == 6:
#                 generate_report()

#             elif choice == 7:
#                 add_student()
#             elif choice == 8:
#                 update_student()
#             elif choice ==9:
#                 view_all_students()
#             elif choice == 10:
#                 search_student()
#             elif choice == 11 :
#                 remove_student()
#             elif choice == 12:
#                 issue_book()
#             elif choice == 13:
#                 return_book()
#             elif choice == 14:
#                 view_issued_books()
#             elif choice == 0:
#                 quit_program()
            

# if __name__ == "__main__":
#     main()
