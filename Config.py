#-------------------------------------------------------------------------------------
# Module that contains all global variables required through the application
#-------------------------------------------------------------------------------------

startHeight = 0 #the starting height of the individual user
startWeight = 0 #the starting weight of the individual user
startBMI = 0 #the starting Body Mass Index of the individual user
duration = 30 #the default length of the activity in minutes
units = "KG" #the units that the program will be set to
# A starting list of activities.
ListOfActivities = [{"Activity":"Cycling", "METvalue":7.5},
{"Activity":"Circuits", "METvalue":4.3},
{"Activity":"Weights", "METvalue":5},
{"Activity":"Rowing", "METvalue":12},
{"Activity":"Yoga", "METvalue":2.5},
{"Activity":"Aerobics", "METvalue":9.5},
{"Activity":"Running", "METvalue":8}]