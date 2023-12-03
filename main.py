# импортируем необходимые библиотеки
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as st
# импортируем библиотеки логгирования
import logging
import pkg_resources

# Настройка логгирования
logging.basicConfig(filename='my_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для логгирования версий библиотек
def log_library_versions():
    libraries = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'statsmodels', 'scipy']
    for lib in libraries:
        try:
            version = pkg_resources.get_distribution(lib).version
            logging.info(f'{lib} version: {version}')
        except pkg_resources.DistributionNotFound:
            logging.warning(f'{lib} is not installed')

# Логгируем версии библиотек
log_library_versions()

# загружаем данные из файла datastats.csv
data = pd.read_csv('datastats.csv')
logging.info("Данные из файла datastats.csv успешно загружены.")

# создаем объект логгера с именем data_logger
data_logger = logging.getLogger('data_logger')
# устанавливаем уровень логирования
data_logger.setLevel(logging.INFO)
# создаем объект обработчика, который будет выводить логи в консоль
stream_handler = logging.StreamHandler()
# создаем объект форматтера, который будет определять формат логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# связываем обработчик с форматтером
stream_handler.setFormatter(formatter)
# добавляем обработчик к логгеру
data_logger.addHandler(stream_handler)
# логируем количество строк и столбцов в данных
data_logger.info(f"Data has {data.shape[0]} rows and {data.shape[1]} columns")
# логируем количество пропущенных значений в данных
data_logger.info(f"Data has {data.isna().sum().sum()} missing values")
# логируем количество дубликатов в данных
data_logger.info(f"Data has {data.duplicated().sum()} duplicated rows")
# логируем количество выбросов в данных, используя правило трех сигм
outliers = data[(data - data.mean()).abs() > 3 * data.std()].count().sum()
data_logger.info(f"Data has {outliers} outliers using the 3-sigma rule")

# генерируем данные из гамма-распределения
np.random.seed(42)
n = 100 # размер выборки
k = 2 # параметр формы
theta = 3 # параметр масштаба
y = np.random.gamma(k, theta, n) # зависимая переменная
x1 = np.random.normal(0, 1, n) # независимая переменная 1
x2 = np.random.uniform(0, 1, n) # независимая переменная 2
x3 = np.random.binomial(1, 0.5, n) # независимая переменная 3
df = pd.DataFrame({'y': y, 'x1': x1, 'x2': x2, 'x3': x3}) # создаем датафрейм
logging.info("Данные успешно сгенерированы и добавлены в датафрейм.")

# Выводим информацию о данных
logging.info(df.info())

# Выводим описательную статистику
logging.info(df.describe())

# Строим матрицу корреляций
corr_matrix = df.corr()
logging.info("Матрица корреляций:\n" + str(corr_matrix))

# выбираем зависимую и независимые переменные
y = df['y']
X = df[['x1', 'x2', 'x3']]

# добавляем константу к независимым переменным
X = sm.add_constant(X)

# строим гамма-регрессию с логарифмической связью
model = sm.GLM(y, X, family=sm.families.Gamma(link=sm.families.links.log))
results = model.fit()

# Выводим результаты регрессии
logging.info(results.summary())


# добавляем функцию для расчета ковариационного момента
def cov(x, y):
    # проверяем, что x и y имеют одинаковую длину
    assert len(x) == len(y), "x and y must have the same length"
    # вычисляем средние значения x и y
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    # вычисляем сумму произведений отклонений от средних
    sum_xy = np.sum((x - x_mean) * (y - y_mean))
    # делим сумму на n - 1
    cov_xy = sum_xy / (len(x) - 1)
    # возвращаем ковариационный момент
    logging.info("Функция cov() успешна выполнена")
    return cov_xy

# добавляем функцию для расчета математического ожидания
def mean(x):
    # вычисляем сумму всех элементов x
    sum_x = np.sum(x)
    # делим сумму на количество элементов
    mean_x = sum_x / len(x)
    # возвращаем математическое ожидание
    logging.info("Функция mean() успешна выполнена")
    return mean_x

# добавляем функцию для вычисления совместной плотности распределения двух нормально-распределенных величин
def joint_pdf(x, y, mu_x, mu_y, sigma_x, sigma_y, rho):
    # проверяем, что x и y имеют одинаковую длину
    assert len(x) == len(y), "x and y must have the same length"
    # вычисляем константу перед экспонентой
    c = 1 / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))
    # вычисляем аргумент экспоненты
    z = - 1 / (2 * (1 - rho**2)) * ((x - mu_x) / sigma_x)**2 - 2 * rho * (x - mu_x) / sigma_x * (y - mu_y) / sigma_y + ((y - mu_y) / sigma_y)**2
    # возвращаем совместную плотность распределения
    logging.info("Функция joint_pdf() успешна выполнена")
    return c * np.exp(z)

# добавляем функцию для вычисления коэффициента корреляции Пирсона
def pearson_r(x, y):
    # проверяем, что x и y имеют одинаковую длину
    assert len(x) == len(y), "x and y must have the same length"
    # вычисляем средние значения x и y
    x_mean = mean(x)
    y_mean = mean(y)
    # вычисляем числитель и знаменатель формулы
    num = np.sum((x - x_mean) * (y - y_mean))
    den = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
    # возвращаем коэффициент корреляции Пирсона
    logging.info("Функция pearson_r() успешна выполнена")
    return num / den

# добавляем функцию для нахождения двусторонней критической области
def two_sided_critical_region(alpha, dist):
    # проверяем, что alpha лежит в интервале (0, 1)
    assert 0 < alpha < 1, "alpha must be between 0 and 1"
    # проверяем, что dist является объектом scipy.stats.rv_continuous
    assert isinstance(dist, st.rv_continuous), "dist must be a continuous distribution from scipy.stats"
    # вычисляем критическое значение z_alpha/2
    z_alpha_2 = dist.ppf(1 - alpha / 2)
    # возвращаем двустороннюю критическую область в виде списка интервалов
    logging.info("Функция two_sided_critical_region() успешна выполнена")
    return [(-np.inf, -z_alpha_2), (z_alpha_2, np.inf)]

# проводим t-тест для проверки гипотезы о равенстве средних y в зависимости от x3
t, p = st.ttest_ind(y[x3 == 0], y[x3 == 1])
logging.info(f"t-statistic = {t:.3f}, p-value = {p:.3f}")

# строим гистограмму распределения y
plt.hist(y, bins=10)
plt.xlabel('y')
plt.ylabel('Frequency')
plt.title('Histogram of y')
plt.show()

# строим диаграмму рассеяния y и x1
plt.scatter(y, x1)
plt.xlabel('y')
plt.ylabel('x1')
plt.title('Scatter plot of y and x1')
plt.show()

# строим ящик с усами для y в зависимости от x3
sns.boxplot(x=x3, y=y)
plt.xlabel('x3')
plt.ylabel('y')
plt.title('Box plot of y by x3')
plt.show()

# строим гистограмму распределения y
plt.hist(y, bins=10)
plt.xlabel('y')
plt.ylabel('Frequency')
plt.title('Histogram of y')
# сохраняем гистограмму в файл histogram.png
plt.savefig('histogram.png')
plt.show()

# строим диаграмму рассеяния y и x1
plt.scatter(y, x1)
plt.xlabel('y')
plt.ylabel('x1')
plt.title('Scatter plot of y and x1')
# сохраняем диаграмму в файл scatter.png
plt.savefig('scatter.png')
plt.show()

# строим ящик с усами для y в зависимости от x3
sns.boxplot(x=x3, y=y)
plt.xlabel('x3')
plt.ylabel('y')
plt.title('Box plot of y by x3')
# сохраняем ящик с усами в файл boxplot.png
plt.savefig('boxplot.png')
plt.show()