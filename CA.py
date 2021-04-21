#Assingment by Bruna Marjorie Carvalho Santana, brunamarjorie@gmail.com, (089) 946-6612.

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.messagebox as mb
import datetime as dt
import csv


class BMIApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # List of shared variables:
        self.data = {'fname': StringVar(),
                     'weight_kg': StringVar(),
                     'weight_st': StringVar(),
                     'weight_lb': StringVar(),
                     'height_cm': StringVar(),
                     'height_ft': StringVar(),
                     'height_inch': StringVar(),
                     'bmi': StringVar(),
                     'cat': StringVar(),
                     'kg_ideal1': StringVar(),
                     'kg_ideal2': StringVar(),
                     'st_ideal1': StringVar(),
                     'st_ideal2': StringVar(),
                     'lb_ideal1': StringVar(),
                     'lb_ideal2': StringVar()}

        self.text = Text(font=('Calibri', 12), height=10.3, width=50, pady=2)
        self.fileName = 'records.csv'
        # List to store data
        self.dataList = []
        self.currentIndex = 0

        # Container
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Two different interfaces (Metric or Imperial System):
        for F in (Metric, Imperial):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Default interface:
        self.show_frame("Metric")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def clear(self):
        # Clean all the inputs
        self.data['fname'].set('')
        self.data['weight_kg'].set('')
        self.data['weight_st'].set('')
        self.data['weight_lb'].set('')
        self.data['height_cm'].set('')
        self.data['height_ft'].set('')
        self.data['height_inch'].set('')
        self.data['bmi'].set('')
        self.data['cat'].set('')
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        self.text.forget()

    def BMI(self):
        # Calculate BMI
        kg = float(self.data['weight_kg'].get())
        mt = float(self.data['height_cm'].get()) / 100
        bmi = kg / (mt * mt)
        bmi = round(bmi, 1)

        # BMI Categories
        if bmi < 18.5:
            cat = "underweight"
        elif 18.5 <= bmi < 25:
            cat = "normal weight"
        elif 25 <= bmi < 30:
            cat = "overweight"
        elif bmi >= 30:
            cat = "obese"

        # Ideal weight
        kg_ideal1 = 18.5 * mt * mt
        kg_ideal1 = round(kg_ideal1, 1)
        st_ideal1 = int(kg_ideal1 / 6.35029318)
        lb_ideal1 = (((kg_ideal1 / 6.35029318) - st_ideal1) * 14)
        lb_ideal1 = round(lb_ideal1, 1)

        kg_ideal2 = 24.9 * mt * mt
        kg_ideal2 = round(kg_ideal2, 1)
        st_ideal2 = int(kg_ideal2 / 6.35029318)
        lb_ideal2 = (((kg_ideal2 / 6.35029318) - st_ideal2) * 14)
        lb_ideal2 = round(lb_ideal2, 1)



        # Set the values to the variables
        return self.data['bmi'].set(bmi), self.data['cat'].set(cat), self.data['kg_ideal1'].set(kg_ideal1), self.data['kg_ideal2'].set(kg_ideal2), self.data['st_ideal1'].set(st_ideal1), self.data['st_ideal2'].set(st_ideal2), self.data['lb_ideal1'].set(lb_ideal1), self.data['lb_ideal2'].set(lb_ideal2)

    def calculateMetric(self):
        # Clean any text output
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        self.text.forget()

        # Get numbers from the text entry fields
        name = self.data['fname'].get()
        kg = self.data['weight_kg'].get()
        mt = self.data['height_cm'].get()

        # Validate entries
        if kg == '' or mt == '' or name == '':
            mb.showerror('Error', 'Please fill Name, Height and Weight fields.')
        else:
            try:
                kg = float(kg)
                mt = float(mt) / 100

            except ValueError:
                mb.showerror('Error', 'Please enter a valid number.')

            else:
                if mt <= 0 or mt > 3:
                    mb.showerror('Error', 'Enter a valid height.')

                elif kg <= 1.5 or kg > 300:
                    mb.showerror('Error', 'Enter a valid weight.')

                else:
                    st = int(kg / 6.35029318)
                    self.data['weight_st'].set(st)
                    lb = float(((kg / 6.35029318) - st) * 14)
                    lb = round(lb, 1)
                    self.data['weight_lb'].set(lb)
                    ft = int((mt / 0.3048))
                    self.data['height_ft'].set(ft)
                    inch = float(((mt / 0.3048) - ft) * 12)
                    inch = round(inch, 2)
                    self.data['height_inch'].set(inch)
                    bmi = self.BMI()
                    print = self.print()

    def calculateImperial(self):
        # Clean any text output
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        self.text.forget()

        # Get numbers from the text entry fields
        name = self.data['fname'].get()
        stone = self.data['weight_st'].get()
        pounds = self.data['weight_lb'].get()
        feet = self.data['height_ft'].get()
        inch = self.data['height_inch'].get()

        # Validate entries
        if stone == '' or pounds == '' or name == '' or feet == '' or inch == '':
            mb.showerror('Error', 'Please fill Name, Height and Weight fields.')
        else:
            try:
                stone = float(stone)
                pounds = float(pounds)
                feet = float(feet)
                inch = float(inch)

            except ValueError:
                mb.showerror('Error', 'Please enter a valid number.')

            else:
                kg = float((stone + (pounds / 14)) * 6.35029318)
                kg = round(kg, 1)
                self.data['weight_kg'].set(kg)
                mt = float((feet + (inch / 12)) * 0.3048)

                if mt <= 0 or mt > 3:
                    mb.showerror('Error', 'Enter a valid height.')

                elif kg <= 1 or kg > 300:
                    mb.showerror('Error', 'Enter a valid weight.')

                else:
                    cm = mt * 100
                    cm = round(cm, 0)
                    self.data['height_cm'].set(cm)

                    bmi = self.BMI()
                    print = self.print()

    def print(self):
        # Print text output
        mt = float((self.data['height_cm'].get())) / 100
        mt = str(mt)

        self.text.insert(INSERT, ("Hello, " + self.data['fname'].get() + '.\n'))
        self.text.insert(INSERT, ('-----------------------------------------------------------------------------\n'))
        self.text.insert(INSERT, ("Your height is " + mt + 'm or ' + self.data['height_ft'].get() + ' feet and ' +
                                  self.data['height_inch'].get() + ' inches.\n'))
        self.text.insert(INSERT, ("Your weight is " + self.data['weight_kg'].get() + 'kg or ' +
                                  self.data['weight_st'].get() + ' stones and ' + self.data['weight_lb'].get() +
                                  ' pounds.\n'))
        self.text.insert(INSERT, ('-----------------------------------------------------------------------------\n'))
        self.text.insert(INSERT, ("Your BMI is " + self.data['bmi'].get() + ' (' + self.data['cat'].get() + ').\n'))
        self.text.insert(INSERT, ("Your ideal weight is between " + self.data['kg_ideal1'].get() + ' and ' + self.data['kg_ideal2'].get() + 'kg,\n'))
        self.text.insert(INSERT, ("or between " + self.data['st_ideal1'].get() + 'st ' + self.data['lb_ideal1'].get() + 'lb and '+ self.data['st_ideal2'].get() + 'st ' + self.data['lb_ideal2'].get() + 'lb\n'))
        self.text.insert(INSERT, ('-----------------------------------------------------------------------------\n'))
        self.text.insert(END, "Thank you for using the app.")
        self.text.config(state=DISABLED)
        self.text.pack()

    def save(self):
        # Check if there is value to be saved
        if self.data['fname'].get() == '' or self.data['weight_kg'].get() == '' or self.data['height_cm'].get() == '':
            mb.showwarning('Warning', 'Nothing to save')

        else:
            time = f"{dt.datetime.now():%d/%m/%y %H:%M}"
            # Create record
            record = (self.data['fname'].get(), self.data['weight_kg'].get(), self.data['weight_st'].get(),
                      self.data['weight_lb'].get(), self.data['height_cm'].get(),
                      self.data['height_ft'].get(), self.data['height_inch'].get(), time)

            self.dataList.append(record)  # adds record to the list
            self.currentIndex = len(self.dataList) - 1
            mb.showinfo("Record Added", "Record Added")
            self.clear()

            # Save file
            csvfile = open(file=self.fileName, mode='a', newline='\n')
            writer = csv.writer(csvfile, delimiter=",")

            for lcv in range(0, len(self.dataList)):
                writer.writerow(self.dataList[lcv])

            csvfile.close()

    def read(self):

        self.dataList.clear()

        csvfile = open('records.csv', 'r')
        reader = csv.reader(csvfile, delimiter=',')

        for line in reader:
            print(tuple(line))
            self.dataList.append(line)

        csvfile.close()
        self.currentIndex = 0

class Metric(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.controller = controller

        # Display the grid of components
        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky='e')
        ttk.Entry(self, width=10, textvariable=self.controller.data['fname']).grid(row=0, column=1, padx=2, pady=2,
                                                                                   sticky='we', columnspan=4)

        ttk.Label(self, text="Height:").grid(row=1, column=0, sticky='e')
        ttk.Entry(self, width=14, textvariable=self.controller.data['height_cm']).grid(row=1, column=1, padx=2, pady=2,
                                                                                       sticky='we')
        ttk.Label(self, text="(centimeters)").grid(row=1, column=2, sticky='w')
        ttk.Label(self, text="").grid(row=1, column=3, sticky='w')
        ttk.Label(self, text="").grid(row=1, column=4, sticky='w')

        ttk.Label(self, text="Weight:").grid(row=2, column=0, sticky='e')
        ttk.Entry(self, width=14, textvariable=self.controller.data['weight_kg']).grid(row=2, column=1, padx=2, pady=2,
                                                                                       sticky='we')
        ttk.Label(self, text="(kilograms)").grid(row=2, column=2, sticky='w')
        ttk.Label(self, text="          ").grid(row=2, column=3, sticky='w')
        ttk.Label(self, text="          ").grid(row=2, column=4, sticky='w')

        # Buttons
        ttk.Button(self, text="Switch to Imperial", command=lambda: controller.show_frame("Imperial")).grid(
            column=5, row=0, sticky='e')
        ttk.Button(self, text="Calculate", command=lambda: controller.calculateMetric()).grid(column=5,
                                                                                              row=1, sticky='we')
        ttk.Button(self, text="Clear", command=lambda: controller.clear()).grid(column=5,
                                                                                row=2, sticky='we')
        ttk.Button(self, text="Save", width=20, command=lambda: controller.save()).grid(column=0,
                                                                                        row=3, columnspan=2,
                                                                                        sticky='we', pady=5)
        ttk.Button(self, text="Read", width=20, command=lambda: controller.read()).grid(column=2,
                                                                                        row=3, columnspan=3,
                                                                                        sticky='we', pady=5)
        ttk.Button(self, text="Exit", command=lambda: self.quit()).grid(column=5,
                                                                        row=3, sticky='we', pady=5)

class Imperial(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.controller = controller

        # Display the grid of components
        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky='e')
        ttk.Entry(self, width=10, textvariable=self.controller.data['fname']).grid(row=0, column=1, padx=2, pady=2,
                                                                                   sticky='we', columnspan=4)

        ttk.Label(self, text="Height:").grid(row=1, column=0, sticky='e')
        ttk.Entry(self, width=10, textvariable=self.controller.data['height_ft']).grid(row=1, column=1, padx=2, pady=2,
                                                                                       sticky='we')
        ttk.Label(self, text="(feet)").grid(row=1, column=2, sticky='w')
        ttk.Entry(self, width=10, textvariable=self.controller.data['height_inch']).grid(row=1, column=3, padx=2,
                                                                                         pady=2,
                                                                                         sticky='we')
        ttk.Label(self, text="(inches)").grid(row=1, column=4, sticky='w')

        ttk.Label(self, text="Weight:").grid(row=2, column=0, sticky='e')
        ttk.Entry(self, width=10, textvariable=self.controller.data['weight_st']).grid(row=2, column=1, padx=2, pady=2,
                                                                                       sticky='we')
        ttk.Label(self, text="(stones)").grid(row=2, column=2, sticky='w')
        ttk.Entry(self, width=10, textvariable=self.controller.data['weight_lb']).grid(row=2, column=3, padx=2, pady=2,
                                                                                       sticky='we')
        ttk.Label(self, text="(pounds)").grid(row=2, column=4, sticky='w')

        # Buttons
        ttk.Button(self, text=" Switch to Metric ", command=lambda: controller.show_frame("Metric")).grid(
            column=5, row=0, sticky='e')
        ttk.Button(self, text="Calculate", command=lambda: controller.calculateImperial()).grid(column=5,
                                                                                                row=1, sticky='we')
        ttk.Button(self, text="Clear", command=lambda: controller.clear()).grid(column=5,
                                                                                row=2, sticky='we')
        ttk.Button(self, text="Save", width=20, command=lambda: controller.save()).grid(column=0,
                                                                              row=3, columnspan=2, sticky='we', pady=5)
        ttk.Button(self, text="Read", width=20, command=lambda: controller.read()).grid(column=2,
                                                                                   row=3, columnspan=3, sticky='we', pady=5)
        ttk.Button(self, text="Exit", command=lambda: self.quit()).grid(column=5,
                                                                              row=3, sticky='we', pady=5)

if __name__ == "__main__":
    app = BMIApp()
    app.title("BMI Calculator")
    app.wm_iconbitmap('bmi.ico')
    app.mainloop()
