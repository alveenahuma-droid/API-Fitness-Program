import Config as con
import CommonAPI as common
import FileInputOutputAPI as fileIO


# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

def ValidateNumberInput():

    try:

        return int(
            input()
        )

    except ValueError:

        print(
            "\nThis is not a valid whole number. "
            "Please try again."
        )

        return -1


def GetPositiveFloat(prompt):

    while True:

        try:

            value = float(
                input(prompt)
            )

            if value <= 0:

                print(
                    "Please enter a value "
                    "greater than zero."
                )

                continue

            return value

        except ValueError:

            print(
                "Please enter a valid number."
            )


def GetPositiveInt(prompt):

    while True:

        try:

            value = int(
                input(prompt)
            )

            if value <= 0:

                print(
                    "Please enter a whole number "
                    "greater than zero."
                )

                continue

            return value

        except ValueError:

            print(
                "Please enter a valid whole number."
            )


# --------------------------------------------------
# ACTIVITY INPUT
# --------------------------------------------------

def GetMetValueForActivity(search):

    for activity in con.ListOfActivities:

        if (
            activity["Activity"].lower()
            ==
            search.lower()
        ):

            return activity["METvalue"]

    return None


def GetStartHeight():

    con.startHeight = GetPositiveFloat(
        "Please enter your starting "
        "height in metres: "
    )

    return con.startHeight


def GetStartWeight():

    con.startWeight = GetPositiveFloat(
        f"Please enter your starting "
        f"weight in {con.units}: "
    )

    return con.startWeight


def GetActivity():

    while True:

        search = input(
            "\nPlease enter the activity name: "
        ).strip()

        if (
            GetMetValueForActivity(search)
            is not None
        ):

            return search

        print(
            "Activity not found. "
            "Please choose an activity "
            "from the list."
        )


# --------------------------------------------------
# UNIT SELECTION
# --------------------------------------------------

def GetUnits():

    while True:

        print("\nSelect the weight unit:")
        print("1. Kilograms (KG)")
        print("2. Pounds (LBS)")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            return "KG"

        if choice == "2":

            return "LBS"

        print(
            "Invalid selection. "
            "Please enter 1 or 2."
        )


# --------------------------------------------------
# ACTIVITY DURATION
# --------------------------------------------------

def Record15MinActivity():

    return 15


def Record60MinActivity():

    return 60


def RecordCustomActivity():

    return GetPositiveInt(
        "Enter the custom activity "
        "duration in minutes: "
    )


def GetActivityDuration():

    while True:

        print("\nSelect activity duration:")

        print("1. 15 minutes")
        print("2. 30 minutes")
        print("3. 60 minutes")
        print("4. Custom duration")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            return Record15MinActivity()

        if choice == "2":

            return 30

        if choice == "3":

            return Record60MinActivity()

        if choice == "4":

            return RecordCustomActivity()

        print(
            "Invalid selection. "
            "Please enter 1, 2, 3 or 4."
        )


# --------------------------------------------------
# DISPLAY ACTIVITIES
# --------------------------------------------------

def ViewActivityList():

    print(
        "\nACTIVITY\tMET VALUE"
    )

    print(
        "-" * 28
    )

    for activity in con.ListOfActivities:

        print(
            f'{activity["Activity"]:<12}\t'
            f'{activity["METvalue"]}'
        )


# --------------------------------------------------
# DISPLAY STARTING DATA
# --------------------------------------------------

def ViewStartingData():

    fileData = (
        fileIO.LoadAllFileData()
    )

    if len(fileData) < 2:

        return

    header = (
        fileData[0].split(",")
    )

    values = (
        fileData[1].split(",")
    )

    print()

    print(
        " | ".join(header)
    )

    print(
        " | ".join(values)
    )


# --------------------------------------------------
# ACTIVITY LOG
# --------------------------------------------------

def DisplayActivityLogHeader(
        fileData):

    if len(fileData) >= 3:

        print(
            "\n" +
            " | ".join(
                fileData[2].split(",")
            )
        )


def DisplayActivityLogData(
        fileData):

    if len(fileData) <= 3:

        print(
            "No activity records are available."
        )

        return

    for line in fileData[3:]:

        if line.strip():

            print(
                " | ".join(
                    line.split(",")
                )
            )


# --------------------------------------------------
# INTERNAL RECORD CONVERSION
# --------------------------------------------------

def _activity_records(
        fileData):

    records = []

    for line in fileData[3:]:

        if not line.strip():

            continue

        parts = line.split(",")

        if len(parts) != 5:

            continue

        try:

            records.append(
                {
                    "activity":
                        parts[0],

                    "duration":
                        int(parts[1]),

                    "calories":
                        float(parts[2]),

                    "weight_loss":
                        float(parts[3]),

                    "units":
                        parts[4].upper()
                }
            )

        except ValueError:

            continue

    return records


# --------------------------------------------------
# TOTAL DURATION
# --------------------------------------------------

def CalculateTotalActvityDuration(
        fileData):

    return sum(
        record["duration"]
        for record
        in _activity_records(fileData)
    )


# --------------------------------------------------
# TOTAL CALORIES
# --------------------------------------------------

def CalculateTotalCaloriesBurned(
        fileData):

    return round(
        sum(
            record["calories"]
            for record
            in _activity_records(fileData)
        ),
        2
    )


# --------------------------------------------------
# TOTAL WEIGHT LOSS
# --------------------------------------------------

def CalculateTotalWeightLoss(
        fileData,
        targetUnits="KG"):

    totalKg = 0.0

    for record in _activity_records(
        fileData
    ):

        if record["units"] == "LBS":

            totalKg += (
                common.PoundsToKilos(
                    record["weight_loss"]
                )
            )

        else:

            totalKg += (
                record["weight_loss"]
            )

    if targetUnits.upper() == "LBS":

        return round(
            common.KilosToPounds(
                totalKg
            ),
            2
        )

    return round(
        totalKg,
        2
    )


# --------------------------------------------------
# AVERAGE CALORIES
# --------------------------------------------------

def CalculateAverageCalories(
        fileData):

    records = _activity_records(
        fileData
    )

    if not records:

        return 0.0

    total = sum(
        record["calories"]
        for record in records
    )

    return round(
        total / len(records),
        2
    )


# --------------------------------------------------
# BIGGEST CALORIE BURN
# --------------------------------------------------

def CalculateBiggestCalorieBurn(
        fileData):

    records = _activity_records(
        fileData
    )

    if not records:

        return 0.0

    return round(
        max(
            record["calories"]
            for record in records
        ),
        2
    )


# --------------------------------------------------
# BIGGEST WEIGHT LOSS
# --------------------------------------------------

def CalculateBiggestWeightLossInterval(
        fileData,
        targetUnits="KG"):

    records = _activity_records(
        fileData
    )

    if not records:

        return 0.0

    lossesKg = []

    for record in records:

        if record["units"] == "LBS":

            lossesKg.append(
                common.PoundsToKilos(
                    record["weight_loss"]
                )
            )

        else:

            lossesKg.append(
                record["weight_loss"]
            )

    biggestKg = max(
        lossesKg
    )

    if targetUnits.upper() == "LBS":

        return round(
            common.KilosToPounds(
                biggestKg
            ),
            2
        )

    return round(
        biggestKg,
        2
    )


# --------------------------------------------------
# ADD NEW ACTIVITY
# --------------------------------------------------

def AddActivityToList(
        activityName,
        metValue):

    activityName = (
        activityName.strip()
    )

    if not activityName:

        return (
            False,
            "Activity name cannot be empty."
        )

    if metValue <= 0:

        return (
            False,
            "MET value must be greater than zero."
        )

    for activity in con.ListOfActivities:

        if (
            activity["Activity"].lower()
            ==
            activityName.lower()
        ):

            return (
                False,
                "That activity already exists."
            )

    con.ListOfActivities.append(
        {
            "Activity":
                activityName.title(),

            "METvalue":
                float(metValue)
        }
    )

    return (
        True,
        f"{activityName.title()} "
        f"added successfully."
    )


# Converts all activity records in the file to the selected units
def ConvertAllRecordsToNewUnits(newUnits):
    
    try:
        with open("ExerciseData.txt", "r") as f:
            lines = f.readlines()
    except:
        print("Could not open the data file.")
        return
    
    if len(lines) < 4:
        print("No activity records found to convert.")
        return
    
    newLines = []
    newLines.append(lines[0])  # header
    newLines.append(lines[1])  # starting data
    newLines.append(lines[2])  # activity header
    
    for line in lines[3:]:
        if line.strip() == "":
            continue
            
        parts = line.strip().split(",")
        
        if len(parts) != 5:
            newLines.append(line)
            continue
        
        activity = parts[0]
        duration = parts[1]
        calories = parts[2]
        weightLoss = float(parts[3])
        currentUnits = parts[4].upper()
        
        if currentUnits != newUnits:
            if newUnits == "LBS":
                weightLoss = round(weightLoss * 2.2, 4)
            else:
                weightLoss = round(weightLoss / 2.2, 4)
        
        newLine = f"{activity},{duration},{calories},{weightLoss},{newUnits}\n"
        newLines.append(newLine)
    
    try:
        with open("ExerciseData.txt", "w") as f:
            f.writelines(newLines)
        print("All activity records have been converted to", newUnits)
    except:
        print("Error while saving the file.")