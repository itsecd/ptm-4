import hashlib
import multiprocessing as mp

hash_func = {'blake2b': hashlib.blake2b,
                  'md5': hashlib.md5,
                  'blake2s': hashlib.blake2s,
                  'sha1': hashlib.sha1,
                  'sha224': hashlib.sha224,
                  'sha256': hashlib.sha256,
                  'sha384': hashlib.sha384,
                  'sha512': hashlib.sha512,
                  'sha3_224': hashlib.sha3_224,
                  'sha3_256': hashlib.sha3_256,
                  'sha3_384': hashlib.sha3_384,
                  'sha3_512': hashlib.sha3_512,
                  'md5': hashlib.md5
                  }
def check_hash(lst: list) -> str:
    """Сравниваем хэши, в случае успеха возвращаем номер карты, иначе False"""
    hash = lst[3]
    full_card_num = f"{lst[0]}{lst[1]:06d}{lst[2]}"
    if hash_func[lst[4]](full_card_num.encode()).hexdigest() == hash:
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
