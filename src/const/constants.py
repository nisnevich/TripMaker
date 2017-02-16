import os

# ----- Functional constants

# Главные (крупнейшие + наиболее близкие к Европе): MOW - Мск, LED - СПб
# Второстепенные: KGD - Калининград, PKV - Псков, BZK - Брянск, EGO - Белгород, PES - Петрозаводск, VOZ - Воронеж,
# VOG - Волгоград, ROV - Ростов, AER - Сочи, MCX - Махачкала, RTW - Саратов, KUF - Самара, KZN - Казань,
# GOJ - Нижний Новгород

DEFAULT_ORIGIN_IATA = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ"]
# DEFAULT_ORIGIN_IATA = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ", "VOG", "ROV", "AER", "MCX", "RTW", "KUF",
#                        "KZN", "GOJ"]
MAX_TOTAL_PRICE = 20000
MAX_BILL_PRICE_RU = 2400
MAX_BILL_PRICE_EU = 1500
MAX_BILL_PRICE_INSIDE_COUNTRY = 100
MAX_BILL_PRICE_GENERIC = MAX_BILL_PRICE_RU
# The value of 2000 for this parameter reduces the search time TENFOLD!
MAX_CITY_DISTANCE = 2000

PRINTING_LEVEL = 4

ORIGIN_DATE_PERIOD = "2017-03-01:month"
MIN_DAYS_PER_COUNTRY = 1
MAX_DAYS_PER_COUNTRY = 7
DATE_FORMAT = "%Y-%m-%d"

# ----- Application constants
# Main:
# AS_ACCESS_TOKEN = "3bb88d0122282a9a02bdc94ff129fef9"
# Left:
AS_ACCESS_TOKEN = "2ca3d0f09ca5e1345cb6cca126154c47"
TIMEOUT_SLEEP_CONNECTION_ERROR = 30

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_ROOT = os.path.join(PROJECT_ROOT, 'input')
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
CONFIG_ROOT = os.path.join(PROJECT_ROOT, 'config')

PATH_DATA_WORLD_CITIES = os.path.join(DATA_ROOT, 'world_cities.json')
PATH_DATA_EU_AIRPORTS = os.path.join(DATA_ROOT, 'eu_airports.data')
PATH_ROUTE_DUMP = os.path.join(INPUT_ROOT, 'route.dump')
PATH_LOG = os.path.join(PROJECT_ROOT, 'logs')
