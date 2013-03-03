from django import template

register = template.Library()

@register.filter(is_safe=True)
def mission_time(mission):
    return " ".join([mission.day.strftime("%A"), mission.TIMES[mission.time]])
