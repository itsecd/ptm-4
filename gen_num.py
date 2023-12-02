import hashlib
import multiprocessing as mp

def check_hash(lst: list) -> str:
    """Сравниваем хэши, в случае успеха возвращаем номер карты, иначе False"""
    hash = lst[3]
    full_card_num = f"{lst[0]}{lst[1]:06d}{lst[2]}"
    match lst[4]:
        case 'blake2b':
            if hashlib.blake2b(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'blake2s':
            if hashlib.blake2s(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha1':
            if hashlib.sha1(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha224':
            if hashlib.sha224(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha256':
            if hashlib.sha256(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha384':
            if hashlib.sha384(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha3_224':
            if hashlib.sha3_224(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha3_256':
            if hashlib.sha3_256(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha3_384':
            if hashlib.sha3_384(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha3_512':
            if hashlib.sha3_512(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'sha512':
            if hashlib.sha512(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
        case 'md5':
            if hashlib.md5(full_card_num.encode()).hexdigest() == hash:
                return full_card_num
    return False


def num_selection(data: dict, core) -> str:
    """Перебираем номера карт, (прогоняем каждый номер через функцию выше) в случае успеха возвращаем номер карты"""
    arguments_for_check_hash = [[data["bins"][j], i, data["last_num"], data["hash"],
                                 data["hash_format"]] for j in range(len(data["bins"])) for i in range(10 ** 6)]
    with mp.Pool(processes=core) as p:
        for full_card_num in p.map(check_hash, arguments_for_check_hash):
            if full_card_num:
                p.terminate()
                print(full_card_num)
                return full_card_num

