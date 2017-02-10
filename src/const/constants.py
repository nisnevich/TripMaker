# ----- Functional constants

# Главные (крупнейшие + наиболее близкие к Европе): MOW - Мск, LED - СПб
# Второстепенные: KGD - Калининград, PKV - Псков, BZK - Брянск, EGO - Белгород, PES - Петрозаводск, VOZ - Воронеж,
# VOG - Волгоград, ROV - Ростов, AER - Сочи, MCX - Махачкала, RTW - Саратов, KUF - Самара, KZN - Казань,
# GOJ - Нижний Новгород

DEFAULT_ORIGIN_IATA = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ", "VOG", "ROV", "AER", "MCX", "RTW", "KUF",
                       "KZN", "GOJ"]
MAX_TOTAL_PRICE = 20000
MAX_BILL_PRICE_RU = 4000
MAX_BILL_PRICE_EU = 4000
MAX_BILL_PRICE_INSIDE_COUNTRY = 500
MAX_BILL_PRICE_GENERIC = MAX_BILL_PRICE_RU
ORIGIN_DATE_PERIOD = "2017-02-11:month"
MIN_DAYS_PER_COUNTRY = 1
MAX_DAYS_PER_COUNTRY = 7
DATE_FORMAT = "%Y-%m-%d"

# ----- Application constants

PATH_DATA_WORLD_CITIES = '../data/world_cities.json'
PATH_DATA_EU_AIRPORTS = '../data/eu_airports.data'