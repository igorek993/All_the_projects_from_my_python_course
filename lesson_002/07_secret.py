#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть зашифрованное сообщение

secret_message = [
    'квевтфпп6щ3стмзалтнмаршгб5длгуча',
    'дьсеы6лц2бане4т64ь4б3ущея6втщл6б',
    'т3пплвце1н3и2кд4лы12чф1ап3бкычаь',
    'ьд5фму3ежородт9г686буиимыкучшсал',
    'бсц59мегщ2лятьаьгенедыв9фк9ехб1а',
]

# Нужно его расшифровать и вывести на консоль в удобочитаемом виде.
# Должна получиться фраза на русском языке, например: как два байта переслать.

# Ключ к расшифровке:
#   первое слово - 4-я буква
#   второе слово - буквы с 10 по 13, включительно
#   третье слово - буквы с 6 по 15, включительно, через одну
#   четвертое слово - буквы с 8 по 13, включительно, в обратном порядке
#   пятое слово - буквы с 17 по 21, включительно, в обратном порядке
#
# Подсказки:
#   В каждом элементе списка защифровано одно слово.
#   Требуется задать конкретные индексы, например secret_message[3][12:23:4]
#   Если нужны вычисления и разные пробы - делайте это в консоли пайтона, тут нужен только результат

word1 = secret_message[0][3]
word2 = secret_message[1][9:13]
word3 = secret_message[2][5:15:2]
word4 = secret_message[3][7:13:-1]
word5 = secret_message[4][16:21:-1]
#  Похоже произошло недопонимание: "двойной" слайс был примером неверного слайса (и это было именно аналог того,
#  прошлого варианта) нужен одинарный вот такой:
#  any_string[12:6-1]
#  Обратите внимание, что при отрицательном шаге направление "движения" меняется, и, соответственно, указатели начала и
#  конца слайса тоже меняются местами
print(word1, word2, word3, word4, word5)


#  Thank you for the explanation, I did understood you correctly for the very first time! :) And I also new from
#  the very beginning that this is the way I should have done this task... the issue is that if I write it like this
#  ''print( secret_message[4][16:21:-1])'' pycharm does not show anything in my console after executing the code,
#  it just ignores the string. I think our teacher faced the same issue during his class as well. What is the right
#  way I should do it so it pops up in the console? You can run it and take a look by yourself...

print('tricky slice that does not show anything:', secret_message[4][16:21:-1])
# TODO As I pointed you last time, you should use reversed order of indexes due to negative step, like this:
print('magic tricky slice:', secret_message[4][21:16:-1])
