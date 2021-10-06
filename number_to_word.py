currencies = {
    'EUR': ('euro', 'centów'),
    'PLN': ('złotych', 'groszy'),
    'GBP': ('funtów', 'pensów')
}


def number_to_word(number, currency='EUR'):
    jednostki = {
        1: 'jeden',
        2: 'dwa',
        3: 'trzy',
        4: 'cztery',
        5: 'pięć',
        6: 'sześć',
        7: 'siedem',
        8: 'osiem',
        9: 'dziewięć'
    }
    nastki = {
        1: 'jedenaście',
        2: 'dwanaście',
        3: 'trzynaście',
        4: 'czternaście',
        5: 'piętnaście',
        6: 'szesnaście',
        7: 'siedemnaście',
        8: 'osiemnaście',
        9: 'dziewiętnaście'
    }
    dziesiatki = {
        1: 'dziesięć',
        2: 'dwadzieścia',
        3: 'trzydzieści',
        4: 'czterdzieści',
        **{v: jednostki[v] + 'dziesiąt' for v in range(5, 10)}
    }
    setki = {
        1: 'sto',
        2: 'dwieście',
        3: 'trzysta',
        4: 'czterysta',
        **{v: jednostki[v] + 'set' for v in range(5, 10)}
    }
    tysiace = {
        1: 'tysiąc',
        2: 'tysiące',
        3: 'tysiące',
        4: 'tysiące'
    }
    ret = []
    if number // 10 ** 6:
        ret.append('milion')
        number %= 10 ** 6
    if number // 10 ** 5:
        tmp = number // 10 ** 5
        ret.append(setki[tmp])
        number %= 10 ** 5
    if number // 10 ** 4:
        tmp = number // 10 ** 4
        ret.append(dziesiatki[tmp])
        number %= 10 ** 4
    if number // 10 ** 3:
        tmp = number // 10 ** 3
        ret.extend([jednostki[tmp], tysiace.get(tmp, 'tysięcy')])
        number %= 10 ** 3
    if number // 10 ** 2:
        tmp = number // 10 ** 2
        ret.append(setki[tmp])
        number %= 10 ** 2
    if number // 10:
        tmp = number // 10
        jed = int(number % 10)
        if tmp > 1 or jed == 0:
            ret.append(dziesiatki[tmp])
            if jed > 0:
                ret.append(jednostki[jed])
        else:
            ret.append(nastki[jed])
    elif int(number % 10):
        ret.append(jednostki[int(number % 10)])
    reszta = f'{number % 1 * 100:0.0f}'
    waluta, koncowki = currencies[currency]
    calak = ' '.join(ret)
    pt1 = f'{calak} {waluta}'
    if reszta != '0':
        pt1 += f' i {reszta} {koncowki}'
    return pt1
