"""Store your constants here!

All constants should be in ALL_CAPS, since they'll probably be
*-imported and might pollute the namespace otherwise.

Also, _TT means it's the two-tuple version used in the choices field.

"""

#Building Legend is a list of building types. It's used for identifying buildings in the Buildings model.
BUILDING_LEGEND = {
    "C": "Academic building",
    "T": "Athletic field, building, or area",
    "D": "Dormitory",
    "I": "Dining hall",
    "L": "Landmark or notable feature",
    "O": "Other building"
}

BUILDING_LEGEND_TT =  (
    ("C","Academic Building"),
    ("T","Athletic field, building, or area"),
    ("D","Dormitory"),
    ("I","Dining Hall"),
    ("L","Landmark or notable feature"),
    ("O","Other building"),
)

#Class year is what year your standing is in college. It is used for identifying characters. It is repeated in players as a guideline.
CLASS_YEAR = {
    "F": "Froshling",
    "O": "Sophomore",
    "J": "Junior",
    "N": "Senior",
    "U": "Super Senior",
    "A": "Alum"
}

CLASS_YEAR_TT = (
    ("F","Froshling"),
    ("O","Sophomore"),
    ("J","Junior"),
    ("N","Senior"),
    ("U","Super Senior"),
    ("A","Alum")
)

#Days is a 0-indexed list of days that game events occur on. It is most important in missions where we refer to Tuesday as day 1.
DAYS = ["Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
]

DAYS_TT = (
    (0,"Monday"),
    (1,"Tuesday"),
    (2,"Wednesday"),
    (3,"Thursday"),
    (4,"Friday"),
    (5,"Saturday"),
)

#Location legend is a list of tasks that can be completed at a point on a mission. It is used in the missionpoint model.
LOCATION_LEGEND = {
        "S": "Start at",
        "T": "Do task at",
        "F": "Find something at",
        "G": "Go to",
        "E": "Escort to",
        "R": "Respawn at",
        "C": "Complete mission at"
}

LOCATION_LEGEND_TT = (
    ("S","Start"),
    ("T","Do task at"),
    ("F","Find something at"),
    ("G","Go to"),
    ("E","Escort to"),
    ("R","Respawn"),
    ("C","Complete Mission")
)

#Mission legend is a list of the varieties of different missions. X is used for NPC so it comes alphabetically after Night.
MISSION_LEGEND = {
    "D": "Day",
    "T": "Night",
    "X": "NPC",
    "Y": "Legendary",
}

MISSION_LEGEND_TT = (
    ("D","Day"),
    ("N","Night"),
    ("X","NPC"),
    ("Y","Legendary"),
)

#Time format is the standard time format used on most of the site. An example is Tue 9:22 PM.
TIME_FORMAT = "%a %I:%M %p"

#Times are rough categorizations of the time. For now they are only used in specifying when you will be in class. In the future it could be used for multipart missions or graphs.
TIMES = {
    "E":"Early Morning (6-8 AM)",
    "M":"Morning (8-11 AM)",
    "L":"Lunch (11 AM-1 PM)",
    "A":"Afternoon (1-3 PM)",
    "B":"Before Dinner (3-5 PM)",
    "D":"Dinner (5-7 PM)",
    "I":"Mission (7-10 PM)",
    "N":"Night (10 PM-6 AM)", 
}

TIMES_TT = (
    ("E","Early Morning (6-8 AM)"),
    ("M","Morning (8-11 AM)"),
    ("L","Lunch (11 AM-1 PM)"),
    ("A","Afternoon (1-3 PM)"),
    ("B","Before Dinner (3-5 PM)"),
    ("D","Dinner (5-7 PM)"),
    ("I","Mission (7-10 PM)"),
    ("N","Night (10 PM-6 AM)"),
)

#Victory is the outcome of the mission. It is used in missions.
VICTORY = {
    "N":  "Not Over",
    "HF": "Human Full",
    "HP": "Human Partial",
    "D":  "Draw",
    "ZP": "Zombie Partial",
    "ZF": "Zombie Full",
}

#Victory order is a number associated with the outcome of the mission. It is used because we want people to be able to sort by who won/to what degree.
VICTORY_ORDER = {
    "N":  0,
    "HF": 1,
    "HP": 2,
    "D":  3,
    "ZP": 4,
    "ZF": 5,
}

VICTORY_TT = (
    ("N","Not Over"),
    ("HF","Human Full"),
    ("HP","Human Partial"),
    ("D","Draw"),
    ("ZP","Zombie Partial"),
    ("ZF","Zombie Full"),
)

#Visibility is who can see something. It is used all over the place for missions, profile fields, plot stuff, and forum threads
VISIBILITY = {
    "M": "Moderators Only",
    "B": "Both Teams",
    "H": "Humans Only",
    "Z": "Zombies Only",
}

VISIBILITY_TT = (
    ("M","Moderators Only"),
    ("B","Both Teams"),
    ("H","Humans Only"),
    ("Z","Zombies Only")
)
