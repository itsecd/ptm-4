import matplotlib.pyplot as plt
import logging


def show_plt(cores: list, times: list) -> None:
    """Показываем график в соответсвии с полученными данными, ничего не возвращает"""
    plt.plot(cores, times)
    plt.xlabel("ядра, шт")
    plt.ylabel("Время, сек")
    plt.show()
