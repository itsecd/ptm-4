import random


def generate_mas(list_where_write: list, left: int, right: int, size: int) -> None:
    for i in range(size):
        list_where_write.append(random.randint(left, right))


def del_n_elem(list_where_del: list, num_of_elem: int) -> None:
    for i in range(num_of_elem):
        list_where_del.pop(0)
        list_where_del.pop(-1)
