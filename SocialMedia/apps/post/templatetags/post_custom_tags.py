from django import template
from django.utils.timezone import now

register = template.Library()


@register.simple_tag(name='cal_age_tag')
def calculate_age(time):
    age = now() - time
    year = age.days // 365
    month = age.days // 30
    day = age.days
    hour = (age.seconds // 60) // 60

    if year:
        return f'{year} year(s) ago'
    else:
        if month:
            return f'{month} month(s) ago'
        else:
            if day:
                return f'{day} day(s) ago'
            else:
                if hour :
                    return f'{hour} hour(s) ago'
                else:
                    return 'recently'
