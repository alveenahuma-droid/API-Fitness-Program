import time
from functools import wraps
#-------------------------------------------------------------------------------------
#Module that contains basic functionality for logging a user in to the application
#-------------------------------------------------------------------------------------
#a basic list of users stored in a dictionary.
#each entry is a KEY:VALUE pair of UserName keys and Password keys.
ListOfUsers = [{"UserName":"TEST", "Password":"TEST01"},
{"UserName":"TEST2", "Password":"TEST02"},
{"UserName":"TEST3", "Password":"TEST03"}]
#This is the main login function.
#The function will make sure that a username has been entered. If not, a user will be prompted for another go.
#It will then be checked against the usernames in the dictionary.
#If the username does not exist, the user will be prompted for another go. There are no limits on this checking.
#If a username does exist,the function will make sure that a password has been entered.
#If not, a user will be prompted for #another go.
#The username and password combination will then be checked against the KEY:VALUE paird in the dictionary.
#If the supplied combination does not exist, the user will be prompted for another password entry.
#There are no limits on this checking.
#RETURNS TRUE if the all login criteria are met.
def LoginUser():
    userName = ""
    password = ""
    loginSuccessful = False
    while not loginSuccessful:
        userName = input("Please enter a user name: ")
        if userName == "":
            print("\nYou have not entered a user name.\nPlease try again.\n")
        else:
            loginSuccessful = CheckUsernameExists(userName)
            if not loginSuccessful:
                print("\nUser Name not found.\nPlease try again.\n")
    loginSuccessful = False
    while not loginSuccessful:
        password = input("Please enter a password: ")
        if password == "":
            print("\nYou have not entered a password.\nPlease try again.\n")
        else:
            loginSuccessful = CheckPasswordMatchesUserName(userName, password)
            if not loginSuccessful:
                print("Password is incorrect.\nPlease try again.\n")
    return loginSuccessful
#function to see if the supplied username exists in the dictionary.
#RETURNS TRUE if the username exists.
def CheckUsernameExists(inputUserName):
    userNameExists = False
    for user in ListOfUsers:
        if user.get("UserName").lower() == inputUserName.lower():
            userNameExists = True
            break
    return userNameExists
#function to check that the supplied username and password pair match.
#RETURNS TRUE if they do.

def CheckPasswordMatchesUserName(inputUserName, inputPassword):
    passwordMatches = False
    for user in ListOfUsers:
        if user.get("UserName") == inputUserName and user.get("Password") == inputPassword:
            passwordMatches = True
            break
    return passwordMatches

#function to check that the supplied username and password pair match.
#RETURNS TRUE if they do.

def CheckPasswordMatchesUserName(inputUserName, inputPassword):
    passwordMatches = False
    for user in ListOfUsers:
        if user.get("UserName") == inputUserName and user.get("Password") == inputPassword:
            passwordMatches = True
            break
    return passwordMatches

# Note: this code has been copied from StackOverflow
def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"\n{time.time() - start_time:.2f} seconds elapsed")
        return result
    return inner


#Login Attempts function that allows a user to attempt to login 3 times before being denied access.
@timer
def LoginAttempts():
    attempts = 0
    maxAttempts = 3

    while attempts < maxAttempts:
        userName = input("Please enter a user name: ")

        if userName == "":
            print("\nYou have not entered a user name.\nPlease try again.\n")
            attempts += 1
            continue

        if not CheckUsernameExists(userName):
            print("\nUser Name not found.\nPlease try again.\n")
            attempts += 1
            continue

        password = input("Please enter a password: ")

        if password == "":
            print("\nYou have not entered a password.\nPlease try again.\n")
            attempts += 1
            continue

        if CheckPasswordMatchesUserName(userName, password):
            return True

        attempts += 1
        print("\nPassword is incorrect.\nPlease try again.\n")

        if attempts < maxAttempts:
            time.sleep(10)

    print("\nLogin failed. You have exceeded the maximum number of attempts.")
    return False

def AttemptLogin(username, password):
    """
    Called by matrix_gui.py
    Returns: (success, message, correct_username)
    """
    username = username.strip()

    if username == "":
        return False, "You have not entered a user name", None

    if not CheckUsernameExists(username):
        return False, "User Name not found", None

    # Get the exact stored username (fixes case sensitivity)
    correct_username = None
    for user in ListOfUsers:
        if user.get("UserName").lower() == username.lower():
            correct_username = user.get("UserName")
            break

    if password == "":
        return False, "You have not entered a password", None

    if CheckPasswordMatchesUserName(correct_username, password):
        return True, "Login successful", correct_username
    else:
        return False, "Password is incorrect", None


if __name__ == "__main__":
    LoginAttempts()
 