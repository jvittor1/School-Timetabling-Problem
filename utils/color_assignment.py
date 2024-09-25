import matplotlib.pyplot as plt
import hashlib


def hash_to_color(hash_value: str):
    cmap = plt.get_cmap("rainbow")
    color_index = int(hash_value, 16) % cmap.N
    return cmap(color_index)


def schedule_to_hash(schedule: str):
    return hashlib.sha1(schedule.encode()).hexdigest()


def color_function(schedule: str):
    hash_value = schedule_to_hash(schedule)
    return hash_to_color(hash_value)
