import os.path
import logging
import numpy as np
import statistics as st
import scipy.stats as sts
import matplotlib.pyplot as plt

logging.basicConfig(filename="logs.log", level=logging.INFO,
                    format=u'%(levelname)s  %(filename)s %(asctime)s %(message)s')
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
    logging.info(f'Expectation inter [{x_l}, {x_r}] with known dispersion was successfully found for gamma = {gamma}')
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
    logging.info(f'Expectation inter [{x_l}, {x_r}] with known dispersion was successfully found for gamma = {gamma}')
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
    chi_left = sts.chi2.ppf(alpha, len(normal_sample) - 1)
    chi_right = sts.chi2.ppf(1 - alpha, len(normal_sample) - 1)
    sg_l = (len(normal_sample) - 1) * s / chi_left
    sg_r = (len(normal_sample) - 1) * s / chi_right
    if chi_left == 0 or chi_right == 0:
        logging.warning(f'Gamma value({gamma}) might be incorrect, must be in [0, 1)')
    else:
        logging.info(f'Dispersion interval [{sg_l}, {sg_r}] was successfully found for gamma = {gamma}')
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
        logging.error(f'One or both sample_size and numer_of_points argument is incorrect, should be > 0')
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
    if not os.path.isdir(save_path):
        logging.error(f'save path: {save_path}, is incorrect')
        return None
    if not os.path.exists(save_path):
        logging.error(f'save path: {save_path} does not exist')
        return None
    if not fig_name.endswith(".png") or not fig_name.endswith(".jpg"):
        logging.error(f'Name for plot {fig_name} has incorrect extention')
        return None
    else:
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)
        logging.info(f'Dependence L of gamma for expectation plot was successfully saved in {full_path}')


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
        logging.error(f'One or both sample_size and numer_of_points argument is incorrect, should be > 0')
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
    if not os.path.isdir(save_path):
        logging.error(f'save path: {save_path}, is incorrect')
        return None
    if not os.path.exists(save_path):
        logging.error(f'save path: {save_path} does not exist')
        return None
    if not fig_name.endswith(".png") or not fig_name.endswith(".jpg"):
        logging.error(f'Name for plot {fig_name} has incorrect extension')
        return None
    else:
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)
        logging.info(f'Dependence L of gamma for dispersion plot was successfully saved in {full_path}')


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
    if min_size <= 0 or max_size <= min_size:
        logging.error(f'One or both of arguments for minimum sample size ({min_size}) or maximum sample size '
                      f'({max_size}) is incorrect, should be > 0, max size should be > min size')
        return None
    if number_of_points <= 0:
        logging.error(f'number of points argument({number_of_points}) is incorrect, should be > 0')
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
    if not os.path.isdir(save_path):
        logging.error(f'save path: {save_path}, is incorrect')
        return None
    if not os.path.exists(save_path):
        logging.error(f'save path: {save_path} does not exist')
        return None
    if not fig_name.endswith(".png") or not fig_name.endswith(".jpg"):
        logging.error(f'Name for plot {fig_name} has incorrect extension')
        return None
    else:
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)
        logging.info(f'Dependence L of sample size for expectation plot was successfully saved in {full_path}')


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
    if min_size <= 0 or max_size <= min_size:
        logging.error(f'One or both of arguments for minimum sample size ({min_size}) or maximum sample size '
                      f'({max_size}) is incorrect, should be > 0, max size should be > min size')
        return None
    if number_of_points <= 0:
        logging.error(f'number of points argument({number_of_points}) is incorrect, should be > 0')
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
    if not os.path.isdir(save_path):
        logging.error(f'save path: {save_path}, is incorrect')
        return None
    if not os.path.exists(save_path):
        logging.error(f'save path: {save_path} does not exist')
        return None
    if not fig_name.endswith(".png") or not fig_name.endswith(".jpg"):
        logging.error(f'Name for plot {fig_name} has incorrect extension')
        return None
    else:
        full_path = os.path.join(save_path, fig_name)
        fig.savefig(full_path)
        logging.info(f'Dependence L of sample size for dispersion plot was successfully saved in {full_path}')


def find_emp_gamma(m: int) -> float:
    """
    Функция нахождения точечной оценки доверительной вероятности гамма при m испытаниях
    :param m: число испытаний
    :return: точечная оценка доверительной вероятности, -1 в случае ошибки
    """
    if m <= 0:
        logging.error(f'Incorrect number of tests({m}), should be > 0')
        return -1
    counter = 0
    for i in range(m):
        sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=N)
        left, right = find_expectation_inter_no_dis(sample, GAMMA)
        if left <= A <= right:
            counter += 1
    logging.info("Empirical value of gamma was successfully found")
    return counter/m


if __name__ == "__main__":
    sample = np.random.normal(loc=A, scale=np.sqrt(SIGMA2), size=N)
    find_expectation_inter(sample, gamma=GAMMA, sigma=np.sqrt(SIGMA2))
    find_expectation_inter_no_dis(sample, GAMMA)
    find_dispersion(sample, GAMMA)
    find_dispersion(sample, 1)
    find_emp_gamma(M)
    find_emp_gamma(-1)
    plot_dependence_l_of_n_dis(GAMMA, 5, 100, 500, "D:", "fg.png")
    plot_dependence_l_of_n_dis(GAMMA, 10, 5, 500, "D:", "fg.png")
    plot_dependence_l_of_gamma_ex(1000, 1000, "R//", "fg.pnb")
    plot_dependence_l_of_gamma_ex(1000, 1000, "D:", "fg134")
