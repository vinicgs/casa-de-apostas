import re

def validate_contact_info(emails_str, phones_str):
    if emails_str:
        for email in emails_str.split(','):
            email = email.strip()
            if email and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                return False, f"O e-mail '{email}' é inválido."
    if phones_str:
        for phone in phones_str.split(','):
            phone = phone.strip()
            digits = re.sub(r'\D', '', phone)
            if phone and len(digits) < 8:
                return False, f"O telefone '{phone}' é muito curto para ser válido."
    return True, ""
