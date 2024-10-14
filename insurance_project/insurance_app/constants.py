# constants.py

# Status constants for quotes/policies
POLICY_STATUS_NEW = 'NEW'
POLICY_STATUS_QUOTED = 'QUOTED'
POLICY_STATUS_LIVE = 'LIVE'

# Choices tuple for use in models (if required)
POLICY_STATUS_CHOICES = [
    (POLICY_STATUS_NEW, 'New'),
    (POLICY_STATUS_QUOTED, 'Quoted'),
    (POLICY_STATUS_LIVE, 'Live'),
]

# Insurance types constants
PERSONAL_ACCIDENT = 'personal-accident'
HEALTH_INSURANCE = 'health-insurance'
LIFE_INSURANCE = 'life-insurance'
HOME_INSURANCE = 'home-insurance'
AUTO_INSURANCE = 'auto-insurance'

# Choices tuple for insurance types
INSURANCE_TYPES = [
    (PERSONAL_ACCIDENT, 'Personal Accident'),
    (HEALTH_INSURANCE, 'Health Insurance'),
    (LIFE_INSURANCE, 'Life Insurance'),
    (HOME_INSURANCE, 'Home Insurance'),
    (AUTO_INSURANCE, 'Auto Insurance'),
]

DEFAULT_MULTIPLIER = 1.0

AGE_MULTIPLIERS = {
    (0, 18): 0.7,  # For ages between 0 and 18
    (19, 30): 0.8,  # For ages between 19 and 30
    (31, 50): DEFAULT_MULTIPLIER,  # For ages between 31 and 50
    (51, 65): 1.2,  # For ages between 51 and 65
    (66, 100): 1.5  # For ages between 66 and 100
}

QUOTE_NOT_PAID_ERROR = 'Quote cannot be paid as it is not in QUOTED status.'
STATUS_NOT_ACTIVE_ERROR = 'Invalid status. Status must be "active".'
FUTURE_DOB_ERROR = 'Date of birth cannot be in the future.'
INVALID_CUSTOMER_OR_POLICY_ERROR = 'Invalid customer or policy type.'
STATUS_NOT_ACCEPTED_ERROR = 'Invalid status. Status must be "accepted".'
QUOTE_NOT_FOUND = 'Quote not found.'
QUOTE_NOT_NEW_ERROR = 'Quote cannot be accepted as it is not in NEW status.'
CUSTOMER_ID_NOT_FOUND = 'customer_id not found.'
CUSTOMER_NOT_FOUND = 'customer not found.'
INVALID_DOB_DATE_FORMAT = 'Invalid date format. Use DD-MM-YYYY.'
