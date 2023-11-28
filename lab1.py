import csv
import json
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename="logs.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
SETTINGS_PATH = "settings.json"


def check_max_year(url: str) -> int:
    """Function that checks the maximum available year on the site

    Args:
        url (str): site url

    Returns:
        int: Maximum available year on the site
    """
    try:
        is_year_last = False
        year_counter = 2008
        while not is_year_last:
            try:
                html_text = requests.get(
                    url, headers={"User-Agent": "agent"}).text
            except Exception as e:
                logging.error(f"Invalid URL '{url}': No host supplied {e}")
            data = BeautifulSoup(html_text, "lxml")
            if data.find("span", class_="grey error-span"):
                is_year_last = True
                year_counter -= 1
            else:
                year_counter += 1
                url = url.replace(str(year_counter - 1), str(year_counter))
        return year_counter
    except Exception as e:
        logging.error(f"Error in check_max_year: {e}")
        raise


def check_max_month(url: str) -> int:
    """Function that checks the maximum available month on the site

    Args:
        url (str): site url

    Returns:
        int: maximum available month on the site
    """
    try:
        is_month_last = False
        month_counter = 1
        while not is_month_last:
            try:
                html_text = requests.get(
                    url, headers={"User-Agent": "agent"}).text
            except Exception as e:
                logging.error(f"Invalid URL '{url}': No host supplied {e}")
            data = BeautifulSoup(html_text, "lxml")
            if data.find("span", class_="grey error-span"):
                is_month_last = True
                month_counter -= 1
            else:
                month_counter += 1
                url = url[0:39] + "/" + str(month_counter) + "/"
        return month_counter
    except Exception as e:
        logging.error(f"Error in check_max_month: {e}")
        raise


def url_month_change(url: str, month: int, change_type: int) -> str:
    """Function that changes the month in the url

    Args:
        url (str): site url
        month (int): The month that need to change in the url
        change_type (int): Flag that responsible for how the url will change

    Returns:
        str: Changed url
    """
    try:
        if change_type == 1:
            url = url[0:39] + "/1/"
        elif change_type == 2:
            url = url[0:39] + "/" + str(month) + "/"
        return url
    except Exception as e:
        logging.error(f"Error in url_month_change: {e}")
        raise


def url_year_change(url: str, years: int) -> str:
    """Function that changes the year in the url

    Args:
        url (str): site url
        years (int): The month that need to change in the url

    Returns:
        str: Changed url
    """
    try:
        url = url.replace(str(years-1), str(years))
        return url
    except Exception as e:
        logging.error(f"Error in url_year_change: {e}")
        raise


def data_to_list(output: list[str], elements) -> list[str]:
    """This function extracts data from BeautifulSoup and appends it to the output list.

    Args:
        output (list[str]): The list to which the extracted data will be appended
        elements (): The ResultSet containing HTML elements.

    Returns:
        list[str]: The updated output list with extracted data.
    """
    try:
        x = [0, 1, 2, 5, 6, 7, 10]
        for i in x:
            output.append(elements[i].text)
        return output
    except Exception as e:
        logging.error(f"Error in data_to_list: {e}")
        raise


def days_redact(output: list[str]) -> str:
    """Function that checks if a number is less than 10, and if it is, it adds a leading 0 to the number

    Args:
        output (list[str]): List with data from site

    Returns:
        str: Changed number
    """
    try:
        if int(output[0]) < 10:
            return "0" + output[0]
        else:
            return output[0]
    except Exception as e:
        logging.error(f"Error in days_redact: {e}")
        raise


def months_redact(month: int) -> str:
    """Function that checks if a number is less than 10, and if it is, it adds a leading 0 to the number

    Args:
        month (int): Month number

    Returns:
        str: Changed number
    """
    try:
        if month < 10:
            return "0" + str(month)
        else:
            return str(month)
    except Exception as e:
        logging.error(f"Error in months_redact: {e}")
        raise


def read_settings_file(settings_path: str) -> tuple:
    try:
        with open(settings_path, "r") as file:
            settings = json.load(file)
            return settings.get("url"), settings.get("year_counter")
    except Exception as e:
        logging.error(f"Error reading file {e}")


if __name__ == "__main__":
    url, year_counter = read_settings_file(SETTINGS_PATH)
    current_year = check_max_year(url)
    for years in range(year_counter, current_year + 1):
        url = url_year_change(url, years)
        max_month = 12
        if years == current_year:
            max_month = check_max_month(url)
        for months in range(1, max_month + 1):
            logging.info(f"Processing {years}-{months}")
            is_month_last = False
            if months == max_month:
                url = url_month_change(url, months, 2)
                is_month_last = True
            elif months < max_month:
                url = url_month_change(url, months, 2)
            html_text = requests.get(
                url, headers={"User-Agent": "Ivan"}).text
            soup = BeautifulSoup(html_text, "lxml")
            lines = soup.find_all("tr", align="center")
            for i in range(len(lines)):
                elements = lines[i].find_all("td")
                output = []
                output = data_to_list(output, elements)
                with open("result.csv", "a", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile, lineterminator="\n")
                    try:
                        writer.writerow((str(years) + "-" + months_redact(months) + "-" + days_redact(
                            output), output[1], output[2], output[3], output[4], output[5], output[6]))
                    except Exception:
                        logging.error(
                            f"Error writing {years}-{ months_redact(months)}-{days_redact(output)}")
                    logging.info(
                        f"Writing {years}-{ months_redact(months)}-{days_redact(output)} was successful")
            if is_month_last:
                url = url_month_change(url, months, 1)
