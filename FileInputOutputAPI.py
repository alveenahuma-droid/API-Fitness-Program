from pathlib import Path

DATA_FILE = Path("ExerciseData.txt")

DEFAULT_DATA = """START_HEIGHT,START_WEIGHT,START_BMI,UNITS
2.0,100.0,25.0,KG
ACTIVITY,DURATION,CALORIES_BURNED,WEIGHT_LOST,UNITS
Yoga,30,125.0,0.02,KG
Cycling,30,375.0,0.05,KG"""

def EnsureDataFile():

    if not DATA_FILE.exists():

        DATA_FILE.write_text(
            DEFAULT_DATA,
            encoding="utf-8"
        )

def InsertNewUserData(
        height,
        weight,
        BMI,
        units):

    EnsureDataFile()

    contents = DATA_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    if len(contents) < 3:

        raise ValueError(
            "ExerciseData.txt does not contain "
            "the expected headers."
        )

    contents[1] = (
        f"{height},{weight},{BMI},{units}"
    )

    DATA_FILE.write_text(
        "\n".join(contents),
        encoding="utf-8"
    )


def AddNewActivityRecord(
        activity,
        duration,
        calories,
        weightLost,
        units):

    EnsureDataFile()

    with DATA_FILE.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n{activity},"
            f"{duration},"
            f"{calories},"
            f"{weightLost},"
            f"{units}"
        )


def LoadDefaultData():

    EnsureDataFile()

    contents = DATA_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    if len(contents) < 2:

        raise ValueError(
            "ExerciseData.txt does not "
            "contain starting user data."
        )

    return contents[1].split(",")


def LoadAllFileData():

    EnsureDataFile()

    return DATA_FILE.read_text(
        encoding="utf-8"
    ).splitlines()