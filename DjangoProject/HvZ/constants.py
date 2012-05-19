"""Store your constants here!

All constants should be in ALL_CAPS, since they'll probably be
*-imported and might pollute the namespace otherwise.

Also, _TT means it's the two-tuple version used in the choices field.

"""

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

LOCATION_LEGEND = {
        "S": "Start",
        "T": "Do task at",
        "F": "Find something at",
        "G": "Go to",
        "E": "Escort to",
        "R": "Respawn",
        "C": "Complete mission"
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

TIMES = {
    "E":"Early Morning (Before 8 AM)",
    "M":"Morning (8-11 AM)",
    "L":"Lunch (11 AM-1 PM)",
    "A":"Afternoon (1-3 PM)",
    "B":"Before Dinner (3-5 PM)",
    "D":"Dinner (5-7 PM)",
    "I":"Mission (7-10 PM)",
}

TIMES_TT = (
    ("E","Early Morning (Before 8 AM)"),
    ("M","Morning (8-11 AM)"),
    ("L","Lunch (11 AM-1 PM)"),
    ("A","Afternoon (1-3 PM)"),
    ("B","Before Dinner (3-5 PM)"),
    ("D","Dinner (5-7 PM)"),
    ("I","Mission (7-9 PM)"),
)

VICTORY = {
    "N":  "Not Over",
    "HF": "Human Full",
    "HP": "Human Partial",
    "D":  "Draw",
    "ZP": "Zombie Partial",
    "ZF": "Zombie Full",
}

VICTORY_TT = (
    ("N","Not Over"),
    ("HF","Human Full"),
    ("HP","Human Partial"),
    ("D","Draw"),
    ("ZP","Zombie Partial"),
    ("ZF","Zombie Full"),
)

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
