import logging


def alg_luhn(number: str) -> bool:
    """Алгоритм луна"""
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
        print("Последовательность верна")
        return True
    else:
        print("Последовательность не верна")
        return False
