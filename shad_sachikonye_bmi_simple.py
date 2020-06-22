from tkinter import *
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox as mb

"""A BMI APP GUI BY SHADRACK SACHIKONYE, EMAIL: shadreck.sachikonye@gmail.com, Phone: +447951577999"""


class BMIFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.pack()

        self.dt = datetime.datetime.now()
        self.vld = self.register(self.only_numeric_input)

        # defining string variables
        self.name = tk.StringVar()
        self.bmi_weight = tk.StringVar()
        self.bmi_height = tk.StringVar()
        self.bmi = tk.StringVar()
        self.imp_lbs = tk.StringVar()
        self.imp_feet = tk.StringVar()
        self.imp_inches = tk.StringVar()
        self.imp_stones = tk.StringVar()
        self.imp_bmi = tk.StringVar()

        # radio buttons for methods
        self.metric = tk.StringVar()
        self.imperial = tk.StringVar()

        ttk.Label(self, text="Measurement Method:").grid(row=0, column=0, sticky=W)
        self.but1 = ttk.Radiobutton(self, text="Metric", command=self.MetricButtons, value="Metric", state='normal')
        self.but1.grid(row=0, column=1, sticky=W)
        self.but2 = ttk.Radiobutton(self, text="Imperial", command=self.ImperialButtons, value="Imperial",
                                    state='normal')
        self.but2.grid(row=0, column=2, sticky=W)

    # display metric grid components

    def MetricButtons(self):

        self.but2.configure(state='disabled')
        ttk.Label(self, text="Name:").grid(row=1, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.name).grid(row=1, column=1, columnspan=1, sticky=EW)
        ttk.Label(self, text="Weight(KGs):").grid(row=2, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.bmi_weight, validate="key", validatecommand=(self.vld, "%P")).grid(row=2,
                                                                                                             column=1,
                                                                                                             sticky=E)

        ttk.Label(self, text="Height(CMs):").grid(row=3, sticky=W)
        ttk.Entry(self, textvariable=self.bmi_height, validate="key", validatecommand=(self.vld, "%P")).grid(row=3,
                                                                                                             column=1,
                                                                                                             sticky=E)

        ttk.Label(self, text="BMI:").grid(row=4, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.bmi, state="readonly").grid(row=4, column=1, sticky=W)
        self.bmi.set("Just A Moment..")

        ttk.Button(self, text="Calculate BMI", command=self.calculate).grid(row=6, column=1, sticky=E)
        ttk.Button(self, text="Clear", command=self.clear).grid(row=7, column=1, sticky=E)

    # display imperial grid

    def ImperialButtons(self):

        self.but1.config(state='disabled')
        ttk.Label(self, text="Name:").grid(row=1, column=2, sticky=E)
        ttk.Entry(self, textvariable=self.name).grid(row=1, column=3, columnspan=2, sticky=EW)
        ttk.Label(self, text="Weight(Stones & lbs):").grid(row=2, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.imp_stones, validate="key", validatecommand=(self.vld, "%P")).grid(row=2,
                                                                                                             column=3,
                                                                                                             sticky=E)
        ttk.Spinbox(self, textvariable=self.imp_lbs, from_=0, to=13, state="readonly").grid(row=2, column=4, sticky=W)
        self.imp_lbs.set("0")

        ttk.Label(self, text="Height(Ft & Inches):").grid(row=3, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.imp_feet, validate="key", validatecommand=(self.vld, "%P")).grid(row=3,
                                                                                                           column=3,
                                                                                                           sticky=E)
        ttk.Spinbox(self, textvariable=self.imp_inches, from_=0, to=11, state="readonly").grid(row=3, column=4,
                                                                                               sticky=W)
        self.imp_inches.set("0")

        ttk.Label(self, text="BMI:").grid(row=4, column=2, sticky=E)
        ttk.Entry(self, textvariable=self.bmi, state="readonly").grid(row=4, column=3, sticky=W)
        self.bmi.set("Just A Moment...")

        ttk.Button(self, text="Calculate BMI", command=self.calculate).grid(row=6, column=3, sticky=E)
        ttk.Button(self, text="Clear", command=self.clear).grid(row=7, column=3, sticky=E)

    # metric bmi calculation

    def calculate(self):

        if self.but1.instate(['disabled']):
            self.metric_from_imperial()
        else:
            self.imperial_from_metric()

        fo = open("bmi_data.csv", "a")
        try:
            weight = float(self.bmi_weight.get())
            height = float(self.bmi_height.get())
            bmi_met = weight / ((height / 100) ** 2)
            bmi_met = round(bmi_met, 2)
            self.bmi.set(bmi_met)
        except ValueError:  # non integer value
            self.bmi.set("Numbers Only!")
        except ZeroDivisionError:  # zero division errors exceptions
            self.bmi.set("Cannot Divide by Zero")
        except:
            self.bmi.set("Something went wrong")
        else:

            self.bmi.set(bmi_met)
            fo.write(
                "\nName: %s,Height: %.2fCMS,Weight: %.2fKGs, BMI: %.2f, Date: %s \n" % (self.name.get(), weight, height,
                                                                                        bmi_met, self.dt))
            self.bmi_info_message()

        fo.close()

    def clear(self):  # calls the set methods for all str var and sets them to empty strings

        self.name.set("")
        self.bmi.set("")
        self.bmi_weight.set("")
        self.bmi_height.set("")
        self.imp_feet.set("")
        self.imp_inches.set("")
        self.imp_lbs.set("")
        self.imp_stones.set("")
        self.imp_bmi.set("")
        for widget in BMIFrame.winfo_children(self):
            widget.destroy()

        ttk.Label(self, text="Measurement Method:").grid(row=0, column=0, sticky=W)
        self.but1 = ttk.Radiobutton(self, text="Metric", command=self.MetricButtons, value="Metric", state='normal')
        self.but1.grid(row=0, column=1, sticky=W)
        self.but2 = ttk.Radiobutton(self, text="Imperial", command=self.ImperialButtons, value="Imperial",
                                    state='normal')
        self.but2.grid(row=0, column=2, sticky=W)

    def imperial_from_metric(self):

        kgs_to_stones = ((int(self.bmi_weight.get())) / 6.35)
        kgs_to_stones = int(kgs_to_stones)
        self.imp_stones.set(kgs_to_stones)

        kgs_to_lbs = (int(self.bmi_weight.get()) * 2.205)
        kgs_to_lbs = int(kgs_to_lbs)
        kgs_to_lbs = (kgs_to_lbs % 14)
        self.imp_lbs.set(kgs_to_lbs)

        cms_to_inches = (((int(self.bmi_height.get())) / 2.54) % 12)
        cms_to_inches = int(cms_to_inches)
        self.imp_inches.set(cms_to_inches)

        cms_to_feet = int(int(self.bmi_height.get()) / 30.48)
        self.imp_feet.set(cms_to_feet)

        ttk.Button(self, text="Calculate BMI", command=self.calculate).grid(row=6, column=1, sticky=E)
        ttk.Button(self, text="Clear", command=self.clear).grid(row=7, column=1, sticky=E)

        ttk.Label(self, text="Weight(Stones & lbs):").grid(row=2, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.imp_stones, state="readonly").grid(row=2, column=3, sticky=E)
        ttk.Entry(self, textvariable=self.imp_lbs, state="readonly").grid(row=2, column=4, sticky=W)

        ttk.Label(self, text="Height(Ft & Inches):").grid(row=3, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.imp_feet, state="readonly").grid(row=3, column=3, sticky=E)
        ttk.Entry(self, textvariable=self.imp_inches, state="readonly").grid(row=3, column=4, sticky=W)

    def metric_from_imperial(self):

        stones_to_kgs = ((int(self.imp_stones.get())) * 6.35)
        stones_to_kgs = round(stones_to_kgs, 1)

        lbs_to_kgs = (int(self.imp_lbs.get()) / 2.205)
        lbs_to_kgs = round(lbs_to_kgs, 1)

        self.bmi_weight.set(round((lbs_to_kgs + stones_to_kgs)))

        inches_to_cms = (int(self.imp_inches.get()) * 2.54)
        inches_to_cms = round(inches_to_cms, 2)
        feet_to_cms = (int(self.imp_feet.get()) * 30.48)
        feet_to_cms = round(feet_to_cms, 2)
        ft_in_to_cm = (float(feet_to_cms + inches_to_cms))
        ft_in_to_cm = round(ft_in_to_cm, 2)
        self.bmi_height.set(ft_in_to_cm)

        ttk.Label(self, text="Weight(KGs):").grid(row=2, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.bmi_weight).grid(row=2, column=1, sticky=E)

        ttk.Label(self, text="Height(CMs):").grid(row=3, sticky=W)
        ttk.Entry(self, textvariable=self.bmi_height).grid(row=3, column=1, sticky=E)

        ttk.Button(self, text="Calculate BMI", command=self.calculate).grid(row=6, column=3, sticky=E)
        ttk.Button(self, text="Clear", command=self.clear).grid(row=7, column=3, sticky=E)

    def bmi_info_message(self):
        check = float(self.bmi.get())

        if check < 18.5:
            mb.showwarning("Your BMI", "You are Underweight!")
        elif 18.5 <= check <= 24.9:
            mb.showinfo("Your BMI", "You are a normal and healthy weight")
        elif 25 <= check <= 29.9:
            mb.showwarning("Your BMI", "You Are Overweight")
        else:
            mb.showwarning("Your BMI", "You are Obese")

    def only_numeric_input(self, P):

        """"checks if entry's value is an integer, greater than 1 or empty and returns an appropriate boolean"""
        if P.isdigit() and float(P) > 0:  # if a digit was entered or nothing was entered
            return True
        elif P == "":  # if nothing was entered or digit deleted
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    root.title("BMI Calculator")
    BMIFrame(root)
    root.mainloop()
