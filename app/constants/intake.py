ENHANCEMENT = "Enhancement"
NEW_PROJECT = "New Project"
LEGACY = "Replacement of Legacy System"

PROJECT_TYPE = [
    ("", ""),
    (NEW_PROJECT, NEW_PROJECT),
    (ENHANCEMENT, ENHANCEMENT),
    (LEGACY, LEGACY),
]

CRITICAL = "Critical"
HIGH = "High"
MEDIUM = "Medium"
LOW = "Low"

PRIORITY = [("", ""), (LOW, LOW), (MEDIUM, MEDIUM), (HIGH, HIGH), (CRITICAL, CRITICAL)]

INTERNAL = "DORIS Only"
CITYNET = "Multi-Agency"
PUBLIC = "Public"

PROJECT_ACCESS = [("", ""), (INTERNAL, INTERNAL), (CITYNET, CITYNET), (PUBLIC, PUBLIC)]

YES = "Yes"
NO = "No"
YES_NO = [("", ""), (YES, YES), (NO, NO)]
