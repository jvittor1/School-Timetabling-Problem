import networkx as nx
from models.schedules import Schedules
from models.discipline import Discipline


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.schedules = Schedules()

    def print_disciplines(self):
        for node in self.graph.nodes:
            print(self.graph.nodes[node]["discipline"])

    def add_node(self, discipline: Discipline):
        self.graph.add_node(discipline.index, discipline=discipline)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def add_schedule(self, discipline_code, schedule):
        for node in self.graph.nodes:
            discipline = self.graph.nodes[node]["discipline"]
            if discipline.code == discipline_code:
                discipline.add_schedule(schedule)
                break

    def order_by_weight(self):
        nodes_sorted_by_weight = sorted(
            self.graph.nodes,
            key=lambda x: self.graph.nodes[x]["discipline"].weight,
            reverse=True,
        )
        return nodes_sorted_by_weight
