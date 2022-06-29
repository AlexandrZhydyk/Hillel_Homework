import psutil
import functools
import requests


def mem_measur(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Создаем экземпляр класса, передавая ему id текущего процесса
        process = psutil.Process()  # Можна не передавати pid в аргумент конструктора. Він візьме поточній pid.
        # Размер выделенной памяти до выполнения ф-ции
        init_memo = process.memory_info().rss  # Краще використовувати імена, а не індекси, якщо є така можливість
        result = func(*args, **kwargs)
        # Размер выделенной памяти после выполнения ф-ции
        end_memo = process.memory_info().rss
        # Занятый размер памяти процессом
        occup_memo = (end_memo - init_memo)
        print(f'Function {func.__name__} takes {occup_memo} bytes')
        return result

    return wrapper


@mem_measur
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
    print(fetch_url("https://www.google.com/maps"))
