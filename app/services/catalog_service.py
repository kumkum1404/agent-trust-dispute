from statistics import median


# ============================================================
# SYNTHETIC PRODUCT CATALOG
# ============================================================
# Buildathon demo ke liye synthetic historical catalog data.
# Production mein ye merchant/catalog database se aayega.

PRODUCT_CATALOG = {

    "HP Laptop": {
        "category": "laptop",
        "prices": [
            39000,
            41000,
            42000,
            42500,
            43000,
            41500,
            40500
        ]
    },

    "Dell Laptop": {
        "category": "laptop",
        "prices": [
            45000,
            47000,
            46000,
            48000,
            45500,
            46500
        ]
    },

    "MacBook Air": {
        "category": "laptop",
        "prices": [
            85000,
            88000,
            90000,
            87000,
            89500,
            86000
        ]
    },

    "Gaming Laptop": {
        "category": "laptop",
        "prices": [
            70000,
            75000,
            80000,
            78000,
            82000,
            76000
        ]
    },

    "iPhone": {
        "category": "mobile",
        "prices": [
            65000,
            68000,
            70000,
            67500,
            69000
        ]
    },

    "Samsung Phone": {
        "category": "mobile",
        "prices": [
            30000,
            32000,
            35000,
            33000,
            34000
        ]
    },

    "Gold Necklace": {
        "category": "jewelry",
        "prices": [
            50000,
            55000,
            60000,
            58000,
            62000
        ]
    }

}


# ============================================================
# NORMALIZE PRODUCT NAME
# ============================================================

def normalize_product_name(product_name: str) -> str:

    if not product_name:
        return ""

    return product_name.strip().lower()


# ============================================================
# FIND PRODUCT
# ============================================================

def find_product(product_name: str):

    normalized_name = normalize_product_name(
        product_name
    )

    for name, data in PRODUCT_CATALOG.items():

        if name.lower() == normalized_name:

            return name, data

    return None, None


# ============================================================
# GET CATALOG MEDIAN PRICE
# ============================================================

def get_catalog_median_price(
    product_name: str,
    category: str
):

    product_name_found, product = find_product(
        product_name
    )

    # --------------------------------------------------------
    # Exact product match
    # --------------------------------------------------------

    if product:

        if (
            product["category"].lower()
            == category.lower()
        ):

            return float(
                median(product["prices"])
            )


    # --------------------------------------------------------
    # Category fallback
    # --------------------------------------------------------

    category_prices = []

    for product_data in PRODUCT_CATALOG.values():

        if (
            product_data["category"].lower()
            == category.lower()
        ):

            category_prices.extend(
                product_data["prices"]
            )


    if category_prices:

        return float(
            median(category_prices)
        )


    # --------------------------------------------------------
    # Unknown product/category
    # --------------------------------------------------------

    return None


# ============================================================
# GET PRODUCT CATALOG DETAILS
# ============================================================

def get_catalog_details(
    product_name: str,
    category: str
):

    product_name_found, product = find_product(
        product_name
    )

    if product:

        prices = product["prices"]

        return {

            "product_found": True,

            "product_name":
                product_name_found,

            "category":
                product["category"],

            "historical_prices":
                prices,

            "median_price":
                float(median(prices)),

            "min_price":
                min(prices),

            "max_price":
                max(prices)

        }


    return {

        "product_found": False,

        "product_name":
            product_name,

        "category":
            category,

        "historical_prices": [],

        "median_price": None,

        "min_price": None,

        "max_price": None

    }