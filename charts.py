import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='charts.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
plt.switch_backend('agg')


def line(list_x, list_y):
    """
    функция строит линейный график и сохраняет его для последующего отображения
    :param list_x: список координат x
    :param list_y: список координат y
    :return:
    """
    try:
        x = list_x[0:]
        y = list_y[0:]
        plt.plot(x, y)
        plt.savefig('line')
        plt.clf()
        logger.info("Line chart created")
    except Exception as e:
        logger.error("Error creating line chart: %s", str(e))


def hist(list_x, list_y):
    """
        функция строит гистограмму и сохраняет ее для последующего отображения
        :param list_x: список координат x
        :param list_y: список координат y
        :return:
        """
    try:
        x = list_x[0:]
        y = list_y[0:]
        plt.hist(y, bins=len(x))
        plt.savefig('hist')
        plt.clf()
        logger.info("Histogram created")
    except Exception as e:
        logger.error("Error creating histogram: %s", str(e))
