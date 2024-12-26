from email_validator import validate_email, EmailNotValidError


def validate_and_normalize_email(email: str) -> str:
    """
    :param email: The email address to be validated and normalized.
    :type email: str
    :return: The validated and normalized email address in lowercase format.
    :rtype: str
    :raises EmailNotValidError: If the provided email address is not valid.
    """
    try:
        validated_email = validate_email(email).normalized
        normalized_email = validated_email.lower()
        return normalized_email
    except EmailNotValidError as e:
        raise EmailNotValidError(f'Invalid email: {e}')
