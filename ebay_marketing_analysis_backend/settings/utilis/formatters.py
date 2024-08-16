from django.utils.formats import date_format
from django.utils import timezone
import re
 
def custom_datetime_format(custom_datetime):
    created_at = timezone.datetime.strptime(str(custom_datetime), '%Y-%m-%dT%H:%M:%S.%f%z')
    formated_datetime = date_format(created_at, format='M d, Y, P')
    formated_datetime = formated_datetime.replace('a.m.', 'AM').replace('p.m.', 'PM')
    return formated_datetime

def format_number(number):
    number = float(number)
    number_info = str(round(number, 2)).split('.')
    integral_part = number_info[0]
    last_3_digits = integral_part[-3:]
    integral_part = integral_part[:-3] 
    if len(number_info) == 2:
        fractional_part = number_info[1]
    formated_number = str(integral_part)[::-1]  # Reverse the string representation of the number
    formated_number = re.sub(r'(\d{2})(?=\d)', r'\1,', formated_number)  # Add commas after every 2 digits
    formated_number = formated_number[::-1]  # Reverse the string back to its original order
    if formated_number:
        formated_number += ',' + last_3_digits
    else:
        formated_number = last_3_digits
    if len(number_info) == 2:
        formated_number = f'{formated_number}.{fractional_part}' 
    return formated_number
