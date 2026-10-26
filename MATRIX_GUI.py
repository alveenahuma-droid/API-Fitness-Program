# MATRIX Fitness Tracker - Graphical User Interface
# This GUI connects to the existing modules:
# LoginModule, DataAPI, CommonAPI, FileInputOutputAPI and Config
# All data is read from and saved to ExerciseData.txt

import os
import tkinter as tk
from tkinter import ttk, messagebox

# Make sure the program runs from the same folder as the other files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import Config as con
import CommonAPI as common
import DataAPI as data
import FileInputOutputAPI as fileIO
import LoginModule as login

# colours
WHITE = "#ffffff"
DARK = "#1e293b"
GREY = "#e2e8f0"
LIGHT = "#f1f5f9"
BLUE = "#0ea5e9"
GREEN = "#16a34a"
RED = "#dc2626"
FONT = "Segoe UI"

MAX_ATTEMPTS = 3


class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MATRIX - Fitness Tracker")
        self.geometry("1000x650")
        self.configure(bg=WHITE)
        self.username = ""
        self.attempts = 0

        # Load starting data from ExerciseData.txt
        if not self.load_data():
            self.destroy()
            return

        self.show_login()

    # --------------------------------------------------
    # Loads default data from the ExerciseData.txt file
    # --------------------------------------------------
    def load_data(self):
        try:
            contents = fileIO.LoadDefaultData()
            con.startHeight = float(contents[0])
            con.startWeight = float(contents[1])
            con.startBMI = float(contents[2])
            con.units = contents[3].strip().upper()
            return True
        except:
            messagebox.showerror("Error", "Could not load ExerciseData.txt")
            return False

    # --------------------------------------------------
    # Login screem
    # --------------------------------------------------
    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg=WHITE)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="MATRIX", font=(FONT, 28, "bold"),
                 bg=WHITE, fg=DARK).pack(pady=(0, 5))
        tk.Label(frame, text="Fitness Tracking Application",
                 font=(FONT, 11), bg=WHITE, fg="#64748b").pack(pady=(0, 25))

        tk.Label(frame, text="Username", bg=WHITE, font=(FONT, 10)).pack(anchor="w")
        self.user_entry = tk.Entry(frame, font=(FONT, 12), width=28, bd=1, relief="solid")
        self.user_entry.pack(pady=(2, 12))

        tk.Label(frame, text="Password", bg=WHITE, font=(FONT, 10)).pack(anchor="w")
        self.pass_entry = tk.Entry(frame, font=(FONT, 12), width=28, show="*", bd=1, relief="solid")
        self.pass_entry.pack(pady=(2, 18))

        tk.Button(frame, text="Login", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, width=20, height=2,
                  relief="flat", cursor="hand2",
                  command=self.try_login).pack()

        self.login_msg = tk.Label(frame, text="", bg=WHITE, fg=RED, font=(FONT, 10))
        self.login_msg.pack(pady=12)

        self.user_entry.focus()
        self.pass_entry.bind("<Return>", lambda e: self.try_login())

    def try_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()

        success, message, correct_user = login.AttemptLogin(username, password)

        if success:
            self.username = correct_user
            self.build_main()
        else:
            self.attempts += 1
            remaining = MAX_ATTEMPTS - self.attempts
            self.login_msg.config(text=f"{message}. Attempts left: {remaining}", fg=RED)
            self.pass_entry.delete(0, "end")
            self.check_lockout()
            
    
    def check_lockout(self):
        if self.attempts >= MAX_ATTEMPTS:
            self.user_entry.config(state="disabled")
            self.pass_entry.config(state="disabled")

            # Disable Login button
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget("text") == "Login":
                            child.config(state="disabled")

            # Starts 10-second countdown
            self.lock_time = 10
            self.update_lock_message()

    def update_lock_message(self):
        if self.lock_time > 0:
            self.login_msg.config(
                text=f"Login failed. Try again in {self.lock_time} seconds...",
                fg=RED
            )
            self.lock_time -= 1
            self.after(1000, self.update_lock_message)   # wait 1 second then call again
        else:
            # Timer finished – unlocks everything
            self.attempts = 0
            self.user_entry.config(state="normal")
            self.pass_entry.config(state="normal")

            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget("text") == "Login":
                            child.config(state="normal")

            self.login_msg.config(text="You can try logging in again.", fg=GREEN)
            self.user_entry.focus()
    # --------------------------------------------------
    # Main window
    # --------------------------------------------------
    def build_main(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.load_data()

        # Header
        header = tk.Frame(self, bg=DARK, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="  MATRIX", font=(FONT, 16, "bold"),
                 bg=DARK, fg=WHITE).pack(side="left", padx=15)

        tk.Label(header, text=self.username.upper(),
                 font=(FONT, 11, "bold"), bg=DARK, fg="#94a3b8").pack(side="right", padx=20)

        # Body
        body = tk.Frame(self, bg=WHITE)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=LIGHT, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        menu = [
            ("Dashboard", self.show_dashboard),
            ("Enter / Update Data", self.show_userdata),
            ("Change Units", self.show_units),
            ("Record Activity", self.show_record),
            ("Basic Activity Log", lambda: self.show_log(False)),
            ("Extended Activity Log", lambda: self.show_log(True)),
            ("Add New Activity", self.show_add),
            ("Verify with Web APIs", self.show_verify),
            ("Convert Records", self.show_convert),
            ("Exit", self.quit)
        ]

        for text, command in menu:
            btn = tk.Button(sidebar, text=text, font=(FONT, 10),
                            bg=LIGHT, fg=DARK, relief="flat",
                            anchor="w", padx=20, pady=10,
                            cursor="hand2", command=command)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=GREY))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=LIGHT))

        # Content area
        self.content = tk.Frame(body, bg=WHITE)
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------
    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.content, text="Activity Dashboard",
                 font=(FONT, 18, "bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(0, 15))

        file_data = fileIO.LoadAllFileData()
        records = data._activity_records(file_data)

        # Calculate values
        try:
            total_loss = data.CalculateTotalWeightLoss(file_data, con.units)
            current_weight = round(max(con.startWeight - total_loss, 0.01), 2)
            if con.units == "KG":
                bmi = round(common.BMICalculator(current_weight, con.startHeight), 1)
            else:
                bmi = round(common.BMICalculatorWeightInPounds(current_weight, con.startHeight), 1)
            total_cals = data.CalculateTotalCaloriesBurned(file_data)
        except:
            current_weight, bmi, total_cals, total_loss = con.startWeight, 0, 0, 0

        # Metric cards
        cards_frame = tk.Frame(self.content, bg=WHITE)
        cards_frame.pack(fill="x", pady=10)

        metrics = [
            (f"{current_weight} {con.units}", "Current Weight", BLUE),
            (str(bmi), "BMI", "#8b5cf6"),
            (str(total_cals), "Calories Burned", "#f59e0b"),
            (f"{total_loss} {con.units}", "Weight Lost", GREEN)
        ]

        for value, label, colour in metrics:
            card = tk.Frame(cards_frame, bg=WHITE, highlightbackground=GREY,
                            highlightthickness=1, width=170, height=100)
            card.pack(side="left", padx=8)
            card.pack_propagate(False)

            tk.Label(card, text=value, font=(FONT, 16, "bold"),
                     bg=WHITE, fg=colour).pack(pady=(20, 5))
            tk.Label(card, text=label, font=(FONT, 9),
                     bg=WHITE, fg="#64748b").pack()

        # Recent activities
        tk.Label(self.content, text="Recent Activities",
                 font=(FONT, 13, "bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(25, 8))

        columns = ("Activity", "Duration", "Calories", "Weight Lost", "Units")
        tree = ttk.Treeview(self.content, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        tree.pack(fill="x")

        for r in records[-8:]:
            tree.insert("", "end", values=(
                r["activity"], r["duration"], r["calories"],
                r["weight_loss"], r["units"]
            ))

        if not records:
            tree.insert("", "end", values=("No records yet", "", "", "", ""))

    # --------------------------------------------------
    # Enter/update user data
    # --------------------------------------------------
    def show_userdata(self):
        self.clear_content()
        tk.Label(self.content, text="Enter / Update User Data",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        form = tk.Frame(self.content, bg=WHITE)
        form.pack(anchor="w")

        tk.Label(form, text="Height (metres):", bg=WHITE, font=(FONT, 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.height_entry = tk.Entry(form, font=(FONT, 11), width=20)
        self.height_entry.grid(row=0, column=1, pady=8, padx=10)
        self.height_entry.insert(0, str(con.startHeight))

        tk.Label(form, text="Weight:", bg=WHITE, font=(FONT, 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.weight_entry = tk.Entry(form, font=(FONT, 11), width=20)
        self.weight_entry.grid(row=1, column=1, pady=8, padx=10)
        self.weight_entry.insert(0, str(con.startWeight))

        tk.Label(form, text="Units:", bg=WHITE, font=(FONT, 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.unit_var = tk.StringVar(value=con.units)
        unit_frame = tk.Frame(form, bg=WHITE)
        unit_frame.grid(row=2, column=1, sticky="w", padx=10)
        tk.Radiobutton(unit_frame, text="KG", variable=self.unit_var, value="KG", bg=WHITE).pack(side="left")
        tk.Radiobutton(unit_frame, text="LBS", variable=self.unit_var, value="LBS", bg=WHITE).pack(side="left")

        tk.Button(self.content, text="Save Data", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, relief="flat", width=15, height=2,
                  command=self.save_userdata).pack(anchor="w", pady=20)

        self.msg = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10))
        self.msg.pack(anchor="w")

    def save_userdata(self):
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            units = self.unit_var.get()

            if height <= 0 or weight <= 0:
                self.msg.config(text="Height and weight must be greater than 0", fg=RED)
                return

            con.startHeight = height
            con.startWeight = weight
            con.units = units

            if units == "KG":
                con.startBMI = round(common.BMICalculator(weight, height), 2)
            else:
                con.startBMI = round(common.BMICalculatorWeightInPounds(weight, height), 2)

            fileIO.InsertNewUserData(con.startHeight, con.startWeight, con.startBMI, con.units)
            self.msg.config(text="User data saved successfully!", fg=GREEN)
        except:
            self.msg.config(text="Please enter valid numbers", fg=RED)

    # --------------------------------------------------
    # Change units
    # --------------------------------------------------
    def show_units(self):
        self.clear_content()
        tk.Label(self.content, text="Change Weight Units",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        tk.Label(self.content, text=f"Current unit: {con.units}",
                 font=(FONT, 12), bg=WHITE).pack(anchor="w", pady=5)
        tk.Label(self.content, text=f"Current weight: {con.startWeight} {con.units}",
                 font=(FONT, 12), bg=WHITE).pack(anchor="w", pady=5)

        btn_frame = tk.Frame(self.content, bg=WHITE)
        btn_frame.pack(anchor="w", pady=25)

        tk.Button(btn_frame, text="Switch to KG", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, width=15, height=2, relief="flat",
                  command=lambda: self.change_units("KG")).pack(side="left", padx=8)

        tk.Button(btn_frame, text="Switch to LBS", font=(FONT, 11, "bold"),
                  bg="#8b5cf6", fg=WHITE, width=15, height=2, relief="flat",
                  command=lambda: self.change_units("LBS")).pack(side="left", padx=8)

        self.msg = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10))
        self.msg.pack(anchor="w", pady=10)

    def change_units(self, new_unit):
        if new_unit == con.units:
            self.msg.config(text=f"Already using {con.units}", fg=RED)
            return

        if new_unit == "LBS":
            con.startWeight = common.KilosToPounds(con.startWeight)
        else:
            con.startWeight = common.PoundsToKilos(con.startWeight)

        con.units = new_unit
        con.startBMI = round(common.BMICalculator(con.startWeight, con.startHeight)
                             if new_unit == "KG" else
                             common.BMICalculatorWeightInPounds(con.startWeight, con.startHeight), 2)

        fileIO.InsertNewUserData(con.startHeight, con.startWeight, con.startBMI, con.units)

        # Also convert old activity records
        try:
            data.ConvertAllRecordsToNewUnits(new_unit)
        except:
            pass

        self.msg.config(text=f"Units changed to {new_unit}. Weight is now {con.startWeight} {new_unit}", fg=GREEN)

    # --------------------------------------------------
    # Record activity
    # --------------------------------------------------
    def show_record(self):
        self.clear_content()
        tk.Label(self.content, text="Record Activity",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        form = tk.Frame(self.content, bg=WHITE)
        form.pack(anchor="w")

        tk.Label(form, text="Activity:", bg=WHITE, font=(FONT, 11)).grid(row=0, column=0, sticky="w", pady=8)
        activities = [a["Activity"] for a in con.ListOfActivities]
        self.act_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.act_var, values=activities,
                     state="readonly", width=25).grid(row=0, column=1, pady=8, padx=10)

        tk.Label(form, text="Duration:", bg=WHITE, font=(FONT, 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.dur_var = tk.StringVar(value="30")
        dur_frame = tk.Frame(form, bg=WHITE)
        dur_frame.grid(row=1, column=1, sticky="w", padx=10)
        for text, val in [("15 min", "15"), ("30 min", "30"), ("60 min", "60"), ("Custom", "custom")]:
            tk.Radiobutton(dur_frame, text=text, variable=self.dur_var, value=val, bg=WHITE).pack(side="left")

        tk.Label(form, text="Custom minutes:", bg=WHITE, font=(FONT, 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.custom_entry = tk.Entry(form, font=(FONT, 11), width=10)
        self.custom_entry.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        tk.Button(self.content, text="Save Activity", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, relief="flat", width=15, height=2,
                  command=self.save_activity).pack(anchor="w", pady=20)

        self.msg = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10))
        self.msg.pack(anchor="w")

    def save_activity(self):
        activity = self.act_var.get()
        if not activity:
            self.msg.config(text="Please select an activity", fg=RED)
            return

        met = data.GetMetValueForActivity(activity)

        if self.dur_var.get() == "custom":
            try:
                minutes = int(self.custom_entry.get())
                if minutes <= 0:
                    self.msg.config(text="Duration must be greater than 0", fg=RED)
                    return
            except:
                self.msg.config(text="Please enter a valid number of minutes", fg=RED)
                return
        else:
            minutes = int(self.dur_var.get())

        try:
            if con.units == "KG":
                cals = common.CaloriesBurnedInCustomTime(met, con.startWeight, minutes)
                loss = common.WeightLostInKilosCustomTime(met, con.startWeight, minutes)
            else:
                cals = common.CaloriesBurnedInCustomTimeLb(met, con.startWeight, minutes)
                loss = common.WeightLostInPoundsInCustomTime(met, con.startWeight, minutes)

            cals = round(cals, 2)
            loss = round(loss, 4)

            fileIO.AddNewActivityRecord(activity, minutes, cals, loss, con.units)
            self.msg.config(text=f"Saved! {activity} - {cals} calories, {loss} {con.units} lost", fg=GREEN)
        except Exception as e:
            self.msg.config(text=f"Error: {e}", fg=RED)

    # --------------------------------------------------
    # Activity extended log
    # --------------------------------------------------
    def show_log(self, extended=False):
        self.clear_content()
        title = "Extended Activity Log" if extended else "Basic Activity Log"
        tk.Label(self.content, text=title, font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        file_data = fileIO.LoadAllFileData()
        records = data._activity_records(file_data)

        columns = ("Activity", "Duration", "Calories", "Weight Lost", "Units")
        tree = ttk.Treeview(self.content, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        tree.pack(fill="x", pady=10)

        for r in records:
            tree.insert("", "end", values=(
                r["activity"], r["duration"], r["calories"],
                r["weight_loss"], r["units"]
            ))

        # Summary
        summary = tk.Frame(self.content, bg=LIGHT)
        summary.pack(fill="x", pady=15)

        total_cals = data.CalculateTotalCaloriesBurned(file_data)
        total_loss = data.CalculateTotalWeightLoss(file_data, con.units)

        tk.Label(summary, text=f"Total Calories: {total_cals}",
                 bg=LIGHT, font=(FONT, 11)).pack(anchor="w", padx=15, pady=3)
        tk.Label(summary, text=f"Total Weight Lost: {total_loss} {con.units}",
                 bg=LIGHT, font=(FONT, 11)).pack(anchor="w", padx=15, pady=3)

        if extended:
            avg = data.CalculateAverageCalories(file_data)
            biggest = data.CalculateBiggestCalorieBurn(file_data)
            biggest_loss = data.CalculateBiggestWeightLossInterval(file_data, con.units)

            tk.Label(summary, text=f"Average Calories: {avg}",
                     bg=LIGHT, font=(FONT, 11)).pack(anchor="w", padx=15, pady=3)
            tk.Label(summary, text=f"Largest Calorie Burn: {biggest}",
                     bg=LIGHT, font=(FONT, 11)).pack(anchor="w", padx=15, pady=3)
            tk.Label(summary, text=f"Biggest Weight Loss: {biggest_loss} {con.units}",
                     bg=LIGHT, font=(FONT, 11)).pack(anchor="w", padx=15, pady=3)

    # --------------------------------------------------
    # Add new activity
    # --------------------------------------------------
    def show_add(self):
        self.clear_content()
        tk.Label(self.content, text="Add New Activity",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        form = tk.Frame(self.content, bg=WHITE)
        form.pack(anchor="w")

        tk.Label(form, text="Activity Name:", bg=WHITE, font=(FONT, 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.name_entry = tk.Entry(form, font=(FONT, 11), width=25)
        self.name_entry.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(form, text="MET Value:", bg=WHITE, font=(FONT, 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.met_entry = tk.Entry(form, font=(FONT, 11), width=25)
        self.met_entry.grid(row=1, column=1, pady=8, padx=10)

        tk.Button(self.content, text="Add Activity", font=(FONT, 11, "bold"),
                  bg=GREEN, fg=WHITE, relief="flat", width=15, height=2,
                  command=self.add_activity).pack(anchor="w", pady=20)

        self.msg = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10))
        self.msg.pack(anchor="w")

    def add_activity(self):
        name = self.name_entry.get().strip()
        try:
            met = float(self.met_entry.get())
        except:
            self.msg.config(text="MET value must be a number", fg=RED)
            return

        success, message = data.AddActivityToList(name, met)
        self.msg.config(text=message, fg=GREEN if success else RED)

        if success:
            self.name_entry.delete(0, "end")
            self.met_entry.delete(0, "end")

    # --------------------------------------------------
    # Verify with web APIs
    # --------------------------------------------------
    def show_verify(self):
        self.clear_content()
        tk.Label(self.content, text="Verify with Web APIs",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        tk.Label(self.content, text="This compares your local calculations with online web services.",
                 bg=WHITE, font=(FONT, 10)).pack(anchor="w", pady=5)

        tk.Button(self.content, text="Run Verification", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, relief="flat", width=18, height=2,
                  command=self.run_verify).pack(anchor="w", pady=15)

        self.verify_result = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10),
                                      justify="left", wraplength=600)
        self.verify_result.pack(anchor="w", pady=10)

    def run_verify(self):
        try:
            if con.units == "KG":
                local = common.KilosToPounds(con.startWeight)
                web = common.KilosToPoundsWebService(con.startWeight)
                text = f"Local conversion: {con.startWeight} KG = {local} LBS\n"
                text += f"Web API result: {web if web else 'Unavailable'}\n\n"
            else:
                local = common.PoundsToKilos(con.startWeight)
                web = common.PoundsToKilosWebService(con.startWeight)
                text = f"Local conversion: {con.startWeight} LBS = {local} KG\n"
                text += f"Web API result: {web if web else 'Unavailable'}\n\n"

            # BMI check
            if con.units == "KG":
                weight_kg = con.startWeight
            else:
                weight_kg = common.PoundsToKilos(con.startWeight)

            local_bmi = common.BMICalculator(weight_kg, con.startHeight)
            web_bmi = common.BMICalculatorWebService(weight_kg, con.startHeight)

            text += f"Local BMI: {local_bmi}\n"
            text += f"Web API BMI: {web_bmi if web_bmi else 'Unavailable'}"

            self.verify_result.config(text=text, fg=DARK)
        except Exception as e:
            self.verify_result.config(text=f"Error: {e}", fg=RED)

    # --------------------------------------------------
    # convert all records 
    # --------------------------------------------------
    def show_convert(self):
        self.clear_content()
        tk.Label(self.content, text="Convert All Records",
                 font=(FONT, 18, "bold"), bg=WHITE).pack(anchor="w", pady=(0, 15))

        tk.Label(self.content, text="This will convert all saved activity records to a new unit.",
                 bg=WHITE, font=(FONT, 10)).pack(anchor="w", pady=5)

        self.conv_var = tk.StringVar(value="KG")
        tk.Radiobutton(self.content, text="Convert everything to KG",
                       variable=self.conv_var, value="KG", bg=WHITE, font=(FONT, 11)).pack(anchor="w", pady=3)
        tk.Radiobutton(self.content, text="Convert everything to LBS",
                       variable=self.conv_var, value="LBS", bg=WHITE, font=(FONT, 11)).pack(anchor="w", pady=3)

        tk.Button(self.content, text="Convert Records", font=(FONT, 11, "bold"),
                  bg=BLUE, fg=WHITE, relief="flat", width=18, height=2,
                  command=self.convert_records).pack(anchor="w", pady=20)

        self.msg = tk.Label(self.content, text="", bg=WHITE, font=(FONT, 10))
        self.msg.pack(anchor="w")

    def convert_records(self):
        target = self.conv_var.get()
        try:
            data.ConvertAllRecordsToNewUnits(target)
            self.msg.config(text=f"All records converted to {target}", fg=GREEN)
        except Exception as e:
            self.msg.config(text=f"Error: {e}", fg=RED)


# starts application
if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()