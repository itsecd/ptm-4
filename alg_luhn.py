import my_logger


def alg_luhn(number: str) -> bool:
    """Алгоритм луна"""
    logger = my_logger.My_log(__file__).get_logger()
    summa = 0
    for index in range(len(number)):
        if index % 2 != 1:
            even_number = int(number[index]) * 2
            if even_number > 9:
                summa += even_number - 9
            else:
                summa += even_number
        else:
            summa += int(number[index])
    if summa % 10 == 0:
        logger.info("The lunch algorithm was successful. The card number is correct")
        return True
    else:
        logger.warning("The sequence failed the luhn check. Check it out")
        return False
