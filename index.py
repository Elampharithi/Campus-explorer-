"""
Advanced Smart Campus Record Explorer
-------------------------------------
Records are stored as a list of lists (nested lists):
    [student_id, name, department, year, cgpa, email]
Features: add, update, display, filter, text processing,
linear search, binary search, bubble sort, selection sort.
"""

# Column indexes
ID, NAME, DEPT, YEAR, CGPA, EMAIL = range(6)
HEADERS = ["ID", "Name", "Department", "Year", "CGPA", "Email"]

records = [
    [103, "Riya Sharma", "CSE", 2, 8.7, "riya.sharma@campus.edu"],
    [101, "Aman Verma", "ECE", 3, 7.9, "aman.verma@campus.edu"],
    [105, "Neha Singh", "CSE", 1, 9.2, "neha.singh@campus.edu"],
    [102, "Karan Mehta", "MECH", 4, 6.8, "karan.mehta@campus.edu"],
    [104, "Priya Nair", "ECE", 2, 8.1, "priya.nair@campus.edu"],
]


# ---------------- Text processing ----------------
def clean_name(name):
    """Trim extra spaces and convert to Title Case."""
    return " ".join(name.split()).title()


def make_email(name):
    """Generate email like first.last@campus.edu from a name."""
    return ".".join(name.lower().split()) + "@campus.edu"


def initials(name):
    return "".join(w[0].upper() for w in name.split())


# ---------------- Display ----------------
def display(data=None):
    data = records if data is None else data
    if not data:
        print("No records found.")
        return
    print("-" * 82)
    print(f"{HEADERS[0]:<6}{HEADERS[1]:<20}{HEADERS[2]:<12}{HEADERS[3]:<6}"
          f"{HEADERS[4]:<7}{HEADERS[5]}")
    print("-" * 82)
    for r in data:
        print(f"{r[ID]:<6}{r[NAME]:<20}{r[DEPT]:<12}{r[YEAR]:<6}"
              f"{r[CGPA]:<7}{r[EMAIL]}")
    print("-" * 82)


# ---------------- Add / Update ----------------
def add_record(sid, name, dept, year, cgpa):
    if any(r[ID] == sid for r in records):
        print("Error: ID already exists.")
        return False
    name = clean_name(name)
    records.append([sid, name, dept.upper().strip(), year, cgpa, make_email(name)])
    print(f"Added {name}.")
    return True


def update_record(sid, field, value):
    """field: 'name', 'dept', 'year' or 'cgpa'."""
    for r in records:
        if r[ID] == sid:
            if field == "name":
                r[NAME] = clean_name(value)
                r[EMAIL] = make_email(r[NAME])
            elif field == "dept":
                r[DEPT] = value.upper().strip()
            elif field == "year":
                r[YEAR] = int(value)
            elif field == "cgpa":
                r[CGPA] = float(value)
            else:
                print("Unknown field.")
                return False
            print("Record updated.")
            return True
    print("ID not found.")
    return False


# ---------------- Filters ----------------
def filter_by_dept(dept):
    return [r for r in records if r[DEPT] == dept.upper()]


def filter_by_cgpa(min_cgpa):
    return [r for r in records if r[CGPA] >= min_cgpa]


def filter_by_name_text(text):
    """Case-insensitive substring match on name."""
    return [r for r in records if text.lower() in r[NAME].lower()]


# ---------------- Searching ----------------
def linear_search(data, key, col):
    """Works on unsorted data. Returns index or -1."""
    for i in range(len(data)):
        if str(data[i][col]).lower() == str(key).lower():
            return i
    return -1


def binary_search(data, key, col=ID):
    """Requires data sorted by `col` (ascending). Returns index or -1."""
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][col] == key:
            return mid
        elif data[mid][col] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# ---------------- Sorting (on copies) ----------------
def bubble_sort(data, col, reverse=False):
    arr = [r[:] for r in data]
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            a, b = arr[j][col], arr[j + 1][col]
            if (a < b) if reverse else (a > b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(data, col, reverse=False):
    arr = [r[:] for r in data]
    n = len(arr)
    for i in range(n - 1):
        best = i
        for j in range(i + 1, n):
            if (arr[j][col] > arr[best][col]) if reverse else (arr[j][col] < arr[best][col]):
                best = j
        arr[i], arr[best] = arr[best], arr[i]
    return arr


# ---------------- Demo ----------------
def demo():
    print("\n=== Original records ===")
    display()

    print("\n=== Add + Update ===")
    add_record(106, "  rohit   kumar ", "cse", 3, 7.5)
    update_record(101, "cgpa", "8.3")
    display()

    print("\n=== Text processing ===")
    print("Clean name   :", clean_name("  aRYa    deSAI "))
    print("Generated mail:", make_email("Aarav Patel"))
    print("Initials     :", initials("Riya Sharma"))
    print("Name contains 'an':")
    display(filter_by_name_text("an"))

    print("\n=== Filters ===")
    print("CSE students:")
    display(filter_by_dept("cse"))
    print("CGPA >= 8.0:")
    display(filter_by_cgpa(8.0))

    print("\n=== Linear search (by name, unsorted) ===")
    i = linear_search(records, "Neha Singh", NAME)
    print("Found at index", i, "->", records[i] if i != -1 else "Not found")

    print("\n=== Bubble sort by CGPA (descending) ===")
    display(bubble_sort(records, CGPA, reverse=True))

    print("\n=== Selection sort by Name (ascending) ===")
    display(selection_sort(records, NAME))

    print("\n=== Binary search (by ID, after sorting by ID) ===")
    by_id = selection_sort(records, ID)
    idx = binary_search(by_id, 104, ID)
    print("ID 104 ->", by_id[idx] if idx != -1 else "Not found")
    print("ID 999 ->", "Not found" if binary_search(by_id, 999, ID) == -1 else "Found")


# ---------------- Menu ----------------
def menu():
    options = """
===== Smart Campus Record Explorer =====
1. Display all      2. Add record      3. Update record
4. Filter by dept   5. Filter by min CGPA   6. Search name text
7. Linear search (name)   8. Binary search (ID)
9. Bubble sort by CGPA    10. Selection sort by Name
11. Run demo        0. Exit"""
    while True:
        print(options)
        ch = input("Choice: ").strip()
        try:
            if ch == "1":
                display()
            elif ch == "2":
                add_record(int(input("ID: ")), input("Name: "), input("Dept: "),
                           int(input("Year: ")), float(input("CGPA: ")))
            elif ch == "3":
                update_record(int(input("ID: ")),
                              input("Field (name/dept/year/cgpa): ").lower(),
                              input("New value: "))
            elif ch == "4":
                display(filter_by_dept(input("Dept: ")))
            elif ch == "5":
                display(filter_by_cgpa(float(input("Min CGPA: "))))
            elif ch == "6":
                display(filter_by_name_text(input("Text: ")))
            elif ch == "7":
                i = linear_search(records, input("Name: "), NAME)
                display([records[i]] if i != -1 else [])
            elif ch == "8":
                s = selection_sort(records, ID)
                i = binary_search(s, int(input("ID: ")), ID)
                display([s[i]] if i != -1 else [])
            elif ch == "9":
                display(bubble_sort(records, CGPA, reverse=True))
            elif ch == "10":
                display(selection_sort(records, NAME))
            elif ch == "11":
                demo()
            elif ch == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter correct data types.")


if __name__ == "__main__":
    menu()
