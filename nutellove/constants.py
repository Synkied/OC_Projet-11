# coding: utf8

# csv constants
CSV_URL = "https://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"
CSV_FNAME = 'fr.openfoodfacts.org.products.csv'
CLEANED_CSV_FILE = "db_file.csv"

# config files constants
CFG_FNAME = "postgresql_config.ini"

HEADERS_LIST = [
    "code",
    "url",
    "product_name",
    "brands",
    "stores",
    "nutrition_grade_fr",
    "main_category_fr",
    'countries_fr',
    "energy_100g",
    "fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
    "image_url",
    "image_small_url",
    "last_modified_t",
]

CATEGORIES_LIST = [
    # 'Petit-déjeuners',
    'Chips et frites',
    # 'Soupes',
    'Biscuits',
]

COUNTRIES_LIST = ["France"]
