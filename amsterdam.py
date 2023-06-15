"""Creates a schedule for Amsterdam smoke shop"""
import tkinter as tk
import os
from PIL import ImageGrab
import datetime


class Employee:
    """class that stores employee name, availibility, and hours working this week"""

    def __init__(self, name: str, avail: list[int], hours: int):
        self.name = name
        self.avail = avail
        self.hours = hours

    def __str__(self) -> str:
        return f"{self.name}, {self.hours}"


def create_schedule(employees: list[Employee]):
    """creates a list of arrays of workers"""
    shifts = [[] for i in range(14)]
    for shift in range(14):
        employees.sort(
            key=lambda x: x.hours
        )  # sorts employees by amount of hours, to give people with less hours priority
        for employee in employees:
            if employee.avail[shift] == 1:
                break
        else:
            continue
        assigned = False
        if shift % 2 == 0:  # even shift, day time, 1 employee
            for employee in employees:
                if (
                    employee.avail[shift] == 1
                    and employee.hours < 40
                    and len(shifts[shift]) < 1
                ):
                    employee.hours += 7 if shift in [0, 2, 4, 6, 8, 11, 13] else 8
                    shifts[shift].append(employee.name)
                    assigned = True
                    break
        else:  # odd shift, night time, 2 employees
            max_closers = (
                1 if shift in [3, 5, 7] else 2
            )  # 1 closer for Monday, Tuesday, Wednesday nights
            for employee in employees:
                if (
                    employee.avail[shift] == 1
                    and employee.hours < 40
                    and len(shifts[shift]) < max_closers
                ):
                    employee.hours += 6 if shift in [1, 3, 5, 7, 9] else 8
                    shifts[shift].append(employee.name)
                    assigned = True
        if not assigned:  # if empty shift, because people would go over hours
            for employee in employees:
                if employee.avail[shift] == 1:
                    if shift % 2 == 0:
                        if len(shifts[shift]) < 1:
                            employee.hours += (
                                7 if shift in [0, 2, 4, 6, 8, 11, 13] else 8
                            )
                            shifts[shift].append(employee.name)
                            break
                    else:
                        max_closers = (
                            1 if shift in [3, 5, 7] else 2
                        )  # 1 closer for Monday, Tuesday, Wednesday nights
                        if len(shifts[shift]) < max_closers:
                            employee.hours += 6 if shift in [1, 3, 5, 7, 9] else 8
                            shifts[shift].append(employee.name)
                            break
    return shifts


def create_schedule_grid(schedule):
    """turns schedule array into a GUI"""
    root = tk.Tk()
    # Get next Sunday's date
    today = datetime.date.today()
    sunday = today + datetime.timedelta(days=(6 - today.weekday()) % 7)

    # Generate days list for the next week
    days = []
    for i in range(7):
        date = sunday + datetime.timedelta(days=i)
        days.append(date.strftime("%A\n%m/%d"))

    # Modify the first element to be Sunday
    days[0] = "Sunday\n" + days[0].split("\n")[1]

    # print(days)

    for i in range(4):
        for j in range(7):
            if i == 0:
                day_label = tk.Label(
                    root,
                    text=days[j],
                    font=("Arial", 12),
                    width=10,
                    height=2,
                    borderwidth=1,
                    relief="solid",
                    anchor="center",
                )
                day_label.grid(row=i, column=j)
            elif i == 1:
                if j * 2 == 0 or j * 2 == 2 or j * 2 == 4 or j * 2 == 6 or j * 2 == 8:
                    hour_range = "9am-4pm"
                elif j * 2 == 1 or j * 2 == 3 or j * 2 == 5 or j * 2 == 7 or j * 2 == 9:
                    hour_range = "4pm-10pm"
                elif j * 2 == 10 or j * 2 == 12:
                    hour_range = "9am-5pm"
                elif j * 2 == 11 or j * 2 == 13:
                    hour_range = "5pm-12am"
                cell = tk.Label(
                    root,
                    text=hour_range + "\n" + schedule[j * 2][0],
                    font=("Arial", 12),
                    width=10,
                    height=4,
                    borderwidth=1,
                    relief="solid",
                    anchor="center",
                    justify="center",
                )
                cell.grid(row=i, column=j)
            elif i == 2:
                names = "\n".join(schedule[j * 2 + 1])
                if j in [5, 6]:
                    cell = tk.Label(
                        root,
                        text="3pm-12am\n5pm-12am \n" + names,
                        font=("Arial", 12),
                        width=10,
                        height=4,
                        borderwidth=1,
                        relief="solid",
                        anchor="center",
                        justify="center",
                    )
                else:
                    cell = tk.Label(
                        root,
                        text="4pm-10pm \n" + names,
                        font=("Arial", 12),
                        width=10,
                        height=4,
                        borderwidth=1,
                        relief="solid",
                        anchor="center",
                        justify="center",
                    )

                cell.grid(row=i, column=j)

    # Delay and update the window to ensure it is fully drawn
    root.update()
    root.after(200)
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    width = root.winfo_width()
    height = root.winfo_height()
    screenshot = ImageGrab.grab((x, y, x + width, y + height))

    # Save the screenshot as a PNG file with a name in the format "Mar19-Mar25.png"
    start_date = sunday.strftime("%b%d")
    end_date = (sunday + datetime.timedelta(days=6)).strftime("%b%d")
    file_name = start_date + "-" + end_date + ".png"
    file_path = os.path.join(
        os.path.expanduser("~"), "Pictures", "Schedules", file_name
    )
    screenshot.save(file_path)

    root.mainloop()


#########################################################################################
# To add a new employee create an array of their shifts formatted same as below

patty = [
    1,  # sun day CAN WORK
    1,  # sun night CAN WORK
    1,  # mon day
    1,  # mon night
    0,  # tues day
    0,  # tues night
    1,  # wed day
    1,  # wed night
    1,  # thurs day
    1,  # thurs night CAN WORK
    1,  # fri day CAN WORK
    1,  # fri night
    0,  # sat day CAN WORK
    0,  # sat night CAN WORK
]
matt = [
    0,  # sun day CAN WORK
    0,  # sun night CAN WORK
    1,  # mon day CAN WORK
    1,  # mon night CAN WORK
    0,  # tues day
    0,  # tues night
    1,  # wed day CAN WORK
    1,  # wed night CAN WORK
    1,  # thurs day
    1,  # thurs night
    1,  # fri day CAN WORK
    1,  # fri night CAN WORK
    1,  # sat day CAN WORK
    1,  # sat night CAN WORK
]
leo = [
    0,  # sun day CAN WORK
    0,  # sun night CAN WORK
    1,  # mon day
    1,  # mon night CAN WORK
    0,  # tues day
    0,  # tues night
    1,  # wed day
    1,  # wed night CAN WORK
    1,  # thurs day
    0,  # thurs night
    1,  # fri day CAN WORK
    1,  # fri night CAN WORK
    0,  # sat day CAN WORK
    0,  # sat night CAN WORK
]
brandon = [
    1,  # sun day CAN WORK
    1,  # sun night CAN WORK
    1,  # mon day CAN WORK
    1,  # mon night CAN WORK
    1,  # tues day CAN WORK
    1,  # tues night CAN WORK
    1,  # wed day CAN WORK
    1,  # wed night CAN WORK
    1,  # thurs day CAN WORK
    1,  # thurs night CAN WORK
    1,  # fri day CAN WORK
    1,  # fri night CAN WORK
    1,  # sat day CAN WORK
    1,  # sat night
]
shania = [
    0,  # sun day CAN WORK
    1,  # sun night CAN WORK
    0,  # mon day CAN WORK
    0,  # mon night CAN WORK
    0,  # tues day CAN WORK
    1,  # tues night CAN WORK
    0,  # wed day CAN WORK
    1,  # wed night CAN WORK
    0,  # thurs day CAN WORK
    0,  # thurs night CAN WORK
    0,  # fri day CAN WORK
    1,  # fri night CAN WORK
    0,  # sat day CAN WORK
    1,  # sat night
]
rose = [
    0,  # sun day CAN WORK
    1,  # sun night CAN WORK
    0,  # mon day CAN WORK
    0,  # mon night CAN WORK
    0,  # tues day CAN WORK
    1,  # tues night CAN WORK
    0,  # wed day CAN WORK
    1,  # wed night CAN WORK
    0,  # thurs day CAN WORK
    0,  # thurs night CAN WORK
    0,  # fri day CAN WORK
    1,  # fri night CAN WORK
    0,  # sat day CAN WORK
    1,  # sat night
]

# add all the employees to this 'employees' array IF ADDING NEW EMPLOYEE DONT FORGET TO ADD COMMA
workers = [
    Employee(name="Patty", avail=patty, hours=0),
    Employee(name="Matt", avail=matt, hours=0),
    Employee(name="Leo", avail=leo, hours=0),
    Employee(name="Brandon", avail=brandon, hours=0),
    Employee(name="Shania", avail=shania, hours=0),
    Employee(name="Rose", avail=rose, hours=0),
]


create_schedule_grid(create_schedule(workers))
# print(schedule)

print("Employee hours for the week: ")
for person in workers:
    print(person)
