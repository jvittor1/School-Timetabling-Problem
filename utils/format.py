from models.graph import Graph


def format_schedule(graph: Graph):
    for node in graph.graph.nodes:
        discipline = graph.graph.nodes[node]["discipline"]
        formatted_schedules = []

        for schedule in discipline.schedule:
            for day, slot in schedule.items():
                day_number = format_days(day)
                formatted_slot = format_class(slot)
                formatted_schedules.append(f"{day_number}{formatted_slot}")

        formatted_schedule_str = " ".join(formatted_schedules)
        discipline.schedule = formatted_schedule_str


def format_days(day: str):
    days_map = {
        "monday": "2",
        "tuesday": "3",
        "wednesday": "4",
        "thursday": "5",
        "friday": "6",
        "saturday": "7",
    }
    return days_map[day.lower()]


def format_class(class_: int):
    if class_ < 5:
        return f"M{class_}"

    if class_ < 10:
        return f"T{class_ - 5}"

    if class_ < 15:
        return f"N{class_ - 10}"
    return class_
