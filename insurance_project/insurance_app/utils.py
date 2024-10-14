from .constants import AGE_MULTIPLIERS, DEFAULT_MULTIPLIER

def get_multiplier_for_age(age):
    for age_range, multiplier in AGE_MULTIPLIERS.items():
        if age_range[0] <= age <= age_range[1]:
            return multiplier
    return DEFAULT_MULTIPLIER # Return default if no range matches