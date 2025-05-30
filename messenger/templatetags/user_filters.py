from django import template

register = template.Library()

@register.filter
def user_declension(count):
    count = abs(int(count))
    last_digit = count % 10
    last_two_digits = count % 100

    if 11 <= last_two_digits <= 14:
        form = "користувачів"
    elif last_digit == 1:
        form = "користувач"
    elif last_digit in [2, 3, 4]:
        form = "користувачі"
    else:
        form = "користувачів"

    return f"{count} {form}"
