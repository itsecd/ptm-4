import os.path
import numpy as np
import statistics as st
import scipy.stats as sts
import matplotlib.pyplot as plt

GAMMA = 0.95
A = 2
SIGMA2 = 7
N = 20
K = 140
M = 1800


def find_expectation_inter(normal_sample: np.ndarray, gamma: float, sigma: float) -> tuple:
    """
    Функция нахождения доверительного интервала для математического ожидания выборки из нормальной
    генеральной совокупности при известной дисперсии
    :param normal_sample: Выборка из нормальной генеральной совокупности
    :param gamma: доверительная вероятность
    :param sigma: СКО
    :return: Кортеж из левой и правой границы доверительного интервала
    """
    t = sts.norm.ppf((1 + gamma) / 2, loc=0, scale=1)
    delta = t * sigma / np.sqrt(len(normal_sample))
    x_l = normal_sample.mean() - delta
    x_r = normal_sample.mean() + delta
    return x_l, x_r


def find_expectation_inter_no_dis(normal_sample: np.ndarray, gamma: float) -> tuple:
    """
    Функция нахождения доверительного интервала для математического ожидания выборки из нормальной
    генеральной совокупности при неизвестной дисперсии
    :param normal_sample: Выборка из нормальной генеральной совокупности
    :param gamma: доверительная вероятность
    :return: Кортеж из левой и правой границы доверительного интервала
    """
    t = sts.t.ppf(gamma/2 + 0.5, len(normal_sample) - 1)
    s = np.sqrt(st.pvariance(normal_sample))
    delta = t * s / np.sqrt(len(normal_sample))
    x_l = normal_sample.mean() - delta
    x_r = normal_sample.mean() + delta
    return x_l, x_r


def find_dispersion(normal_sample: np.ndarray, gamma: float) -> tuple:
    """
    Функция нахождения доверительного интервала для дисперсии выборки из нормальной
    генеральной совокупности
    :param normal_sample: Выборка из нормальной генеральной совокупности
    :param gamma: доверительная вероятность
    :return: Кортеж из левой и правой границы доверительного интервала
    """
    alpha = gamma/2 + 0.5
    s = st.pvariance(normal_sample)
    chil = sts.chi2.ppf(alpha, len(normal_sample) - 1)
    chir = sts.chi2.ppf(1 - alpha, len(normal_sample) - 1)
    sg_l = (len(normal_sample) - 1) * s / chil
    sg_r = (len(normal_sample) - 1) * s / chir
    return sg_l, sg_r


def plot_dependence_l_of_gamma_ex(number_of_points: int, sample_size: int, save_path: str, fig_name: str) -> None:
    """
    Функция создает график зависимости длины доверительного интервала математического ожидания от величины доверительной
    вероятности при неизменном объеме выборки
    :param number_of_points: число точек на графике
    :param sample_size: размер выборки
    :param save_path: путь для сохранения картинки
    :param fig_name: имя сохраненной картинки
    :return:
    """
    if sample_size <= 0 or number_of_points <= 0:
        return None
    gm = np.linspace(0, 1, number_of_points)
    sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=sample_size)
    len_ar = np.array([])
    for i in gm:
        l, r = find_expectation_inter_no_dis(sample, i)
        length = r - l
        len_ar = np.append(len_ar, length)
    fig = plt.figure()
    plt.plot(gm, len_ar)
    plt.ylabel("L")
    plt.xlabel("gamma")
    plt.title(f'Зависимость L от gamma при n={len(sample)}')
    if os.path.isdir(save_path) and os.path.exists(save_path) \
            and (fig_name.endswith(".png") or fig_name.endswith(".jpg")):
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)


def plot_dependence_l_of_gamma_dis(number_of_points: int, sample_size: int, save_path: str, fig_name: str) -> None:
    """
    Функция создает график зависимости длины доверительного интервала дисперсии от величины доверительной
    вероятности при неизменном объеме выборки
    :param number_of_points: число точек на графике
    :param sample_size: размер выборки
    :param save_path: путь для сохранения картинки
    :param fig_name: имя сохраненной картинки
    :return:
    """
    if sample_size <= 0 or number_of_points <= 0:
        return None
    gm = np.linspace(0, 0.99, number_of_points)
    sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=sample_size)
    len_ar = np.array([])
    for i in range(len(gm)):
        l, r = find_dispersion(sample, gm[i])
        length = r - l
        len_ar = np.append(len_ar, length)
    fig = plt.figure()
    plt.plot(gm, len_ar)
    plt.ylabel("L")
    plt.xlabel("gamma")
    plt.title(f'Зависимость L от gamma при n={len(sample)}')
    if os.path.isdir(save_path) and os.path.exists(save_path) \
            and (fig_name.endswith(".png") or fig_name.endswith(".jpg")):
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)


def plot_dependence_l_of_n_ex(gamma: float, min_size: int, max_size: int,
                              number_of_points: int, save_path: str, fig_name: str) -> None:
    """
     Функция создает график зависимости длины доверительного интервала математического ожидания от объъема выборки
    :param gamma: доверительная вероятность
    :param min_size: минимальный объем выборки
    :param max_size: максимальный объем выборки
    :param number_of_points: число точек на графике
    :param save_path: путь для сохранения картинки
    :param fig_name: имя сохраненной картинки
    :return:
    """
    if min_size <= 0 or max_size <= min_size or number_of_points <= 0:
        return None
    n_ar = np.linspace(min_size, max_size, number_of_points, dtype=int)
    len_ar = np.array([])
    for i in n_ar:
        normal_sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=i)
        l, r = find_expectation_inter_no_dis(normal_sample, gamma)
        length = r - l
        len_ar = np.append(len_ar, length)
    fig = plt.figure()
    plt.plot(n_ar, len_ar)
    plt.xlabel("N")
    plt.ylabel("L")
    plt.title(f'Зависимость L от N при gamma = {gamma}')
    if os.path.isdir(save_path) and os.path.exists(save_path)\
            and (fig_name.endswith(".png") or fig_name.endswith(".jpg")):
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)


def plot_dependence_l_of_n_dis(gamma: float, min_size: int, max_size: int,
                               number_of_points: int, save_path: str, fig_name: str) -> None:
    """
    Функция создает график зависимости длины доверительного интервала дисперсии от объъема выборки
    :param gamma: доверительная вероятность
    :param min_size: минимальный объем выборки
    :param max_size: максимальный объем выборки
    :param number_of_points: число точек на графике
    :param save_path: путь для сохранения картинки
    :param fig_name: имя сохраненной картинки
    :return:
    """
    if min_size <= 0 or max_size <= min_size or number_of_points <= 0:
        return None
    n_ar = np.linspace(min_size, max_size, number_of_points, dtype=int)
    len_ar = np.array([])
    for i in n_ar:
        normal_sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=i)
        l, r = find_dispersion(normal_sample, gamma)
        length = r - l
        len_ar = np.append(len_ar, length)
    fig = plt.figure()
    plt.plot(n_ar, len_ar)
    plt.xlabel("N")
    plt.ylabel("L")
    plt.title(f'Зависимость L от N при gamma = {gamma}')
    if os.path.isdir(save_path) and os.path.exists(save_path) \
            and (fig_name.endswith(".png") or fig_name.endswith(".jpg")):
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)


def find_emp_gamma(m: int) -> float:
    """
    Функция нахождения точечной оценки доверительной вероятности гамма при m испытаниях
    :param m: число испытаний
    :return: точечная оценка доверительной вероятности, -1 в случае ошибки
    """
    if m <= 0:
        return -1
    counter = 0
    for i in range(m):
        sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=N)
        left, right = find_expectation_inter_no_dis(sample, GAMMA)
        if left <= A <= right:
            counter += 1
    return counter/m
