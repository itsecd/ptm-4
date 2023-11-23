import matplotlib.pyplot as plt
plt.switch_backend('agg')


def line(list_x, list_y):
    x = list_x[0:]
    y = list_y[0:]
    plt.plot(x, y)
    plt.savefig('line')
    plt.clf()


def hist(list_x, list_y):
    x = list_x[0:]
    y = list_y[0:]
    plt.hist(y, bins=len(x))
    plt.savefig('hist')
    plt.clf()