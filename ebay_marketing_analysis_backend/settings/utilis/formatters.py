from django.utils.formats import date_format
from django.utils import timezone

def custom_datetime_format(custom_datetime):
    created_at = timezone.datetime.strptime(str(custom_datetime), '%Y-%m-%dT%H:%M:%S.%f%z')
    formated_datetime = date_format(created_at, format='M d, Y, P') 
    return formated_datetime