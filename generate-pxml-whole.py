#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import xml.etree.ElementTree as ET

# 1) Папки для результату
BASE_DIR = os.path.join("static", "roman-uk", "xml", "pxml")
DAY_DIR = os.path.join(BASE_DIR, "day")
MONTH_DIR = os.path.join(BASE_DIR, "month")

for folder in (DAY_DIR, MONTH_DIR):
    os.makedirs(folder, exist_ok=True)

# 2) Визначимо допоміжні словники та функції

# Приклад: карта урочистостей для січня (потрібно доповнити по всіх місяцях)
LITURGICAL_CALENDAR_UK = {
    '2025-01-01': ('<span>Пресвятої Діви Марії, Матері Божої</span>','B', 52, 1, 2, 'Різдвяний період', 2, 'Урочистість', 'Соломітність', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:0]{index=0}
    '2025-01-02': ('<span>Святих Василія Великого і Григорія Богослова, єпископів і вчителів</span>','B', 1, 2, 2, 'Різдвяний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:1]{index=1}
    '2025-01-03': ('<span>Свято Пресвятого Імені Ісуса</span>','B', 1, 2, 2, 'Різдвяний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:2]{index=2}
    '2025-01-04': ('<span>Вівторок після Богоявлення</span>','B', 1, 2, 2, 'Різдвяний період', 0, 'Буденний день', 'Буденний', 'Необов’язковий', 4, 'Фіолетовий', 'всеукраїнський', '01I'),
    '2025-01-05': ('<span>Субота після Богоявлення</span>','B', 1, 2, 2, 'Різдвяний період', 0, 'Буденний день', 'Буденний', 'Необов’язковий', 4, 'Фіолетовий', 'всеукраїнський', '01I'),
    '2025-01-06': ('<span>Богоявлення Господнє</span>','B', 2, 3, 2, 'Різдвяний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:3]{index=3}
    '2025-01-12': ('<span>Хрещення Господнього</span>','B', 2, 3, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:4]{index=4}
    '2025-01-17': ('<span>Святого Антонія, абата</span>','B', 2, 4, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 4, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:5]{index=5}
    '2025-01-21': ('<span>Святої Агнеси, діви і мучениці</span>','B', 2, 4, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:6]{index=6}
    '2025-01-24': ('<span>Святого Франциска де Сейса, єпископа і доктора церкви</span>','B', 2, 4, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:7]{index=7}
    '2025-01-25': ('<span>Перетворення Святого Павла, апостола</span>','B', 2, 4, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:8]{index=8}
    '2025-01-26': ('<span>Третя неділя звичайного періоду</span>','B', 2, 4, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 3, 'Зелений', 'всеукраїнський', '02I'),  #:contentReference[oaicite:9]{index=9}
    '2025-02-02': ('<span>Стрітення Господнє</span>','B', 3, 4, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:10]{index=10}
    '2025-02-14': ('<span>Святих Кирила, монаха, і Мефодія, єпископа, учителів слов’янських</span>','B', 3, 6, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:11]{index=11}
    '2025-02-24': ('<span>Свята Покрова Пресвятої Богородиці</span>','B', 3, 7, 5, 'Звичайний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:12]{index=12}
    '2025-03-03': ('<span>Святих Перпетуї та Феліксів, мучеників</span>','B', 3, 8, 3, 'Піст', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:13]{index=13}
    '2025-03-08': ('<span>Святий Йоан Богослов</span>','B', 3, 9, 3, 'Піст', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:14]{index=14}
    '2025-03-09': ('<span>Перша неділя Великого посту</span>','B', 3, 9, 3, 'Піст', 1, 'Неділя', 'Неділя', 'Обов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:15]{index=15}
    '2025-03-17': ('<span>Святого Патріка, єпископа</span>','B', 3, 10, 3, 'Піст', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:16]{index=16}
    '2025-03-19': ('<span>Собор Святого Йосифа, Обручника Пресвятої Богородиці</span>','B', 3, 10, 3, 'Піст', 2, 'Урочистість', 'Урочистість', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '03I'),  #:contentReference[oaicite:17]{index=17}
    '2025-03-25': ('<span>Благовіщення Пресвятої Богородиці</span>','B', 3, 11, 3, 'Піст', 2, 'Урочистість', 'Урочистість', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:18]{index=18}
    '2025-03-30': ('<span>Четверта неділя Великого посту (Летарія)</span>','B', 3, 12, 3, 'Піст', 1, 'Неділя', 'Неділя', 'Обов’язковий', 4, 'Рожевий', 'всеукраїнський', '04I'),  #:contentReference[oaicite:19]{index=19}
    '2025-04-06': ('<span>П’ята неділя Великого посту</span>','B', 4, 13, 3, 'Піст', 1, 'Неділя', 'Неділя', 'Обов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:20]{index=20}
    '2025-04-13': ('<span>Вербна неділя (Неділя Господнього Страстей)</span>','B', 4, 14, 3, 'Піст', 1, 'Неділя', 'Неділя', 'Обов’язковий', 4, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:21]{index=21}
    '2025-04-17': ('<span>Великий четвер</span>','B', 4, 15, 4, 'Пасхальне тридення', 2, 'Урочистість', 'Урочистість', 'Обов’язковий', 4, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:22]{index=22}
    '2025-04-18': ('<span>Страсна п’ятниця</span>','B', 4, 15, 4, 'Пасхальне тридення', 2, 'Урочистість', 'Урочистість', 'Обов’язковий', 5, 'Чорний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:23]{index=23}
    '2025-04-19': ('<span>Великодня субота</span>','B', 4, 15, 4, 'Пасхальне тридення', 2, 'Урочистість', 'Урочистість', 'Обов’язковий', 4, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:24]{index=24}
    '2025-04-20': ('<span>Воскресіння Господа нашого Ісуса Христа (Великдень)</span>','B', 4, 16, 4, 'Великодній період', 2, 'Урочистість', 'Соломітність', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:25]{index=25}
    '2025-04-27': ('<span>Друга неділя після Великодня (Божественного милосердя)</span>','B', 4, 17, 4, 'Великодній період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '04I'),  #:contentReference[oaicite:26]{index=26}
    '2025-05-01': ('<span>Святого Йосифа Трудяги</span>','B', 4, 17, 4, 'Великодній період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:27]{index=27}
    '2025-05-02': ('<span>Св. Афанасій, єпископ та вчитель церкви</span>','B', 4, 17, 4, 'Великодній період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:28]{index=28}
    '2025-05-03': ('<span>Святих Филипа та Якова, апостолів</span>','B', 4, 18, 4, 'Великодній період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:29]{index=29}
    '2025-05-04': ('<span>Третя неділя після Великодня</span>','B', 4, 18, 4, 'Великодній період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:30]{index=30}
    '2025-05-08': ('<span>Св. Станіслава, єпископа і мученика</span>','B', 4, 18, 4, 'Великодній період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:31]{index=31}
    '2025-05-11': ('<span>Четверта неділя після Великодня</span>','B', 4, 19, 4, 'Великодній період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '04I'),  #:contentReference[oaicite:32]{index=32}
    '2025-05-26': ('<span>Пресвятих Тіла і Крові Христових</span>','B', 5, 21, 4, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:33]{index=33}
    '2025-06-08': ('<span>П’ятидесятниця (Свято Зіслання Святого Духа)</span>','B', 5, 22, 5, 'Звичайний період', 2, 'Неділя', 'Соломітність', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:34]{index=34}
    '2025-06-09': ('<span>Пресвятої Діви Марії Цариці Неба</span>','B', 5, 22, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:35]{index=35}
    '2025-06-11': ('<span>Св. Варнави, апостола</span>','B', 5, 22, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:36]{index=36}
    '2025-06-12': ('<span>Св. Івана з Матоки, вічного Первосвященика</span>','B', 5, 22, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:37]{index=37}
    '2025-06-13': ('<span>Св. Антонія Падуанського, священика і доктора Церкви</span>','B', 5, 22, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:38]{index=38}
    '2025-06-15': ('<span>Недiля Святої Тройцi</span>','B', 5, 23, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:39]{index=39}
    '2025-06-21': ('<span>Св. Луїги Гонзаги, монаха</span>','B', 5, 24, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:40]{index=40}
    '2025-06-22': ('<span>Пресвятих Тіла і Крові Христових</span>','B', 5, 24, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Червоний', 'всеукраїнський', '04I'),  #:contentReference[oaicite:41]{index=41}
    '2025-06-24': ('<span>Народження Івана Хрестителя</span>','B', 5, 25, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:42]{index=42}
    '2025-06-27': ('<span>Св. Іринея, єпископа, мученика і доктора Церкви</span>','B', 5, 25, 5, 'Звичайний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:43]{index=43}
    '2025-06-28': ('<span>Неділя 13-та звичайного періоду</span>','B', 5, 26, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 3, 'Зелений', 'всеукраїнський', '01I'),
    '2025-07-03': ('<span>Св. Томаса, апостола</span>','B', 5, 27, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:44]{index=44}
    '2025-07-04': ('<span>Св. Єлизавети Португальської</span>','B', 5, 27, 5, 'Звичайний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:45]{index=45}
    '2025-07-06': ('<span>Чотирнадцята неділя звичайного періоду</span>','B', 5, 28, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:46]{index=46}
    '2025-07-11': ('<span>Св. Бенедикта, абата</span>','B', 5, 28, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:47]{index=47}
    '2025-07-13': ('<span>П’ятнадцята неділя звичайного періоду</span>','B', 5, 29, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 3, 'Зелений', 'всеукраїнський', '03I'),  #:contentReference[oaicite:48]{index=48}
    '2025-07-15': ('<span>Св. Йоакима і Анни, батьків Пресвятої Богородиці</span>','B', 5, 30, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:49]{index=49}
    '2025-07-25': ('<span>Св. Якова, апостола</span>','B', 5, 31, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:50]{index=50}
    '2025-07-26': ('<span>Св. Анни, матері Пресвятої Богородиці</span>','B', 5, 31, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:51]{index=51}
    '2025-07-28': ('<span>Чотирнадцята неділя звичайного періоду</span>','B', 5, 32, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 3, 'Зелений', 'всеукраїнський', '01I'),
    '2025-08-01': ('<span>Св. Альфонса Лігуорі, єпископа і доктора Церкви</span>','B', 5, 33, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:52]{index=52}
    '2025-08-04': ('<span>Св. Йоана Марії Віаннея, священика</span>','B', 5, 33, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:53]{index=53}
    '2025-08-06': ('<span>Преображення Господнє</span>','B', 5, 33, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:54]{index=54}
    '2025-08-09': ('<span>Св. Онуфрія, пустельника</span>','B', 5, 34, 5, 'Звичайний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:55]{index=55}
    '2025-08-10': ('<span>Св. Терези Авільської, діви і доктора церкви</span>','B', 5, 34, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:56]{index=56}
    '2025-08-14': ('<span>Св. Максима Кольбе, священика і мученика</span>','B', 5, 34, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:57]{index=57}
    '2025-08-15': ('<span>Успіння Пресвятої Богородиці</span>','B', 5, 34, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:58]{index=58}
    '2025-08-22': ('<span>Св. Піо з П’єтрельчіни, священика</span>','B', 5, 35, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:59]{index=59}
    '2025-09-08': ('<span>Народження Пресвятої Богородиці</span>','B', 6, 37, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:60]{index=60}
    '2025-09-14': ('<span>Воздвиження Чесного Хреста</span>','B', 6, 38, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 4, 'Фіолетовий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:61]{index=61}
    '2025-09-21': ('<span>Св. Матвія, апостола</span>','B', 6, 39, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:62]{index=62}
    '2025-09-29': ('<span>Св. Михайла, Гавриїла, Рафаїла, архангелів</span>','B', 6, 39, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:63]{index=63}
    '2025-10-04': ('<span>Св. Франциска Ассизького</span>','B', 6, 40, 5, 'Звичайний період', 3, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:64]{index=64}
    '2025-10-07': ('<span>Св. Розарію Пресвятої Богородиці</span>','B', 6, 40, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:65]{index=65}
    '2025-10-18': ('<span>Св. Луки, євангелиста</span>','B', 6, 40, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '01I'),  #
    '2025-10-28': ('<span>Св. Симона і Св. Юди, апостолів</span>','B', 6, 41, 5, 'Звичайний період', 3, 'Свято', 'Свято', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '02I'),  #:contentReference[oaicite:67]{index=67}
    '2025-11-01': ('<span>Усіх Святих</span>','B', 6, 41, 5, 'Звичайний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:68]{index=68}
    '2025-11-02': ('<span>Всіх померлих християн (Душпастирська річниця)</span>','B', 6, 41, 5, 'Звичайний період', 1, 'Неділя', 'Неділя', 'Обов’язковий', 4, 'Фіолетовий', 'всеукраїнський', '03I'),  #:contentReference[oaicite:69]{index=69}
    '2025-11-05': ('<span>Св. Леонтія Кола, єпископа</span>','B', 6, 42, 5, 'Звичайний період', 3, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Фіолетовий', 'всеукраїнський', '01I'),
    '2025-11-11': ('<span>Св. Мартина Турського, єпископа</span>','B', 6, 42, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:70]{index=70}
    '2025-11-13': ('<span>Св. Йосафата, єпископа і мученика</span>','B', 6, 42, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:71]{index=71}
    '2025-11-21': ('<span>Введення в храм Пресвятої Богородиці</span>','B', 6, 43, 5, 'Звичайний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:72]{index=72}
    '2025-11-22': ('<span>Св. Цецилії, діви і мучениці</span>','B', 6, 43, 5, 'Звичайний період', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 2, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:73]{index=73}
    '2025-11-23': ('<span>Неділя Христового Царства</span>','B', 6, 43, 5, 'Звичайний період', 2, 'Неділя', 'Неділя', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:74]{index=74}
    '2025-12-06': ('<span>Св. Миколая, єпископа</span>','B', 6, 46, 1, 'Адвент', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),  #:contentReference[oaicite:75]{index=75}
    '2025-12-08': ('<span>Непорочне Зачаття Пресвятої Богородиці</span>','B', 6, 47, 1, 'Адвент', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '02I'),  #:contentReference[oaicite:76]{index=76}
    '2025-12-12': ('<span>Св. Хустини Борджіа, діви</span>','B', 6, 47, 1, 'Адвент', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),
    '2025-12-13': ('<span>Св. Люції, діви і мучениці</span>','B', 6, 47, 1, 'Адвент', 4, 'Спомин', 'Спомин обов’язковий', 'Обов’язковий', 3, 'Червоний', 'всеукраїнський', '01I'),  #:contentReference[oaicite:77]{index=77}
    '2025-12-21': ('<span>Четверта неділя Адвенту</span>','B', 6, 48, 1, 'Адвент', 1, 'Неділя', 'Неділя', 'Обов’язковий', 4, 'Рожевий', 'всеукраїнський', 'IV'),
    '2025-12-25': ('<span>Народження Господа нашого Ісуса Христа (Різдво Христове)</span>','B', 1, 48, 2, 'Різдвяний період', 2, 'Урочистість', 'Соломітність', 'Обов’язковий', 1, 'Білий', 'всеукраїнський', '01I'),
    '2025-12-26': ('<span>Собор Пресвятої Богородиці (Св. Стефана, першомученика)</span>','B', 1, 49, 2, 'Різдвяний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Червоний', 'всеукраїнський', '01I'),
    '2025-12-27': ('<span>Св. Іоана Богослова, апостола</span>','B', 1, 49, 2, 'Різдвяний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Червоний', 'всеукраїнський', '01I'),
    '2025-12-28': ('<span>Святих Немовлят, мучеників</span>','B', 1, 49, 2, 'Різдвяний період', 2, 'Урочистість', 'Свято', 'Обов’язковий', 1, 'Червоний', 'всеукраїнський', '01I'),
    '2025-12-31': ('<span>Старий рік (Свято Святого Сильвестра)</span>','B', 1, 49, 2, 'Різдвяний період', 4, 'Спомин', 'Необов’язковий', 'Необов’язковий', 2, 'Червоний', 'всеукраїнський', '01I'),
}


# Для випадку, коли в словнику немає конкретної дати, створюємо “звичайну форму” (ферія у  Святому часі)
def get_celebration_for(date: datetime.date):
    key = date.strftime("%Y-%m-%d")
    if key in LITURGICAL_CALENDAR_UK:
        title_html, year_letter, week_psalms, week_of_psalter, season_id, season_name, ctype_id, ctype_name, clevel, crequired, color_id, color_name, calendar_name, readings_id = LITURGICAL_CALENDAR_UK[key]
    else:
        # За замовчуванням — звичайна ферія (Cезон залежить від пори року)
        # Наприклад, припустимо: Cezročné obdobie, буква року “C”, тиждень = None, колір “зелена”
        title_html = "<span class=\"bold\"><span class=\"uppercase\">Ферія</span></span><br/><span class=\"small\">Cezročné obdobie</span>"
        year_letter = "C"
        week_psalms = None
        week_of_psalter = None
        season_id = 5
        season_name = "Звичайний день"
        ctype_id = 0
        ctype_name = "звичайний день"
        clevel = 2
        crequired = 1
        color_id = 3
        color_name = "зелена"
        calendar_name = "всеукраїнський"
        readings_id = date.strftime("%dC")  # просто за замовчуванням, щоб не було порожнього поля
    return {
        "StringTitle": title_html,
        "LiturgicalYearLetter": year_letter,
        "LiturgicalWeek": week_psalms or "",
        "LiturgicalWeekOfPsalter": week_of_psalter or "",
        "LiturgicalSeasonId": season_id,
        "LiturgicalSeasonName": season_name,
        "CelebrationTypeId": ctype_id,
        "CelebrationTypeName": ctype_name,
        "CelebrationLevel": clevel,
        "CelebrationRequired": crequired,
        "CelebrationColorId": color_id,
        "CelebrationColorName": color_name,
        "LiturgicalCalendar": calendar_name,
        "LiturgicalReadingsId": readings_id,
    }


# Будемо їх використовувати для побудови тега <Celebration>
def build_celebration_element(parent, data: dict):
    celebr = ET.SubElement(parent, "Celebration")
    ET.SubElement(celebr, "Id").text = "0"
    # StringTitle — передамо як CDATA всередину тегу
    st = ET.SubElement(celebr, "StringTitle")
    st.text = None
    st.append(ET.Comment("<![CDATA[%s]]>" % data["StringTitle"]))
    ET.SubElement(celebr, "LiturgicalYearLetter").text = data["LiturgicalYearLetter"]
    ET.SubElement(celebr, "LiturgicalWeek").text = str(data["LiturgicalWeek"])
    ET.SubElement(celebr, "LiturgicalWeekOfPsalter").text = str(data["LiturgicalWeekOfPsalter"])
    ET.SubElement(celebr, "LiturgicalSeason", {"Id": str(data["LiturgicalSeasonId"])}).text = data["LiturgicalSeasonName"]
    ET.SubElement(celebr, "LiturgicalCelebrationType", {"Id": str(data["CelebrationTypeId"])}).text = data["CelebrationTypeName"]
    ET.SubElement(celebr, "LiturgicalCelebrationTypeLocal").text = ""
    ET.SubElement(celebr, "LiturgicalCelebrationLevel").text = str(data["CelebrationLevel"])
    ET.SubElement(celebr, "LiturgicalCelebrationRequired").text = str(data["CelebrationRequired"])
    ET.SubElement(celebr, "LiturgicalCelebrationName").text = ""
    ET.SubElement(celebr, "LiturgicalCelebrationColor", {"Id": str(data["CelebrationColorId"])}).text = data["CelebrationColorName"]
    ET.SubElement(celebr, "LiturgicalCalendar").text = data["LiturgicalCalendar"]
    ET.SubElement(celebr, "LiturgicalReadingsId").text = data["LiturgicalReadingsId"]


# Опція – генерація “набірних параметрів” на рівні <Options> можна копіювати як є.
OPTIONS_BLOCK = """<Options>
  <Opt0Special Value="549507" Name="o0" ForceName="of0" Text="налаштування для літургійного календаря">
    <BitOpt0VerseNumbers Id="1" ForceName="of0v" Text="нумерація віршів">1</BitOpt0VerseNumbers>
    <BitOpt0References Id="2" ForceName="of0r" Text="біблійні посилання з dkc.kbs.sk">1</BitOpt0References>
    <BitOpt0Readings Id="4" ForceName="of0cit" Text="читання в Месі">0</BitOpt0Readings>
    <BitOpt0EpiphanyOnSunday Id="8" ForceName="of0zjvne" Text="Світло Воплочення святкувати в неділю між 2 і 8 січня">0</BitOpt0EpiphanyOnSunday>
    <BitOpt0AssumptionOnSunday Id="16" ForceName="of0nanne" Text="Вознесіння святкувати в неділю">0</BitOpt0AssumptionOnSunday>
    <BitOpt0CorpusChristiOnSunday Id="32" ForceName="of0tkne" Text="Тіло і Кров Христові святкувати в неділю">0</BitOpt0CorpusChristiOnSunday>
    <BitOpt0ForceNormalFontWeight Id="64" ForceName="of0fn" Text="усюди використовувати простий шрифт">0</BitOpt0ForceNormalFontWeight>
    <BitOpt0ButtonsOrder Id="128" ForceName="of0bo" Text="кнопки навігації під читаннями">1</BitOpt0ButtonsOrder>
    <BitOpt0VoiceOutput Id="256" ForceName="of0bf" Text="тільки текст для голосового відтворення">0</BitOpt0VoiceOutput>
    <BitOpt0Footnotes Id="512" ForceName="of0ff" Text="нотатки (підрядок)">1</BitOpt0Footnotes>
    <BitOpt0TransparentNav Id="1024" ForceName="of0tn" Text="прозорі стрілки навігації">0</BitOpt0TransparentNav>
    <BitOpt0PsalmsFullText Id="2048" ForceName="of0zft" Text="повний текст псалмів">0</BitOpt0PsalmsFullText>
    <BitOpt0ReferencesBibleDotCom Id="4096" ForceName="of0bc" Text="біблійні посилання на bible.com">0</BitOpt0ReferencesBibleDotCom>
    <BitOpt0ItalicsConditional Id="8192" ForceName="of0ic" Text="окремі тексти курсивом">1</BitOpt0ItalicsConditional>
    <BitOpt0PrintedEdition Id="16384" ForceName="of0pe" Text="версія за друкованим виданням">1</BitOpt0PrintedEdition>
    <BitOpt0UseTwoYearsCycle Id="32768" ForceName="of0u2rc" Text="двоцикловий цикл читань (biblical readings)">0</BitOpt0UseTwoYearsCycle>
    <BitOpt0TwoYearsCycleInvert Id="65536" ForceName="of02rcinv" Text="зворотний порядок двоциклу">0</BitOpt0TwoYearsCycleInvert>
    <BitOpt0AlternativeReadings Id="131072" ForceName="of02rcinv" Text="альтернативні читання">0</BitOpt0AlternativeReadings>
    <BitOpt0TransparentNavLeft Id="262144" ForceName="of0ltn" Text="стрілки навігації зліва">0</BitOpt0TransparentNavLeft>
    <BitOpt0NavigationMenu Id="524288" ForceName="of0sn" Text="показувати меню навігації">1</BitOpt0NavigationMenu>
    <BitOpt0TransparentNavDownOnly Id="1048576" ForceName="of0dotn" Text="лише стрілка вниз">0</BitOpt0TransparentNavDownOnly>
  </Opt0Special>
  <Opt1PrayerPortions Value="5376" Name="o1" ForceName="of1" Text="налаштування молитв">
    <BitOpt1TeDeum Id="1" ForceName="of1t" Text="гімн Te Deum">0</BitOpt1TeDeum>
    <BitOpt1Rubrics Id="2" ForceName="of1r" Text="рубрики">0</BitOpt1Rubrics>
    <BitOpt1Canticles Id="4" ForceName="of1c" Text="Євангельські речитативи">0</BitOpt1Canticles>
    <BitOpt1GloryPrayer Id="8" ForceName="of1s" Text="Слава Отцю">0</BitOpt1GloryPrayer>
    <BitOpt1OurFatherPrayer Id="16" ForceName="of1o" Text="Отче наш">0</BitOpt1OurFatherPrayer>
    <BitOpt1SupplPsalmodyDuringDay Id="32" ForceName="of1dps" Text="додаткові псалми для молитов дня">0</BitOpt1SupplPsalmodyDuringDay>
    <BitOpt1VigilAfterReadings Id="64" ForceName="of1v" Text="переночна ревірытна молитва">0</BitOpt1VigilAfterReadings>
    <BitOpt1MemoriesTakeFromCommunia Id="128" ForceName="of1spspc" Text="споминки зі спільних текстів">0</BitOpt1MemoriesTakeFromCommunia>
    <BitOpt1FullResponses Id="256" ForceName="of1pr" Text="повні резонзори">1</BitOpt1FullResponses>
    <BitOpt1InvitatoryUsePsalm95 Id="512" ForceName="of1z95" Text="використати псалом 95 замість 24/67/100">0</BitOpt1InvitatoryUsePsalm95>
    <BitOpt1Repeat Id="1024" ForceName="of1prz" Text="повторювати заклик у проханнях">1</BitOpt1Repeat>
    <BitOpt1HideDescription Id="2048" ForceName="of1sp" Text="приховати описи до молитв святих">0</BitOpt1HideDescription>
    <BitOpt1ShowCommuniaDescription Id="4096" ForceName="of1zspc" Text="показати спільні частини">1</BitOpt1ShowCommuniaDescription>
    <BitOpt1UseVespShortenPrayers Id="8192" ForceName="of1vkp" Text="скорочені вечірні молитви">0</BitOpt1UseVespShortenPrayers>
    <BitOpt1PsalmsDuringDayPsalt3Weeks Id="16384" ForceName="of1ps3" Text="триденний псалмодійний цикл">0</BitOpt1PsalmsDuringDayPsalt3Weeks>
    <BitOpt1PrayerConclusions Id="32768" ForceName="of1zm" Text="завершальні молитви">0</BitOpt1PrayerConclusions>
    <BitOpt1OverrideCelebrationLevel Id="65536" ForceName="of1oss" Text="перевизначити рівень святкування">0</BitOpt1OverrideCelebrationLevel>
    <BitOpt1CelebrationLevelForOverride Id="131072" ForceName="of1sss" Text="рівень для перевизначення">0</BitOpt1CelebrationLevelForOverride>
    <BitOpt1ComplineMaryAnt Id="262144" ForceName="of1cma" Text="молитви зі змолоду">0</BitOpt1ComplineMaryAnt>
    <BitOpt1IntroPaterNoster Id="524288" ForceName="of1zou" Text="вступ до Отче наш">0</BitOpt1IntroPaterNoster>
  </Opt1PrayerPortions>
  <Opt2Export Value="29368" Name="o2" ForceName="of2" Text="налаштування сторінок">
    <BitOpt2ISOFormat Id="1" ForceName="of2id" Text="дата в ISO-форматі (YYYY-MM-DD)">0</BitOpt2ISOFormat>
    <BitOpt2FirstVespersButton Id="2" ForceName="of2pv" Text="кнопка перших вечірніх для неділь">0</BitOpt2FirstVespersButton>
    <BitOpt2FontFamily Id="4" ForceName="of2ff" Text="беззасічковий шрифт?">0</BitOpt2FontFamily>
    <BitOpt2FontNameChooser Id="8" ForceName="of2fc" Text="обрати шрифт">1</BitOpt2FontNameChooser>
    <BitOpt2FontSizeChooser Id="16" ForceName="of2fs" Text="розмір шрифту">1</BitOpt2FontSizeChooser>
    <BitOpt2Navigation Id="32" ForceName="of2nav" Text="показати навігацію в текстах">1</BitOpt2Navigation>
    <BitOpt2TextWrap Id="64" ForceName="of2tw" Text="перенос рядків, як у виданні">0</BitOpt2TextWrap>
    <BitOpt2ButtonsCondensed Id="128" ForceName="of2btnu" Text="компактні кнопки">1</BitOpt2ButtonsCondensed>
    <BitOpt2NightMode Id="256" ForceName="of2nr" Text="нічний режим">0</BitOpt2NightMode>
    <BitOpt2OptionsWithinPrayer Id="512" ForceName="of2rm" Text="показати опції всередині молитви">1</BitOpt2OptionsWithinPrayer>
    <BitOpt2HideNavigationButtons Id="1024" ForceName="of2hnb" Text="">0</BitOpt2HideNavigationButtons>
    <BitOpt2HideCalendar Id="2048" ForceName="of2hk" Text="">0</BitOpt2HideCalendar>
    <BitOpt2HideOptionsPart1 Id="4096" ForceName="of2ho1" Text="">1</BitOpt2HideOptionsPart1>
    <BitOpt2HideOptionsPart2 Id="8192" ForceName="of2ho2" Text="">1</BitOpt2HideOptionsPart2>
    <BitOpt2Alternatives Id="16384" ForceName="of2a" Text="альтернативи">1</BitOpt2Alternatives>
    <BitOpt2ShowDefaultCalendar Id="32768" ForceName="of2sdc" Text="показувати національний календар">0</BitOpt2ShowDefaultCalendar>
    <BitOpt2RoundedCorners Id="65536" ForceName="of2sdc" Text="заокруглені кнопки">0</BitOpt2RoundedCorners>
  </Opt2Export>
  <Opt3Communia Value="0" Name="o3" ForceName="of3" Text="спільні частини">не встановлено</Opt3Communia>
  <Opt5Alternatives Value="0" Name="o5" ForceName="of5" Text="альтернативи">
    <BitOpt5HymnCompl Id="1" ForceName="of5hk" Text="гімн для компе">0</BitOpt5HymnCompl>
    <BitOpt5HymnRead Id="2" ForceName="of5hpc" Text="гімн для читання">0</BitOpt5HymnRead>
    <BitOpt5Hymn9h Id="4" ForceName="of5hpred" Text="гімн для вечірні">0</BitOpt5Hymn9h>
    <BitOpt5Hymn12h Id="8" ForceName="of5hna" Text="гімн для обіду">0</BitOpt5Hymn12h>
    <BitOpt5Hymn15h Id="16" ForceName="of5hpo" Text="гімн для вечерні">0</BitOpt5Hymn15h>
    <BitOpt5Psalm122or129 Id="32" ForceName="of5ps29" Text="альтер. псалом 122/129">0</BitOpt5Psalm122or129>
    <BitOpt5Psalm127or131 Id="64" ForceName="of5ps71" Text="альтер. псалом 127/131">0</BitOpt5Psalm127or131>
    <BitOpt5Psalm126or129 Id="128" ForceName="of5ps69" Text="альтер. псалом 126/129">0</BitOpt5Psalm126or129>
    <BitOpt5HymnTPRead Id="256" ForceName="of5vnpc" Text="гімн на вранці">0</BitOpt5HymnTPRead>
    <BitOpt5HymnTPLaud Id="512" ForceName="of5vnhrch" Text="гімн на лаудах">0</BitOpt5HymnTPLaud>
    <BitOpt5HymnTPVesp Id="1024" ForceName="of5vnv" Text="гімн на вечірні">0</BitOpt5HymnTPVesp>
    <BitOpt5Hymn1Vesp Id="2048" ForceName="of5h1v" Text="перша вечірня гімн">0</BitOpt5Hymn1Vesp>
    <BitOpt5AshWednPsalmody Id="4096" ForceName="of5psps" Text="псалми Попільної середи">0</BitOpt5AshWednPsalmody>
    <BitOpt5CZhymnsAlt Id="8192" ForceName="of5czh" Text="альтер. чеські гімни">0</BitOpt5CZhymnsAlt>
    <BitOpt5OffDefPsalm146or150 Id="16384" ForceName="of5ofps60" Text="альтер. псалом 146/150">0</BitOpt5OffDefPsalm146or150>
    <BitOpt5ConclusionPriestDiacon Id="32768" ForceName="of5zkd" Text="заключні молитви">0</BitOpt5ConclusionPriestDiacon>
    <BitOpt5InvitatoryAntWrapOnly Id="65536" ForceName="of5i" Text="не повторювати антифон">0</BitOpt5InvitatoryAntWrapOnly>
    <BitOpt5PerAnnum34Hymns Id="131072" ForceName="of5pa34h" Text="гімена для 34-го тижня">0</BitOpt5PerAnnum34Hymns>
    <BitOpt5ComplOctaves Id="262144" ForceName="of5ko" Text="комплеторій неділі">0</BitOpt5ComplOctaves>
    <BitOpt5MaundyThursPsalmody Id="524288" ForceName="of5zsps" Text="псалми на Великий четвер">0</BitOpt5MaundyThursPsalmody>
  </Opt5Alternatives>
  <Opt6AlternativesMultivalue Value="0" Name="o6" ForceName="of6" Text="множинні альтернативи">
    <PlaceOpt6HymnusMulti Id="1" ForceName="of6h" Text="інший гімн">0</PlaceOpt6HymnusMulti>
    <PlaceOpt6PsalmMulti Id="10" ForceName="of6ps" Text="інший псалом">0</PlaceOpt6PsalmMulti>
    <PlaceOpt6Reading2Multi Id="100" ForceName="of6c2" Text="інше читання">0</PlaceOpt6Reading2Multi>
    <PlaceOpt6Reading1Multi Id="1000" ForceName="of6c1" Text="інше читання">0</PlaceOpt6Reading1Multi>
    <PlaceOpt6AntiphoneMulti Id="10000" ForceName="of6a" Text="інша антифона">0</PlaceOpt6AntiphoneMulti>
    <PlaceOpt6CollectaMulti Id="100000" ForceName="of6m" Text="інша молитва">0</PlaceOpt6CollectaMulti>
    <PlaceOpt6PrecesMulti Id="1000000" ForceName="of6p" Text="інші прохання">0</PlaceOpt6PrecesMulti>
    <PlaceOpt6ComplMariaAntMulti Id="10000000" ForceName="of6cma" Text="інша марійська антифона">0</PlaceOpt6ComplMariaAntMulti>
    <PlaceOpt6ShortRespMulti Id="100000000" ForceName="of6kr" Text="інше резонзоріум">0</PlaceOpt6ShortRespMulti>
    <PlaceOpt6ShortReadingRespMulti Id="1000000000" ForceName="of6kcr" Text="інше читання та резонзоріум">0</PlaceOpt6ShortReadingRespMulti>
    <PlaceOpt6OurLordIntroMulti Id="10000000000" ForceName="of6pn" Text="інший вступ">0</PlaceOpt6OurLordIntroMulti>
  </Opt6AlternativesMultivalue>
</Options>
"""

# 3) Проходимо по кожному дню 2025 року й генеруємо XML
year = 2025

for single_date in (year_day for year_day in 
                    (datetime.date(year, m, d) 
                     for m in range(1, 13) for d in range(1, 32) 
                     if datetime.date(year, m, d).year == year)):
    # 3.1. Базові дані про день
    iso_str = single_date.strftime("%Y-%m-%d")
    day = single_date.day
    month = single_date.month
    year_str = single_date.year
    day_of_year = single_date.timetuple().tm_yday
    weekday = single_date.weekday()  # Понеділок=0 ... Неділя=6
    weekdays_uk = ["понеділок","вівторок","середа","четвер","п’ятниця","субота","неділя"]
    day_of_week_uk = weekdays_uk[weekday]
    
    # 3.2. Інформація про свято на цей день
    celeb = get_celebration_for(single_date)
    
    # 3.3. Створюємо корінь <LHData> та вкладені <CalendarDay> і <Options>
    root = ET.Element("LHData")
    calday = ET.SubElement(root, "CalendarDay")
    ET.SubElement(calday, "DateISO").text = iso_str
    ET.SubElement(calday, "DateDay").text = str(day)
    ET.SubElement(calday, "DateMonth").text = str(month)
    ET.SubElement(calday, "DateYear").text = str(year)
    ET.SubElement(calday, "DayOfYear").text = str(day_of_year)
    ET.SubElement(calday, "DayOfWeek", {"Id": str(weekday)}).text = day_of_week_uk
    
    # 3.4. <Celebration> ... </Celebration>
    build_celebration_element(calday, celeb)
    
    # 3.5. <StringVolume> (буква року + місяць-том). Наприклад "C, I" для січня.
    volume = f"{celeb['LiturgicalYearLetter']}, {month}"  # можна кастомізувати
    ET.SubElement(calday, "StringVolume").text = volume
    
    # 3.6. Додаємо весь блок <Options> як сирий текст (CDATA)
    # Щоб зберегти ієрархію тегів, ми вкладаємо рядок XML як „диво-коментар“
    opts_parent = ET.SubElement(root, "Options")
    opts_parent.text = None
    opts_parent.append(ET.Comment(OPTIONS_BLOCK))
    
    # 3.7. Записуємо дерево у файл
    tree = ET.ElementTree(root)
    filename = os.path.join(DAY_DIR, f"{iso_str}.xml")
    tree.write(filename, encoding="utf-8", xml_declaration=True)

# 4) Додатково генеруємо місячний файл одночасно (наприклад, для червня 2025)
#    У цьому прикладі просто зберемо разом всі <CalendarDay> для червня
for month in range(1, 13):
    # Створюємо загальний корінь
    root_month = ET.Element("LHData")
    for single_date in (datetime.date(year, month, d) for d in range(1, 32) 
                        if datetime.date(year, month, d).year == year):
        # Повторюємо ту саму структуру <CalendarDay> ... </CalendarDay> + <Options>
        iso_str = single_date.strftime("%Y_%m_%d")
        day = single_date.day
        weekday = single_date.weekday()
        day_of_year = single_date.timetuple().tm_yday
        day_of_week_uk = weekdays_uk[weekday]
        
        celeb = get_celebration_for(single_date)
        
        calday = ET.SubElement(root_month, "CalendarDay")
        ET.SubElement(calday, "DateISO").text = iso_str
        ET.SubElement(calday, "DateDay").text = str(day)
        ET.SubElement(calday, "DateMonth").text = str(month)
        ET.SubElement(calday, "DateYear").text = str(year)
        ET.SubElement(calday, "DayOfYear").text = str(day_of_year)
        ET.SubElement(calday, "DayOfWeek", {"Id": str(weekday)}).text = day_of_week_uk
        
        build_celebration_element(calday, celeb)
        
        vol = f"{celeb['LiturgicalYearLetter']}, {month}"
        ET.SubElement(calday, "StringVolume").text = vol
        
        opts_parent = ET.SubElement(root_month, "Options")
        opts_parent.text = None
        opts_parent.append(ET.Comment(OPTIONS_BLOCK))
        
    # Після того як усі <CalendarDay> додані, записуємо місяць у файл
    month_str = f"{year}_{month:02d}"
    tree_month = ET.ElementTree(root_month)
    month_filename = os.path.join(MONTH_DIR, f"{month_str}.xml")
    tree_month.write(month_filename, encoding="utf-8", xml_declaration=True)

print("Генерація завершена!")
