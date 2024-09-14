from utils.json import read_json_data
from models.discipline import Discipline
from models.graph import Graph
from utils.format import format_schedule
from utils.color_assignment import color_function
import networkx as nx
import matplotlib.pyplot as plt


def get_most_teacher_classes(graph: Graph):
    teacher_count = {}

    for node in graph.graph.nodes:
        discipline = graph.graph.nodes[node]["discipline"]
        teacher_count[discipline.teacher] = teacher_count.get(discipline.teacher, 0) + 1

    max_count = max(teacher_count.values())
    max_teachers = [
        teacher for teacher, count in teacher_count.items() if count == max_count
    ]

    return max_teachers


def get_most_heavy_semester(graph: Graph):
    semester_count = {}

    for node in graph.graph.nodes:
        discipline = graph.graph.nodes[node]["discipline"]
        semester_count[discipline.semester] = (
            semester_count.get(discipline.semester, 0) + 1
        )

    max_count = max(semester_count.values())
    max_semesters = [
        semester for semester, count in semester_count.items() if count == max_count
    ]

    return max_semesters


def define_weight(graph: Graph):
    def sin_discipline(discipline):
        return discipline.course.lower() == "sin"

    def cco_discipline(discipline):
        return discipline.course.lower() == "cco"

    def most_teacher_classes(discipline):
        return discipline.teacher in get_most_teacher_classes(graph)

    def most_heavy_semester(discipline):
        return discipline.semester in get_most_heavy_semester(graph)

    for node in graph.graph.nodes:
        discipline = graph.graph.nodes[node]["discipline"]
        weight = 0
        if sin_discipline(discipline):
            weight += 10
        if cco_discipline(discipline):
            weight += 5
        if most_teacher_classes(discipline):
            weight += 3
        if most_heavy_semester(discipline):
            weight += 2
        discipline.set_weight(weight)

    graph.order_by_weight()
    return graph


def available_schedule(slots: list, slot: int, discipline: Discipline):
    for existing_discipline in slots[slot]:
        if existing_discipline["teacher"] == discipline.teacher:
            return False

    for existing_discipline in slots[slot]:
        if (
            discipline.semester == existing_discipline["semester"]
            and discipline.course == existing_discipline["course"]
        ):
            return False

    count = 0
    for day_slots in slots:
        for existing_discipline in day_slots:
            if discipline.index == existing_discipline["index"]:
                count += 1

            if count >= 2 and discipline.ch == 4:
                return False

            if count >= 3 and discipline.ch == 5:
                return False

    count = 0
    for day_slots in slots:
        for existing_discipline in day_slots:
            if existing_discipline["teacher"] == discipline.teacher:
                count += 1

            if count >= 6:
                return False

    return True


def is_night_period(discipline: Discipline, slot: int):
    return discipline.course.lower() == "sin" and slot >= 10


def is_saturday_course(discipline: Discipline):
    return discipline.course.lower() not in ["sin", "cco"]


def generate_schedule(graph: Graph):
    for node in graph.order_by_weight():
        discipline = graph.graph.nodes[node]["discipline"]
        allocated_slots = 0
        while allocated_slots < discipline.ch:
            for day_schedule in graph.schedules.get_schedule():
                for day, slots in day_schedule.items():
                    for slot in range(len(slots)):

                        if discipline.course.lower() == "sin" and not is_night_period(
                            discipline, slot
                        ):
                            continue

                        if day == "Saturday" and not is_saturday_course(discipline):
                            continue

                        if available_schedule(slots, slot, discipline):
                            slots[slot].append(
                                {
                                    "name": discipline.name,
                                    "code": discipline.code,
                                    "teacher": discipline.teacher,
                                    "course": discipline.course,
                                    "semester": discipline.semester,
                                    "ch": discipline.ch,
                                    "index": discipline.index,
                                }
                            )
                            discipline.add_schedule({day: slot})
                            allocated_slots += 1

                        if allocated_slots >= discipline.ch:
                            break

                    if allocated_slots >= discipline.ch:
                        break

                if allocated_slots >= discipline.ch:
                    break

        if allocated_slots < discipline.ch:
            print(
                f"Não foi possível alocar a disciplina {discipline.name} ({discipline.code})"
            )

    return graph


def generate_edge(graph: Graph):
    for node1 in graph.graph.nodes:
        discipline1 = graph.graph.nodes[node1]["discipline"]
        for node2 in graph.graph.nodes:
            if node1 != node2:
                discipline2 = graph.graph.nodes[node2]["discipline"]
                if (discipline1.teacher == discipline2.teacher) or (
                    discipline1.semester == discipline2.semester
                    and discipline1.course == discipline2.course
                ):
                    graph.add_edge(node1, node2)
    return graph


def generate_graph(data: list):
    graph = Graph()
    count = 0
    for index, discipline_data in enumerate(data):
        count += discipline_data["ch"]
        discipline = Discipline(
            index,
            discipline_data["name"],
            discipline_data["teacher"],
            discipline_data["code"],
            discipline_data["semester"],
            discipline_data["ch"],
            discipline_data["course"],
        )
        graph.add_node(discipline)

    graph = generate_edge(graph)
    # print(f"Total classes: {count}")
    return graph


def plot_graph(graph):

    color_map = {}

    for node in graph.graph.nodes:
        discipline = graph.graph.nodes[node]["discipline"]

        if not discipline.schedule:
            color_map[node] = "gray"
        else:
            color_map[node] = color_function(str(discipline.schedule))

    colors = [color_map[node] for node in graph.graph.nodes]

    pos = nx.spring_layout(graph.graph)

    nx.draw(graph.graph, pos, node_color=colors, with_labels=True)

    plt.show()


def main():
    data = read_json_data("cenarios/cenario1.json")
    graph = generate_graph(data)
    graph = define_weight(graph)
    graph = generate_schedule(graph)
    format_schedule(graph)
    plot_graph(graph)
    # graph.print_disciplines()


if __name__ == "__main__":
    main()
