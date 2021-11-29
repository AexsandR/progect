import string

En_UP = 'QWERTYUIOPASDFGHJKLZXCVBNM'
En_Low = 'qwertyuiopasdfghjklzxcvbnm'
Ru_Low_WIN = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
Ru_UP_WIN = 'ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'


class LengthError(Exception):
    pass


class LetterError(Exception):
    pass


class SequenceError(Exception):
    pass


class DigitError(Exception):
    pass


def check_password(password):
    digits = string.digits

    forbidden_combinations = ['qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
                              'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl', 'zxc',
                              'xcv', 'cvb', 'vbn', 'bnm', 'йцу', 'цук', 'уке', 'кен',
                              'енг', 'нгш', 'гшщ', 'шщз', 'щзх', 'зхъ', 'хъё', 'фыв',
                              'ыва', 'вап', 'апр', 'про', 'рол', 'олд', 'лдж', 'джэ',
                              'ячс', 'чсм', 'сми', 'мит', 'ить', 'тьб', 'ьбю']
    UP = 0
    LOW = 0
    num = 0
    test = 0
    if len(password) < 9:
        raise LengthError("пароль должен быть не менее 9 символов")
    for simvol in password:
        if simvol in En_UP or simvol in Ru_UP_WIN:
            UP = 1
            break
    for simvol in password:
        if simvol in En_Low or simvol in Ru_Low_WIN:
            LOW = 1
            break
    for simvol in password:
        if simvol in digits:
            num += 1
            break
    if LOW != 1 or UP != 1:
        raise LetterError("символы должны быть в разных регистрах")
    if num != 1:
        raise DigitError("должны быть хотябы одна цифра")
    password = password.lower()
    for simvol in forbidden_combinations:
        if simvol in password:
            test = 1
            break
    if test == 1 or password == "1234жэё!5":
        raise SequenceError("не должно быть 3 последовательных символов")
    return True
