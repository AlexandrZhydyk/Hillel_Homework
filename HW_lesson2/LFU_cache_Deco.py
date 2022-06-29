import functools
import requests


def cache(max_limit=3):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            # Увеличение counter при повторном запросе
            if cache_key in deco._cache:
                deco._cache[cache_key]["counter"] += 1
                return deco._cache[cache_key]["rez"]
            # Удаление элемента при достижении лимита
            if len(deco._cache) >= max_limit:
                del deco._cache[min(deco._cache, key=lambda x: deco._cache[x]["counter"])]
            # Добавление нового элемента
            deco._cache[cache_key] = {}
            result = f(*args, **kwargs)
            deco._cache[cache_key]["counter"] = 1
            deco._cache[cache_key]["rez"] = result
            print(deco._cache)
            return result

        deco._cache = {}
        return deco

    return internal


@cache()
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


if __name__ == '__main__':
    # Без цієї конструкції імпортований модуль виконується одразу при імпорті
    # У більшості випадків треба використовувати цю конструкцію та викликати
    # об'явлені функції у ній.
    #
    # У PyCharm є шорткат для цього. Просто пишеш "main" та Enter
    print(fetch_url("https://www.google.com"))
    print(fetch_url("https://www.google.com/maps"))
    print(fetch_url("https://www.youtube.com"))
    print(fetch_url("https://www.google.com/maps"))
    print(fetch_url("https://www.google.com/maps"))
    print(fetch_url("https://www.youtube.com"))
    print(fetch_url("https://github.com"))
