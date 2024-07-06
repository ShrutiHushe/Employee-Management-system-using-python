from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from requests import get
import requests
from sqlite3 import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

mw = Tk()
mw.configure(bg="lavender")
mw.title("EMS by Shruti")
mw.geometry("1300x900+50+50")
mw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

def f1():
    mw.withdraw()
    aw.deiconify()

def f2():
    mw.withdraw()
    vw.deiconify()
    vwdata.delete(1.0, END)
    con = None
    try:
        con = connect("Task4.db")
        cursor = con.cursor()
        sql = "select * from employees"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            info = f"Id {d[0]} Name {d[1]} Salary {d[2]}\n"
            vwdata.insert(INSERT, info)
    except Exception as e:
        showerror("issue ", e)
    finally:
        if con is not None:
            con.close()

def f3():
    mw.withdraw()
    uw.deiconify()

def f4():
    mw.withdraw()
    dw.deiconify()

def f5():
    mw.withdraw()
    cw.deiconify()

def f6():
    aw.withdraw()
    mw.deiconify()

def f7():
    vw.withdraw()
    mw.deiconify()

def f8():
    uw.withdraw()
    mw.deiconify()

def f9():
    dw.withdraw()
    mw.deiconify()

def save():
    try:
        id = entId.get().strip()
        name = entName.get().strip()
        salary = entSalary.get().strip()

        if not id or not id.isdigit():
            showerror("Issues", "Please enter a valid Id")
            return False

        if not name or not name.isalpha():
            showerror("Issues", "Please enter a valid name")
            return False

        if not salary or not salary.replace('.', '').isdigit():
            showerror("Issues", "Please enter a valid salary")
            return False

        con = None
        try:
            con = connect("Task4.db")
            cursor = con.cursor()
            sql = "insert into employees values(?, ?, ?)"
            cursor.execute(sql, (id, name, salary))
            con.commit()
            showinfo("Success", "Record created")
            entId.delete(0, END)
            entName.delete(0, END)
            entSalary.delete(0, END)
            entId.focus()
        except Exception as e:
            con.rollback()
            showerror("Issue", e)
        finally:
            if con is not None:
                con.close()

    except Exception as e:
        showerror("Issues", e)

def update():
    try:
        id = uwentId.get().strip()

        con = None
        try:
            con = connect("Task4.db")
            cursor = con.cursor()

            check_sql = "SELECT * FROM employees WHERE id = ?"
            cursor.execute(check_sql, (id,))
            existing_record = cursor.fetchone()

            if not existing_record:
                showerror("Issue", f"Record with ID {id} not found")
                return False

            name = uwentName.get().strip()
            salary = uwentSalary.get().strip()

            if not name or not name.isalpha():
                showerror("Issues", "Please enter a valid name")
                return False

            if not salary or not salary.replace('.', '').isdigit():
                showerror("Issues", "Please enter a valid salary")
                return False

            update_sql = "UPDATE employees SET name=?, salary=? WHERE id=?"
            cursor.execute(update_sql, (name, salary, id))
            con.commit()
            showinfo("Success", "Record updated")
            uwentId.delete(0, END)
            uwentName.delete(0, END)
            uwentSalary.delete(0, END)
            uwentId.focus()

        except Exception as e:
            con.rollback()
            showerror("Issue", e)

        finally:
            if con is not None:
                con.close()

    except Exception as e:
        showerror("Issues", e)


def delete():
    try:
        id = dwentId.get().strip()

        con = None
        try:
            con = connect("Task4.db")
            cursor = con.cursor()

            check_sql = "SELECT * FROM employees WHERE id = ?"
            cursor.execute(check_sql, (id,))
            existing_record = cursor.fetchone()

            if not existing_record:
                showerror("Issue", f"Record with ID {id} not found")
                return False

            delete_sql = "DELETE FROM employees WHERE id = ?"
            cursor.execute(delete_sql, (id,))
            con.commit()
            showinfo("Success", "Record Deleted")
            dwentId.delete(0, END)
            dwentId.focus()

        except Exception as e:
            con.rollback()
            showerror("Issue", e)

        finally:
            if con is not None:
                con.close()

    except Exception as e:
        showerror("Issues", e)

def plot_chart():
    con = None
    try:
        con = connect("Task4.db")
        cursor = con.cursor()
        sql = "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5"
        cursor.execute(sql)
        data = cursor.fetchall()

        names = [entry[0] for entry in data]
        salaries = [entry[1] for entry in data]

        fig, ax = plt.subplots()
        ax.bar(names, salaries)
        ax.set_xlabel('Employee Names')
        ax.set_ylabel('Salaries')
        ax.set_title('Top 5 Employees with Highest Salaries')

        chart_window = Toplevel()
        chart_window.title("Bar Chart")
        chart_window.geometry("800x600+100+100")
        chart_window.iconbitmap("employee.ico")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, chart_window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        chart_window.protocol("WM_DELETE_WINDOW", chart_window.destroy)

    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()

btnAdd = Button(mw, font=f, text="Add", command=f1)
btnAdd.pack(pady=10)
btnView = Button(mw, font=f, text="View", command=f2)
btnView.pack(pady=10)
btnUpdate = Button(mw, font=f, text="Update", command=f3)
btnUpdate.pack(pady=10)
btnDelete = Button(mw, font=f, text="Delete", command=f4)
btnDelete.pack(pady=10)
btnCharts = Button(mw, font=f, text="Charts", command=plot_chart)
btnCharts.pack(pady=10)



def get_city_name():
    try:
        location_url = "https://ipinfo.io/"
        location_res = requests.get(location_url)

        if location_res.status_code == 200:
            location_data = location_res.json()
            city = location_data["city"]
            return city
        else:
            return "Unknown"
    except Exception as e:
        return str(e)

def get_weather(api_key, city):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        weather_res = requests.get(weather_url)

        if weather_res.status_code == 200:
            weather_data = weather_res.json()
            temperature_kelvin = weather_data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            return round(temperature_celsius, 2)
        else:
            return "Can't connect"
    except Exception as e:
        return str(e)

# Use your OpenWeatherMap API key
openweathermap_api_key = "09d14feef82d14c6eccf03fa97dcce07"

try:
    city = get_city_name()
    temperature = get_weather(openweathermap_api_key, city)

    label_location = Label(mw, text=f"Location: {city}", font=f, bg="lavender")
    label_location.pack(pady=10)

    if isinstance(temperature, float):
        label_temperature = Label(mw, text=f"Temperature: {temperature} °C", font=f, bg="lavender")
        label_temperature.pack(pady=10)
    else:
        label_temperature = Label(mw, text=temperature, font=f, bg="lavender")
        label_temperature.pack(pady=10)

except Exception as e:
    print("Issues: ", e)

aw = Toplevel()
aw.title("Add Emp")
aw.geometry("1300x900+50+50")
aw.configure(bg="lavender")
aw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

labId = Label(aw, font=f, text="Enter id")
labId.pack(pady=10)
entId = Entry(aw, font=f)
entId.pack(pady=10)
labName = Label(aw, font=f, text="Enter name")
labName.pack(pady=10)
entName = Entry(aw, font=f)
entName.pack(pady=10)
labSalary = Label(aw, font=f, text="Enter salary")
labSalary.pack(pady=10)
entSalary = Entry(aw, font=f)
entSalary.pack(pady=10)
btnSave = Button(aw, font=f, text="Save", command=save)
btnSave.pack(pady=10)
btnBack = Button(aw, font=f, text="Back", command=f6)
btnBack.pack(pady=10)

aw.withdraw()

vw = Toplevel()
vw.title("View Emp")
vw.geometry("1300x900+50+50")
vw.configure(bg="lavender")
vw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

vwdata = ScrolledText(vw, font=f, width=30, height=10)
vwbtnback = Button(vw, text="Back", font=f, command=f7)
vwdata.pack(pady=10)
vwbtnback.pack(pady=10)

vw.withdraw()

uw = Toplevel()
uw.title("Update Emp")
uw.geometry("1300x900+50+50")
uw.configure(bg="lavender")
uw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

uwlabId = Label(uw, font=f, text="Enter id")
uwlabId.pack(pady=10)
uwentId = Entry(uw, font=f)
uwentId.pack(pady=10)
uwlabName = Label(uw, font=f, text="Enter name")
uwlabName.pack(pady=10)
uwentName = Entry(uw, font=f)
uwentName.pack(pady=10)
uwlabSalary = Label(uw, font=f, text="Enter salary")
uwlabSalary.pack(pady=10)
uwentSalary = Entry(uw, font=f)
uwentSalary.pack(pady=10)
uwbtnSave = Button(uw, font=f, text="Update", command=update)
uwbtnSave.pack(pady=10)
uwbtnBack = Button(uw, font=f, text="Back", command=f8)
uwbtnBack.pack(pady=10)

uw.withdraw()

dw = Toplevel()
dw.title("Delete Emp")
dw.geometry("1300x900+50+50")
dw.configure(bg="lavender")
dw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

dwlabId = Label(dw, font=f, text="Enter id to be deleted")
dwlabId.pack(pady=10)
dwentId = Entry(dw, font=f)
dwentId.pack(pady=10)
dwbtnSave = Button(dw, font=f, text="Delete", command=delete)
dwbtnSave.pack(pady=10)
dwbtnBack = Button(dw, font=f, text="Back", command=f9)
dwbtnBack.pack(pady=10)

dw.withdraw()

cw = Toplevel()
cw.title("Chart")
cw.geometry("1300x900+50+50")
cw.configure(bg="lavender")
cw.iconbitmap("employee.ico")
f = ("Arial", 20, "bold")

cw.withdraw()

def on_closing():
    if askyesno("Quit", "Do u really want to Quit ?"):
        mw.destroy()

mw.protocol("WM_DELETE_WINDOW", on_closing)
mw.mainloop()
