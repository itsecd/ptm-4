import matplotlib.pyplot as plt
import my_logger


def show_plt(cores: list, times: list) -> None:
    """Показываем график в соответсвии с полученными данными, ничего не возвращает"""
    if len(cores) == len(times):
        plt.plot(cores, times)
    else:
        logger = my_logger.My_log(__file__).get_logger()
        logger.error("Plotting is not possible. Different number of points")
    plt.xlabel("ядра, шт")
    plt.ylabel("Время, сек")
    plt.show()

