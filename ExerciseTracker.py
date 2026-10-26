import LoginModule as login
import DataAPI as data
import CommonAPI as common
import Config as con
import FileInputOutputAPI as fileIO

# --------------------------------------------------
# INITIALISE PROGRAM
# --------------------------------------------------
def InitialiseUserData():
    contents = (
        fileIO.LoadDefaultData()
    )

    con.startHeight = float(
        contents[0]
    )

    con.startWeight = float(
        contents[1]
    )

    con.startBMI = float(
        contents[2]
    )

    con.units = (
        contents[3].upper()
    )

# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------
def DisplayMainMenu():
    print(
        "\n" + "=" * 48
    )

    print(
        "FITNESS TRACKING APPLICATION"
    )

    print(
        "=" * 48
    )

    print(
        "1. Enter / update user data"
    )

    print(
        "2. Change weight units"
    )

    print(
        "3. Record an activity"
    )

    print(
        "4. View BASIC activity log"
    )

    print(
        "5. View EXTENDED activity log"
    )

    print(
        "6. Add a new activity"
    )

    print(
        "7. Verify calculations using web APIs"
    )

    print(
        "8. Exit"
    )
    print(
        "9. Convert all records to new units"
        ) #Added option to convert all records to new units

# --------------------------------------------------
# CURRENT BMI
# --------------------------------------------------
def _calculate_current_bmi():
    if con.units == "KG":
        return (
            common.BMICalculator(
                con.startWeight,
                con.startHeight
            )
        )
    return (
        common.BMICalculatorWeightInPounds(
            con.startWeight,
            con.startHeight
        )
    )

# --------------------------------------------------
# USER DATA
# --------------------------------------------------
def EnterOrUpdateUserData():
    print(
        "\nCurrent starting data:"
    )
    data.ViewStartingData()
    con.units = (
        data.GetUnits()
    )
    data.GetStartHeight()
    data.GetStartWeight()
    con.startBMI = (
        _calculate_current_bmi()
    )
    fileIO.InsertNewUserData(
        con.startHeight,
        con.startWeight,
        con.startBMI,
        con.units
    )

    print(
        "\nUser data updated successfully."
    )

    data.ViewStartingData()

# --------------------------------------------------
# CHANGE UNITS
# --------------------------------------------------
def ChangeUnits():
    newUnits = data.GetUnits()

    if newUnits == con.units:
        print(
            f"\nThe application is already "
            f"using {con.units}."
        )
        return
    if newUnits == "LBS":
        con.startWeight = (
            common.KilosToPounds(
                con.startWeight
            )
        )

    else:
        con.startWeight = (
            common.PoundsToKilos(
                con.startWeight
            )
        )

    con.units = newUnits

    con.startBMI = (
        _calculate_current_bmi()
    )

    fileIO.InsertNewUserData(
        con.startHeight,
        con.startWeight,
        con.startBMI,
        con.units
    )

    print(
        f"\nUnits changed to {con.units}."
    )

    print(
        f"Starting weight is now "
        f"{con.startWeight} {con.units}."
    )


# --------------------------------------------------
# RECORD ACTIVITY
# --------------------------------------------------

def RecordActivity():

    data.ViewActivityList()

    activity = (
        data.GetActivity()
    )

    metValue = (
        data.GetMetValueForActivity(
            activity
        )
    )

    duration = (
        data.GetActivityDuration()
    )

    if con.units == "KG":

        caloriesBurned = (
            common.CaloriesBurnedInCustomTime(
                metValue,
                con.startWeight,
                duration
            )
        )

        weightLoss = (
            common.WeightLostInKilosCustomTime(
                metValue,
                con.startWeight,
                duration
            )
        )

    else:

        caloriesBurned = (
            common.CaloriesBurnedInCustomTimeLb(
                metValue,
                con.startWeight,
                duration
            )
        )

        weightLoss = (
            common.WeightLostInPoundsInCustomTime(
                metValue,
                con.startWeight,
                duration
            )
        )

    caloriesBurned = round(
        caloriesBurned,
        2
    )

    weightLoss = round(
        weightLoss,
        2
    )

    fileIO.AddNewActivityRecord(
        activity.title(),
        duration,
        caloriesBurned,
        weightLoss,
        con.units
    )

    print(
        "\nActivity recorded successfully."
    )

    print(
        f"Activity: {activity.title()}"
    )

    print(
        f"Duration: {duration} minutes"
    )

    print(
        f"Calories burned: "
        f"{caloriesBurned}"
    )

    print(
        f"Estimated weight loss: "
        f"{weightLoss} {con.units}"
    )


# --------------------------------------------------
# NEW BMI AFTER ACTIVITY
# --------------------------------------------------

def _new_bmi_after_activity(
        fileData):

    totalWeightLoss = (
        data.CalculateTotalWeightLoss(
            fileData,
            con.units
        )
    )

    newWeight = max(
        con.startWeight -
        totalWeightLoss,
        0.01
    )

    if con.units == "KG":

        return (
            common.BMICalculator(
                newWeight,
                con.startHeight
            )
        )

    return (
        common.BMICalculatorWeightInPounds(
            newWeight,
            con.startHeight
        )
    )


# --------------------------------------------------
# BASIC ACTIVITY LOG
# --------------------------------------------------

def ViewBASICActivityLog():

    fileData = (
        fileIO.LoadAllFileData()
    )

    data.DisplayActivityLogHeader(
        fileData
    )

    data.DisplayActivityLogData(
        fileData
    )

    totalKg = (
        data.CalculateTotalWeightLoss(
            fileData,
            "KG"
        )
    )

    totalLbs = (
        data.CalculateTotalWeightLoss(
            fileData,
            "LBS"
        )
    )

    print(
        "\n--- BASIC SUMMARY ---"
    )

    print(
        "Total activity duration:",
        data.CalculateTotalActvityDuration(
            fileData
        ),
        "minutes"
    )

    print(
        "Total calories burned:",
        data.CalculateTotalCaloriesBurned(
            fileData
        )
    )

    print(
        "Starting weight:",
        con.startWeight,
        con.units
    )

    print(
        "Starting BMI:",
        con.startBMI
    )

    print(
        "Total weight lost in KG:",
        totalKg
    )

    print(
        "Total weight lost in LBS:",
        totalLbs
    )

    print(
        "New BMI:",
        _new_bmi_after_activity(
            fileData
        )
    )


# --------------------------------------------------
# EXTENDED ACTIVITY LOG
# --------------------------------------------------

def ViewEXTENDEDActivityLog():

    ViewBASICActivityLog()

    fileData = (
        fileIO.LoadAllFileData()
    )

    print(
        "\n--- EXTENDED STATISTICS ---"
    )

    print(
        "Average calories burned:",
        data.CalculateAverageCalories(
            fileData
        )
    )

    print(
        "Largest calorie burn:",
        data.CalculateBiggestCalorieBurn(
            fileData
        )
    )

    print(
        f"Biggest weight-loss interval "
        f"({con.units}):",

        data.CalculateBiggestWeightLossInterval(
            fileData,
            con.units
        )
    )


# --------------------------------------------------
# ADD NEW ACTIVITY
# --------------------------------------------------

def AddNewActivity():

    print(
        "\n--- ADD NEW ACTIVITY ---"
    )

    activityName = input(
        "Enter the activity name: "
    ).strip()

    metValue = (
        data.GetPositiveFloat(
            "Enter the MET value: "
        )
    )

    success, message = (
        data.AddActivityToList(
            activityName,
            metValue
        )
    )

    print(message)

    if success:

        data.ViewActivityList()


# --------------------------------------------------
# EXTERNAL WEB API VERIFICATION
# --------------------------------------------------

def VerifyWithWebServices():

    print(
        "\n--- WEB API VERIFICATION ---"
    )

    if con.units == "KG":

        localConversion = (
            common.KilosToPounds(
                con.startWeight
            )
        )

        webConversion = (
            common.KilosToPoundsWebService(
                con.startWeight
            )
        )

        print(
            f"Local conversion: "
            f"{con.startWeight} KG = "
            f"{localConversion} LBS"
        )

        if webConversion is None:

            print(
                "External KG-to-LBS verification "
                "unavailable. Check API key or "
                "internet connection."
            )

        else:

            print(
                f"Web API conversion: "
                f"{con.startWeight} KG = "
                f"{webConversion} LBS"
            )

        weightKg = (
            con.startWeight
        )

    else:

        localConversion = (
            common.PoundsToKilos(
                con.startWeight
            )
        )

        webConversion = (
            common.PoundsToKilosWebService(
                con.startWeight
            )
        )

        print(
            f"Local conversion: "
            f"{con.startWeight} LBS = "
            f"{localConversion} KG"
        )

        if webConversion is None:

            print(
                "External LBS-to-KG verification "
                "unavailable. Check API key or "
                "internet connection."
            )

        else:

            print(
                f"Web API conversion: "
                f"{con.startWeight} LBS = "
                f"{webConversion} KG"
            )

        weightKg = (
            common.PoundsToKilos(
                con.startWeight
            )
        )

    localBMI = (
        common.BMICalculator(
            weightKg,
            con.startHeight
        )
    )

    webBMI = (
        common.BMICalculatorWebService(
            weightKg,
            con.startHeight
        )
    )

    print(
        f"Local BMI calculation: "
        f"{localBMI}"
    )

    if webBMI is None:

        print(
            "External BMI verification "
            "unavailable. Check the "
            "internet connection."
        )

    else:

        print(
            f"Web API BMI calculation: "
            f"{webBMI}"
        )


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

def RunProgram():

    while True:

        DisplayMainMenu()

        choice = input(
            "\nEnter your menu choice: "
        ).strip()

        print(f"DEBUG: You selected [{choice}]")

        if choice == "1":
            EnterOrUpdateUserData()

        elif choice == "2":
            ChangeUnits()

        elif choice == "3":
            RecordActivity()

        elif choice == "4":
            print("\nOpening Basic Activity Log...")
            ViewBASICActivityLog()

        elif choice == "5":
            print("\nOpening Extended Activity Log...")
            ViewEXTENDEDActivityLog()

        elif choice == "6":
            AddNewActivity()

        elif choice == "7":
            VerifyWithWebServices()

        elif choice == "8":
            print("\nGoodbye.")
            break
        elif choice == "9":
            print("\nConvert all previous records")
            print("1. Convert everything to KG")
            print("2. Convert everything to LBS")
            unitChoice = input("Enter choice: ").strip()
            
            if unitChoice == "1":
                data.ConvertAllRecordsToNewUnits("KG")
            elif unitChoice == "2":
                data.ConvertAllRecordsToNewUnits("LBS")
            else:
                print("Invalid choice.")

        else:
            print(
                "\nThis is not a valid menu choice."
            )

# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    InitialiseUserData()
    if login.LoginUser():
        RunProgram()