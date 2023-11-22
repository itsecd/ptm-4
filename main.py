import matplotlib.pyplot as plt
import pandas as pd
import torch
import numpy as np
from torch.nn import Linear, Sigmoid


def load_data():
    """
    Загрузка данных из файла.
    """
    try:
        data = pd.read_csv("./apples_pears.csv")
    except Exception as e:
        print(f"Ошибка при открытии файла: {str(e)}")
    X = data.iloc[:, :2].values
    y = data['target'].values.reshape((-1, 1))
    return data, X, y


def plot_graph(data, c, cmap):
    """
    Построение графика.
    :param c: данные для графика.
    :param cmap: данные для графика.
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=c, cmap=cmap)
    plt.title('Яблоки и груши', fontsize=15)
    plt.xlabel('симметричность', fontsize=14)
    plt.ylabel('желтизна', fontsize=14)
    plt.show()


def neuron_create(data, X):
    """
    Создание нейрона.
    :param data: Данные для создания нейрона.
    :param X: параметр X для создания нейрона.
    """
    num_features = X.shape[1]
    neuron = torch.nn.Sequential(Linear(num_features, out_features=1), Sigmoid())
    neuron(torch.autograd.Variable(torch.FloatTensor([1, 1])))
    proba_pred = neuron(torch.autograd.Variable(torch.FloatTensor(X)))
    y_pred = proba_pred > 0.5
    y_pred = y_pred.data.numpy().reshape(-1)
    plot_graph(data, y_pred, "spring")
    return neuron


def neuron_learning(X, y, neuron, learning_rate, iter_num):
    """
    Обучение нейрона.
    :param X: параметр X для обучения.
    :param y: параметр y для обучения.
    :param neuron: нейрон для обучения.
    :param learning_rate: скорость обучения.
    :param iter_num: Количество итераций.
    """
    X = torch.autograd.Variable(torch.FloatTensor(X))
    y = torch.autograd.Variable(torch.FloatTensor(y))
    loss_fn = torch.nn.MSELoss(reduction='mean')
    optimizer = torch.optim.SGD(neuron.parameters(), lr=learning_rate)
    for t in range(iter_num):
        y_pred = neuron(X)
        loss = loss_fn(y_pred, y)
        """print('{} {}'.format(t, loss.data))"""
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    proba_pred = neuron(X)
    y_pred = proba_pred > 0.5
    y_pred = y_pred.data.numpy().reshape(-1)
    plot_graph(data, y_pred, "spring")


def difficult_sampling():
    """
    Более сложная выборка.
    """
    N = 100
    D = 2
    K = 3
    X = np.zeros((N * K, D))
    y = np.zeros(N * K, dtype='uint8')
    for j in range(K):
        ix = range(N * j, N * (j + 1))
        r = np.linspace(0.0, 1, N)
        t = np.linspace(j * 4, (j + 1) * 4, N) + np.random.randn(N) * 0.2  # theta
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[ix] = j
    plt.figure(figsize=(10, 8))
    plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.rainbow)
    plt.title('Спираль', fontsize=15)
    plt.xlabel('$x$', fontsize=14)
    plt.ylabel('$y$', fontsize=14)
    plt.show()
    X = torch.autograd.Variable(torch.FloatTensor(X))
    y = torch.autograd.Variable(torch.LongTensor(y.astype(np.int64)))
    print(X.data.shape, y.data.shape)
    return X, y


def sigmoid_neuron(X, y):
    """
    Обучение нейрона с сигмоидой на линейно неразделимой выборке.
    :param X: параметр X для обучения.
    :param y: параметр y для обучения.
    """
    N, D_in, D_out = 64, 2, 3
    neuron = torch.nn.Sequential(torch.nn.Linear(D_in, D_out),)
    loss_fn = torch.nn.CrossEntropyLoss(reduction="mean")
    learning_rate = 0.5
    optimizer = torch.optim.SGD(neuron.parameters(), lr=learning_rate)
    for t in range(500):
        y_pred = neuron(X)
        loss = loss_fn(y_pred, y)
        """print('{} {}'.format(t, loss.data))"""
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    X = X.data.numpy()
    y = y.data.numpy()
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    grid_tensor = torch.FloatTensor(np.c_[xx.ravel(), yy.ravel()])
    Z = neuron(torch.autograd.Variable(grid_tensor))
    Z = Z.data.numpy()
    Z = np.argmax(Z, axis=1)
    Z = Z.reshape(xx.shape)
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, cmap=plt.cm.rainbow, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.rainbow)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title('Спираль', fontsize=15)
    plt.xlabel('$x$', fontsize=14)
    plt.ylabel('$y$', fontsize=14)
    plt.show()


if __name__ == '__main__':
    data, X, y = load_data()
    print("Набор данных «Яблоки-груши» в виде точек на плоскости:")
    plot_graph(data, data['target'], "rainbow")
    print("Результат классификации ещё необученным нейроном:")
    neuron = neuron_create(data, X)
    print("Результат обучения при learning_rate = 0.001 и 500 итераций")
    neuron_learning(X, y, neuron, 0.001, 500)
    print("Результат более сложной выборки:")
    diff_X, diff_y = difficult_sampling()
    print("Результат обучения нейрона с сигмоидой на линейно неразделимой выборке:")
    sigmoid_neuron(diff_X, diff_y)