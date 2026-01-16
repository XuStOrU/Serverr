# logic.py
import random

# Удочки
RODS = {
    "Старая удочка":       {"price": 0,     "mult": 1.0},
    "Деревянная удочка":  {"price": 150,   "mult": 1.1},
    "Бамбуковая":         {"price": 300,   "mult": 1.25},
    "Фидер":              {"price": 700,   "mult": 1.5},
    "Карповая удочка":    {"price": 1200,  "mult": 1.8},
    "Спиннинг":           {"price": 2000,  "mult": 2.3},
    "Тяжёлый спиннинг":   {"price": 3500,  "mult": 3.0},
    "Профи спиннинг":     {"price": 6000,  "mult": 4.0},
    "Титановый спиннинг": {"price": 12000, "mult": 6.0},
    "Удочка богов":       {"price": 30000, "mult": 10.0},
}

# Приманки
BAITS = {
    "Червь":      {"price": 0,    "bonus": 1.0},
    "Хлеб":       {"price": 50,   "bonus": 1.1},
    "Опарыш":     {"price": 120,  "bonus": 1.25},
    "Мотыль":     {"price": 250,  "bonus": 1.4},
    "Креветка":   {"price": 500,  "bonus": 1.7},
    "Икра":       {"price": 1000, "bonus": 2.2},
}

# Локации
LOCATIONS = {
    "Местечко": [0, 1.0],
    "Река": [100, 1.2],
    "Озеро": [500, 1.5]
}

# Рыбы
FISHES = {
    "Ёрш": ["Обычная", 0.1, 0.3, 10, "https://fishmanual.ru/images/2018/10/99/zzzzzzf.jpg"],
    "Карась": ["Обычная", 0.2, 0.5, 15, "https://fishermanblog.ru/wp-content/uploads/kruchki-na-karasya-1.jpg"],
    "Плотва": ["Обычная", 0.1, 0.4, 12, "https://velesovik.ru/images/article/473/files_514.jpg"],
    "Окунь": ["Необычная", 0.3, 0.7, 25, "https://fishmanual.ru/images/2018/10/98/zzm.jpg"],
    "Лещ": ["Необычная", 0.5, 1.0, 40, "https://fishmanual.ru/images/2018/10/98/zzm.jpg"],
    "Красноперка": ["Необычная", 0.2, 0.6, 30, "https://sazanya-bukhta.ru/wp-content/uploads/2020/07/Krasnoperka-3.jpg"],
    "Густера": ["Редкая", 0.3, 0.8, 50, "https://fishingday.org/wp-content/uploads/2017/03/1.jpg"],
    "Щука": ["Эпическая", 1.0, 3.0, 150, "https://www.fishing-v.ru/images/img/bayki/Kak_Ya_Poymal_Pervuyu_Chuku.jpg"],
    "Судак": ["Эпическая", 1.0, 2.5, 140, "https://catcher.fish/wp-content/uploads/2017/09/sudak-1.jpg"],
    "Карп": ["Редкая", 1.0, 2.0, 100, "https://fishx.org/wp-content/uploads/karp.jpg"],
    "Трофейный окунь": ["Легендарная", 2.0, 4.0, 300, "https://dailyfish.ru/uploads/posts/2025-07/samyj-krupnyj-okun-pojmannyj-v-rossii-pochti-vdvoe-bolshe-mirovogo-rekorda.jpg"],
    "Белуга": ["Легендарная", 40.0, 60.0, 3000, "https://fishx.org/wp-content/uploads/2018-07-09-16-38-12.jpg"],
    "Осётр": ["Легендарная", 30.0, 50.0, 2000, "https://cs15.pikabu.ru/post_img/big/2024/11/15/7/1731667180114768296.png"],
    "Гигантский сом": ["Легендарная", 50.0, 80.0, 5000, "https://img.tsn.ua/cached/607/tsn-0b4bc102/thumbs/1200x630/89/de/71112303473530ef2acdc9b3b94fde89.jpg"],
    "Сом": ["Эпическая", 5.0, 20.0, 200, "https://i.ibb.co/fz4Bm5CD/primanki-na-soma.jpg"]
}

# Мусор
TRASH = {
    "Сапог": "https://i.pinimg.com/200x150/bd/d1/61/bdd1619dd33df3680d2796c59be9b36f.jpg",
    "Коряга": "https://memchik.ru//images/memes/5efaf617b1c7e3035a7bff79.jpg"
}

# Функция ловли
def catch(rod, bait, location):
    chance = random.randint(1, 100)
    if chance <= 20:  # 20% мусор
        name = random.choice(list(TRASH.keys()))
        return {"type": "trash", "name": name}
    else:
        name = random.choice(list(FISHES.keys()))
        data = FISHES[name]
        weight = round(random.uniform(data[1], data[2]), 2)
        price = int(data[3] * weight)
        xp_dict = {"Обычная":10,"Необычная":25,"Редкая":40,"Эпическая":55,"Легендарная":80}
        xp = xp_dict[data[0]]
        return {"type":"fish","name":name,"weight":weight,"price":price,"xp":xp,"photo":data[4]}