import time
import string
import secrets
import random
import hashlib
import os

base_dir = os.path.dirname(__file__)

def key_fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()[:8]


cipher = {
    "F": "Ğ%)ü",
    "G": "@2!Va",
    "Ğ": ">z<20a",
    "I": "*3b,",
    "O": "9e$bAğ",
    "D": "*S*3/zÇ",
    "R": "$$5vPlt",
    "N": "N@ghaT!$y",
    "H": "Hæt!y$",
    "P": "7$!1€",
    "Q": "K>ü$g5%",
    "U": "8₺a!vö",
    "İ": "æ3!n1",
    "E": "5#v6&",
    "A": "!m",
    "Ü": "Ü1k!$ç$z",
    "T": "T@!y$",
    "K": "#34æb!",
    "M": "{½!4bA",
    "L": "!₺nAb",
    "Y": "!A56½#",
    "Ş": "*>vdf",
    "J": "CaN£#g1",
    "Ö": "Ö!bN$2",
    "V": ")7mÖ$3",
    "C": "½e",
    "Ç": "1m#3",
    "Z": "9Bæ!Æç",
    "S": "Sæ€}",
    "B": "?v"
}

number_to_letter = {
    1: "A",  2: "E",  3: "T",  4: "K",  5: "M",
    6: "L",  7: "Y",  8: "Ş",  9: "I", 10: "O",
    11: "R", 12: "N", 13: "D", 14: "S", 15: "B",
    16: "Ü", 17: "İ", 18: "Z", 19: "Ç", 20: "G",
    21: "C", 22: "P", 23: "H", 24: "F", 25: "V",
    26: "Ö", 27: "Ğ", 28: "J"
}

letter_to_number = {v: k for k, v in number_to_letter.items()}
reverse_cipher = {v: k for k, v in cipher.items()}



_KELIME_CACHE = None


def kelimeler_dosyadan_yukle():
    global _KELIME_CACHE
    if _KELIME_CACHE is None:
        try:
            base_dir = os.path.dirname(__file__)
            path = os.path.join(base_dir, "kelimeler.txt")
            with open(path, "r", encoding="utf-8") as f:
                _KELIME_CACHE = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            _KELIME_CACHE = []
    return _KELIME_CACHE


def kelime_sec(search_term: str) -> str:
    kelimeler = kelimeler_dosyadan_yukle()
    if not kelimeler:
        return "kelime"

    h = hashlib.sha256(search_term.encode()).hexdigest()
    idx = int(h, 16) % len(kelimeler)
    return kelimeler[idx]



def tpc_yukle(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if lines[0] != "[TPC-1]":
        raise ValueError("Desteklenmeyen TPC sürümü")

    data = {}
    for ln in lines[1:]:
        k, v = ln.split("=", 1)
        data[k] = v

    words = data["WORDS"].split(",")
    symbols = data["SYMBOLS"].split(",")
    key_id = data["KEY_ID"]

    return words, symbols, key_id


def tpc_kaydet(filename: str, words: list, symbols: list, key: str):
    key_id = key_fingerprint(key)

    content = (
        "[TPC-1]\n"
        f"KEY_ID={key_id}\n"
        "ENC_TYPE=4FE\n"
        "WORDS=" + ",".join(words) + "\n"
        "SYMBOLS=" + ",".join(symbols) + "\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def key_olustur(length=32) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def symbol_to_search_term(symbol: str, key: str) -> str:
    return hashlib.sha256((symbol + key).encode()).hexdigest()[:3]



def encrypt_4fe(text: str, key: str):
    if len(key) < 8:
        raise ValueError("Anahtar çok kısa")

    text = text.upper()
    result_words = []
    symbol_list = []

    for ch in text:
        num = letter_to_number.get(ch)
        if not num:
            continue

        letter = number_to_letter[num]
        symbol = cipher[letter]

        search_term = symbol_to_search_term(symbol, key)
        word = kelime_sec(search_term)

        result_words.append(word)
        symbol_list.append(symbol)

    return result_words, symbol_list


FAILED_ATTEMPTS = 0

def decrypt_4fe(words: list, key: str) -> str:
    global FAILED_ATTEMPTS
    result = ""

    for word in words:
        found_symbol = None

        for sym in cipher.values():
            term = symbol_to_search_term(sym, key)
            if kelime_sec(term) == word:
                found_symbol = sym
                break

        if not found_symbol:
            FAILED_ATTEMPTS += 1
            time.sleep(min(FAILED_ATTEMPTS, 5))
            return "Yanlış anahtar!"

        result += reverse_cipher[found_symbol]

    FAILED_ATTEMPTS = 0
    return result


def decrypt_4fe_offline(symbols: list) -> str:
    return "".join(reverse_cipher[s] for s in symbols)
