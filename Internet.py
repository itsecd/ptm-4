import logging
import requests
import time


logging.basicConfig(filename='Internet.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def check_internet_connection(timeout=1, max_retries=10):
    """
    Checks for internet connection by attempting to send a request to a specified URL.
    """
    logging.info('Checking internet connection')
    retries = 0

    while retries < max_retries:
        logging.debug(f'Attempt {retries + 1} of {max_retries}')
        try:
            requests.head("https://www.google.com/", timeout=timeout)
            logging.info('Internet connection established')
            return True
        except (requests.ConnectionError, requests.Timeout, requests.RequestException) as e:
            logging.warning(f'No internet connection: {e}')
            retries += 1
            time.sleep(5)

    logging.error('Failed to establish an internet connection after all retries')
    return False


if __name__ == "__main__":
    check_internet_connection()
