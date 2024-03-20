# Define password requirements here
has_uppercase = False       
has_lowercase = False
has_letter = True           # Set to False when either has_uppercase or has_lowercase is True
has_digit = True
has_min_length = True
has_special_chars = False
min_length = 8
special_chars = '@#$%^&+=!*'

def get_password_pattern() -> str:
    """ Returns a regular expression based on requirements set """
    start_pattern = '^'
    end_pattern = '.*$'
    letter_pattern = '(?=.*[a-zA-Z])'
    uppercase_pattern = '(?=.*[A-Z])' if has_uppercase and not has_letter else ''
    lowercase_pattern = '(?=.*[a-z])' if has_lowercase and not has_letter else ''
    digit_pattern = '(?=.*\d)' if has_digit else ''
    special_char_pattern = f'(?=.*[{special_chars}])' if has_special_chars else ''
    length_pattern  = f'.{{{min_length},}}' if has_min_length else ''

    pattern = fr'{start_pattern}{letter_pattern}{uppercase_pattern}{lowercase_pattern}{digit_pattern}{special_char_pattern}{length_pattern}{end_pattern}'

    return pattern

def get_password_help_text() -> str:
    help_text = 'Password must contain '

    if has_letter:
        help_text += 'one letter, '
    else:
        if has_uppercase:
            help_text += 'one uppercase letter, '
        if has_lowercase:
            help_text += 'one lowercase letter, '
        
        if has_digit:
            help_text += 'one digit, '

        if has_special_chars:
            help_text += 'one special character, '

        if has_min_length:
            help_text += f'and must be at least {min_length} characters, '

        return help_text[:-2]

def get_validation_indicators() -> list:
    indicators = []

    if has_letter:
        indicators.append(
            {
                "message": "Must have at least one letter",
                "condition": "hasLetter"
            }
        )
    else:
        if has_uppercase:
            indicators.append(
                {
                    "message": "Must have at least one uppercase letter",
                    "condition": "hasUpperCase"
                }
            )
        
        if has_lowercase:
            indicators.append(
                {
                    "message": "Must have at least one lowercase letter",
                    "condition": "hasLowerCase"
                }
            )

    if has_digit:
        indicators.append(
            {
                "message": "Must have at least one digit",
                "condition": "hasDigit"
            }
        )

    if has_special_chars:
        indicators.append(
            {
                "message": f"Must have at least one special character from {special_chars}",
                "condition": "hasSpecialCharacter"
            }
        )

    if has_min_length:
        indicators.append(
            {
                "message": f"Must be at least {min_length} characters long",
                "condition": "hasLength"
            }
        )

    return indicators

