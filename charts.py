import matplotlib.pyplot as plt

plt.switch_backend('agg')


def line(list_x, list_y):
    """
    функция строит линейный график и сохраняет его для последующего отображения
    :param list_x: список координат x
    :param list_y: список координат y
    :return:
    """
    x = list_x[0:]
    y = list_y[0:]
    plt.plot(x, y)
    plt.savefig('line')
    plt.clf()


def hist(list_x, list_y):
    """
        функция строит гистограмму и сохраняет ее для последующего отображения
        :param list_x: список координат x
        :param list_y: список координат y
        :return:
        """
    x = list_x[0:]
    y = list_y[0:]
    plt.hist(y, bins=len(x))
    plt.savefig('hist')
    plt.clf()
