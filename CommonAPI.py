import os
import re
import requests
import Config as con
from dotenv import load_dotenv


load_dotenv()


PoundToKiloRatio = 2.2
CaloriesInAKilo = 7700


API_NINJAS_URL = (
    "https://" +
    "api.api-ninjas.com/v1/unitconversion"
)

BMI_API_URL = (
    "https://" +
    "healthcalcshub.com/api/v1/bmi"
)

# UNIT CONVERSION

def KilosToPounds(weightInKilos):

    return round(
        weightInKilos * PoundToKiloRatio,
        2
    )


def PoundsToKilos(weightInPounds):

    return round(
        weightInPounds / PoundToKiloRatio,
        2
    )


# BMI


def BMICalculator(
        weightInKilos,
        height):

    if weightInKilos <= 0 or height <= 0:

        raise ValueError(
            "Weight and height must be "
            "greater than zero."
        )

    return round(
        weightInKilos /
        (height * height),
        2
    )


def BMICalculatorWeightInPounds(
        weightInPounds,
        height):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    return BMICalculator(
        weightInKilos,
        height
    )


# --------------------------------------------------
# WEB API - KG TO POUNDS
# --------------------------------------------------

def KilosToPoundsWebService(
        weightInKilos):

    apiKey = os.getenv(
        "API_NINJAS_KEY"
    )

    if not apiKey:

        return None

    try:

        response = requests.get(

            API_NINJAS_URL,

            params={
                "amount": weightInKilos,
                "unit": "kilogram"
            },

            headers={
                "X-Api-Key": apiKey
            },

            timeout=10
        )

        response.raise_for_status()

        apiData = response.json()

        return round(
            float(
                apiData["conversions"]["pound"]
            ),
            2
        )

    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError
    ):

        return None


# --------------------------------------------------
# WEB API - POUNDS TO KG
# --------------------------------------------------

def PoundsToKilosWebService(
        weightInPounds):

    apiKey = os.getenv(
        "API_NINJAS_KEY"
    )

    if not apiKey:

        return None

    try:

        response = requests.get(

            API_NINJAS_URL,

            params={
                "amount": weightInPounds,
                "unit": "pound"
            },

            headers={
                "X-Api-Key": apiKey
            },

            timeout=10
        )

        response.raise_for_status()

        apiData = response.json()

        return round(
            float(
                apiData["conversions"]["kilogram"]
            ),
            2
        )

    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError
    ):

        return None


# --------------------------------------------------
# WEB API - BMI
# --------------------------------------------------

def BMICalculatorWebService(
        weightInKilos,
        heightInMetres):

    try:

        response = requests.get(

            BMI_API_URL,

            params={
                "weight": weightInKilos,
                "height":
                    heightInMetres * 100,
                "unit": "metric",
                "lang": "en"
            },

            timeout=10
        )

        response.raise_for_status()

        apiData = response.json()

        return round(
            float(
                apiData["result"]["bmi"]
            ),
            2
        )

    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError
    ):

        return None


# --------------------------------------------------
# CALORIES - KG
# --------------------------------------------------

def CaloriesBurnedIn60Minutes(
        METvalue,
        weightInKilos):

    return (
        METvalue *
        weightInKilos
    )


def CaloriesBurnedIn30Minutes(
        METvalue,
        weightInKilos):

    return (
        CaloriesBurnedIn60Minutes(
            METvalue,
            weightInKilos
        ) / 2
    )


def CaloriesBurnedIn15Minutes(
        METvalue,
        weightInKilos):

    return (
        CaloriesBurnedIn60Minutes(
            METvalue,
            weightInKilos
        ) / 4
    )


def CaloriesBurnedInCustomTime(
        METvalue,
        weightInKilos,
        interval):

    if interval <= 0:

        raise ValueError(
            "Activity duration must be "
            "greater than zero."
        )

    caloriesPerHour = (
        CaloriesBurnedIn60Minutes(
            METvalue,
            weightInKilos
        )
    )

    return (
        caloriesPerHour *
        (interval / 60)
    )


# --------------------------------------------------
# WEIGHT LOSS - KG
# --------------------------------------------------

def WeightLostInKilosIn15Minutes(
        METValue,
        weightInKilos):

    calories = (
        CaloriesBurnedIn15Minutes(
            METValue,
            weightInKilos
        )
    )

    return (
        calories /
        CaloriesInAKilo
    )


def WeightLostInKilosIn30Minutes(
        METValue,
        weightInKilos):

    calories = (
        CaloriesBurnedIn30Minutes(
            METValue,
            weightInKilos
        )
    )

    return (
        calories /
        CaloriesInAKilo
    )


def WeightLostInKilosIn60Minutes(
        METValue,
        weightInKilos):

    calories = (
        CaloriesBurnedIn60Minutes(
            METValue,
            weightInKilos
        )
    )

    return (
        calories /
        CaloriesInAKilo
    )


def WeightLostInKilosCustomTime(
        METValue,
        weightInKilos,
        interval):

    calories = (
        CaloriesBurnedInCustomTime(
            METValue,
            weightInKilos,
            interval
        )
    )

    return (
        calories /
        CaloriesInAKilo
    )


# --------------------------------------------------
# CALORIES - POUNDS
# --------------------------------------------------

def CaloriesBurnedIn15MinutesLb(
        METvalue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    return CaloriesBurnedIn15Minutes(
        METvalue,
        weightInKilos
    )


def CaloriesBurnedIn30MinutesLb(
        METvalue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    return CaloriesBurnedIn30Minutes(
        METvalue,
        weightInKilos
    )


def CaloriesBurnedIn60MinutesLb(
        METvalue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    return CaloriesBurnedIn60Minutes(
        METvalue,
        weightInKilos
    )


def CaloriesBurnedInCustomTimeLb(
        METvalue,
        weightInPounds,
        interval):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    return CaloriesBurnedInCustomTime(
        METvalue,
        weightInKilos,
        interval
    )


# --------------------------------------------------
# WEIGHT LOSS - POUNDS
# --------------------------------------------------

def WeightLostInPoundsIn15Minutes(
        METValue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    lostKg = (
        WeightLostInKilosIn15Minutes(
            METValue,
            weightInKilos
        )
    )

    return KilosToPounds(
        lostKg
    )


def WeightLostInPoundsIn30Minutes(
        METValue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    lostKg = (
        WeightLostInKilosIn30Minutes(
            METValue,
            weightInKilos
        )
    )

    return KilosToPounds(
        lostKg
    )


def WeightLostInPoundsIn60Minutes(
        METValue,
        weightInPounds):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    lostKg = (
        WeightLostInKilosIn60Minutes(
            METValue,
            weightInKilos
        )
    )

    return KilosToPounds(
        lostKg
    )


def WeightLostInPoundsInCustomTime(
        METValue,
        weightInPounds,
        interval):

    weightInKilos = PoundsToKilos(
        weightInPounds
    )

    lostKg = (
        WeightLostInKilosCustomTime(
            METValue,
            weightInKilos,
            interval
        )
    )

    return KilosToPounds(
        lostKg
    )
    

# Calculates weight lost in kilos for a custom number of minutes
def WeightLostInKilosCustomTime(METValue, weightInKilos, interval):
    calories = CaloriesBurnedInCustomTime(METValue, weightInKilos, interval)
    weightLost = calories / CaloriesInAKilo
    return round(weightLost, 4)

# This function uses a website to convert kilograms to pounds
def KilosToPoundsWebService(weightInKilos):
    
    try:
        # Create the web address (1 kg = 2.2 pounds)
        url = "https://api.mathjs.org/v4/?expr=" + str(weightInKilos) + "*2.2"
        
        # Send request to the website
        response = requests.get(url)
        
        # Check if the request worked
        if response.status_code == 200:
            answer = float(response.text)
            return round(answer, 2)
        else:
            print("Error: Could not get data from website")
            return None
            
    except:
        print("Error: No internet connection or website not working")
        return None