from email_validator import validate_email, EmailNotValidError


def is_email_valid(email):
    try:
        v = validate_email(email)
        return v.normalized.lower()
    except EmailNotValidError as e:
        raise EmailNotValidError(f'Email format is not correct: {e}')
