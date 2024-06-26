import pyodbc
from typing import Union
from pydantic import BaseModel


class Employee(BaseModel):
    first_name: str
    last_name: Union[str, None] = None
    job: str


connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:mysy.database.windows.net,1433;Database=mydb;Uid=shazeb;Pwd=Google321;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


def root():
    print("Lets Perform CURD Operations")
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE Employee (
                ID int NOT NULL PRIMARY KEY IDENTITY,
                FirstName varchar(255),
                LastName varchar(255),
                Job varchar(255)
            );
        """)
        conn.commit()
        while 1:
            print("\nEmployee Management System")
            print("1. Create Employee")
            print("2. Read Employees")
            print("3. Read Employee by ID")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                create_employee()
            elif choice == '2':
                get_employees()
            elif choice == '3':
                get_employee_id()
            elif choice == '4':
                update_employee()
            elif choice == '5':
                delete_employee()
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(e)
    return "Employee API"


def get_employees():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employee")
        print("ID", "FirstName", "LastName", "Job")
        for row in cursor.fetchall():
            print(row.ID,row.FirstName, row.LastName,row.Job)
            rows.append(f"{row.ID}, {row.FirstName}, {row.LastName}, {row.Job}")
    return rows


def get_employee_id():
    employee_id = int(input("Enter the id : "))
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employee WHERE ID = ?", employee_id)
            row = cursor.fetchone()
            if row is not None:
                print(f"{row.ID}, {row.FirstName}, {row.LastName}, {row.Job}")
            else:
                print(f"No Employee With id:{employee_id}")
    except Exception as e:
        print(f"Error:{e}")


def delete_employee():
    employee_id = int(input("Enter the id : "))
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            delete_query = """
            DELETE FROM Employee
            WHERE id = ?
            """
            cursor.execute(delete_query, (employee_id,))
            conn.commit()
            print("Employee deleted successfully.")
    except Exception as e:
        print(f"No Employee With id:{employee_id}",e)
    finally:
        conn.close()


def update_employee():
    try:
        employee_id = int(input("Enter the id : "))
        job = input("Enter the Job Field value : ")
        update_query = """
                UPDATE Employee
                SET job = ?
                WHERE id = ?
                """
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(update_query, (job, employee_id))
            conn.commit()
            print("Employee updated successfully.")
    except Exception as e:
        print(f"Error:{e}")
    finally:
        conn.close()


def create_employee():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name (optional): ")
    job = input("Enter job title: ")
    item = Employee(first_name=first_name, last_name=last_name or None, job=job)
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Employee (FirstName, LastName,Job) VALUES (?, ?, ?)", item.first_name,
                       item.last_name, item.job)
        conn.commit()
    return item


def get_conn():
    conn = pyodbc.connect(connection_string)
    return conn


app = root()