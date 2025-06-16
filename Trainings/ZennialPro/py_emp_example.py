class Employee:
    company = "ZennialPro"       # Class variable shared by all instances
    all_employees = []           # Stores all employee instances

    def __init__(self, name, hourly_rate):  # Constructor
        self.name = name                   # Instance variable
        self._hourly_rate = hourly_rate   # Private-style hourly rate
        self.hours_worked = 0             # Work tracker
        Employee.all_employees.append(self)

    def __str__(self):  # For print()
        return f"Employee: {self.name}"

    def __repr__(self):  # For debug and dev logs
        return f"Employee(name='{self.name}', rate={self._hourly_rate})"

    def __len__(self):  # Custom length logic
        return self.hours_worked

    def __getitem__(self, key):  # Dictionary-like access
        return getattr(self, key, None)

    def __setitem__(self, key, value):  # Dictionary-like assignment
        setattr(self, key, value)

    def __eq__(self, other):  # Equality check
        return isinstance(other, Employee) and self.name == other.name

    def __call__(self):  # Make instance callable
        print(f"{self.name} works at {self.company}!")

    def __del__(self):  # Destructor
        print(f"Deleted employee: {self.name}")

    def log_hours(self, hours):  # Regular method
        self.hours_worked += hours

    # Lambda to return uppercase name
    get_uppercase = lambda self: self.name.upper()

    # Property to calculate salary
    @property
    def salary(self):
        return self.hours_worked * self._hourly_rate

    # Setter to safely update rate
    @salary.setter
    def salary(self, new_rate):
        if new_rate > 0:
            self._hourly_rate = new_rate

    # Class method for company info
    @classmethod
    def total_employees(cls):
        return len(cls.all_employees)

    # Static method for validation
    @staticmethod
    def is_valid_name(name):
        return isinstance(name, str) and len(name.strip()) > 2

    # Alternate constructor
    @classmethod
    def from_string(cls, data_str):  # "name:rate"
        name, rate = data_str.split(":")
        return cls(name.strip(), float(rate))



# Create employees using regular and alternate constructors
e1 = Employee("Ameet", 1000)
e2 = Employee.from_string("Sheea : 1200")



# Log hours
e1.log_hours(5)
e2.log_hours(8)

# Access using property
print(e1.salary)         # 5000

# Update hourly rate
e1.salary = 1100
print(e1.salary)         # 5500

# Property-like access with __getitem__
print(e1["name"])        # Ameet

# Lambda
print(e2.get_uppercase())  # SHEEA

# Class and static method
print(Employee.total_employees())        # 2
print(Employee.is_valid_name("A!"))      # False

# __call__
e1()  # Calls __call__

# __eq__ check
print(e1 == Employee("Ameet", 900))      # True

# Highest paid
highest = max(Employee.all_employees, key=lambda e: e.salary)
print(f"Highest Paid: {highest.name}, ₹{highest.salary}")

# __len__
print(len(e2))  # 8 (hours worked)

# __repr__ and __str__
print(repr(e1))  # Developer output
print(e1)        # User-friendly output

# Cleanup (triggers __del__)
del e2
