from django import template
from datetime import date, timedelta

register = template.Library()


@register.filter
def group_by_week(dias, mes):
    if not dias:
        return []
    primer_dia = date(dias[0]["fecha"].year, mes, 1)
    start_weekday = primer_dia.weekday()
    weeks = []
    current_week = [None] * start_weekday if start_weekday < 6 else []
    dias_ordenados = sorted(dias, key=lambda d: d["dia"])
    for d in dias_ordenados:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)
    return weeks
