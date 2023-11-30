
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import logging # импортируем модуль для логирования
import time # импортируем модуль для измерения времени

# настраиваем параметры логирования
logging.basicConfig(filename="experiment.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# загружаем данные из файла
start_time = time.time() # засекаем время начала загрузки данных
try: # пытаемся загрузить данные из файла
    data = pd.read_csv("experiment_data.csv")
except Exception as e: # если возникает исключение, то ловим его и логируем
    logging.error(f"Failed to load data from file: {e}") # логируем ошибку
    raise # пробрасываем исключение дальше
end_time = time.time() # засекаем время окончания загрузки данных
load_time = end_time - start_time # вычисляем время загрузки данных
logging.info(f"Data loaded in {load_time:.2f} seconds") # логируем время загрузки данных


# логируем количество и качество данных
logging.info(f"Data shape: {data.shape}") # логируем размерность данных
logging.info(f"Data columns: {data.columns}") # логируем названия колонок
logging.info(f"Data types: {data.dtypes}") # логируем типы данных
logging.info(f"Data summary: {data.describe()}") # логируем основные статистики
logging.info(f"Missing values: {data.isnull().sum()}") # логируем количество пропущенных значений
logging.info(f"Outliers: {data[(np.abs(stats.zscore(data["value"])) > 3)]}") # логируем выбросы по колонке value
logging.info(f"Duplicate rows: {data.duplicated().sum()}") # логируем количество дубликатов


control = data[data["group"] == "control"]
experiment = data[data["group"] == "experiment"]

# смотрим на основные статистики по каждой группе
control.describe()
experiment.describe()

# строим гистограммы распределения значений по каждой группе
plt.hist(control["value"], bins=20, alpha=0.5, label="control")
plt.hist(experiment["value"], bins=20, alpha=0.5, label="experiment")
plt.legend()
plt.show()

# логируем графики, которые строятся в коде
plt.savefig("histogram.png") # сохраняем гистограмму в формате png
logging.info(f"Histogram saved as histogram.png") # логируем имя файла гистограммы

# проверяем нормальность распределений с помощью теста Шапиро-Уилка
control_shapiro = stats.shapiro(control["value"])
experiment_shapiro = stats.shapiro(experiment["value"])
print(f"p-value for control group: {control_shapiro[1]}")
print(f"p-value for experiment group: {experiment_shapiro[1]}")

# логируем результаты теста Шапиро-Уилка
logging.info(f"Shapiro-Wilk test for control group: statistic = {control_shapiro[0]}, p-value = {control_shapiro[1]}") # логируем статистику и p-value для контрольной группы
logging.info(f"Shapiro-Wilk test for experiment group: statistic = {experiment_shapiro[0]}, p-value = {experiment_shapiro[1]}") # логируем статистику и p-value для экспериментальной группы

# если p-value меньше 0.05, то отвергаем нулевую гипотезу о нормальности распределения
if control_shapiro[1] < 0.05:
    print("Control group is not normally distributed")
else:
    print("Control group is normally distributed")

if experiment_shapiro[1] < 0.05:
    print("Experiment group is not normally distributed")
else:
    print("Experiment group is normally distributed")

# выбираем подходящий статистический тест в зависимости от нормальности распределений
# если обе группы нормально распределены, то используем t-тест
# если хотя бы одна группа не нормально распределена, то используем U-тест Манна-Уитни
if control_shapiro[1] >= 0.05 and experiment_shapiro[1] >= 0.05:
    # используем t-тест
    start_time = time.time() # засекаем время начала t-теста
    try: # пытаемся провести t-тест
        ttest = stats.ttest_ind(control["value"], experiment["value"])
        print(f"p-value for t-test: {ttest[1]}")
   
        if ttest[1] < 0.05:
            print("There is a significant difference between the means of the two groups")
        else:
            print("There is no significant difference between the means of the two groups")
    
        # логируем результаты t-теста
        logging.info(f"t-test for the difference of means: statistic = {ttest[0]}, p-value = {ttest[1]}, degrees of freedom = {len(control) + len(experiment) - 2}") # логируем статистику, p-value и степени свободы для t-теста
    except Exception as e: # если возникает исключение, то ловим его и логируем
        logging.error(f"Failed to perform t-test: {e}") # логируем ошибку
        raise # пробрасываем исключение дальше
    end_time = time.time() # засекаем время окончания t-теста
    ttest_time = end_time - start_time # вычисляем время t-теста
    logging.info(f"t-test performed in {ttest_time:.2f} seconds") # логируем время t-теста
else:
    # используем U-тест Манна-Уитни
    start_time = time.time() # засекаем время начала U-теста
    try: # пытаемся провести U-тест
        utest = stats.mannwhitneyu(control["value"], experiment["value"])
        print(f"p-value for U-test: {utest[1]}")
   
        if utest[1] < 0.05:
            print("There is a significant difference between the medians of the two groups")
        else:
            print("There is no significant difference between the medians of the two groups")
    
        # логируем результаты U-теста
        logging.info(f"U-test for the difference of medians: statistic = {utest[0]}, p-value = {utest[1]}") # логируем статистику и p-value для U-теста
    except Exception as e: # если возникает исключение, то ловим его и логируем
        logging.error(f"Failed to perform U-test: {e}") # логируем ошибку
        raise # пробрасываем исключение дальше
    end_time = time.time() # засекаем время окончания U-теста
    utest_time = end_time - start_time # вычисляем время U-теста
    logging.info(f"U-test performed in {utest_time:.2f} seconds") # логируем время U-теста