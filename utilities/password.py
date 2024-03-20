# Define password requirements here
has_uppercase = False       
has_lowercase = False
has_letter = True           # Set to False when either has_uppercase or has_lowercase is True
has_digit = False
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
        help_text += 'at least one letter, '

        if has_digit:
            help_text += 'at least one digit, '

        if has_special_chars:
            help_text += 'at least one special character, '

        if has_min_length:
            help_text += f'and must be at least {min_length} characters, '
    else:
        if has_uppercase:
            help_text += 'at least one uppercase letter, '
        if has_lowercase:
            help_text += 'at least one lowercase letter, '
        
        if has_digit:
            help_text += 'at least one digit, '

        if has_special_chars:
            help_text += 'at least one special character, '

        if has_min_length:
            help_text += f'and must be at least {min_length} characters, '

    return help_text[:-2]
