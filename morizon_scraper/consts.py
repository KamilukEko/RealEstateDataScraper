MORIZON_URL = "https://www.morizon.pl"
API_URL = f"{MORIZON_URL}/api-morizon"
HEADER = {
    "Content-Type": "application/json",
    "X-Mzn-Client": "MORIZON",
    "X-Mzn-Cache-Response": "true",
    "X-Mzn-Type": "WWW_2_0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
    "Origin": MORIZON_URL,
    f"Referer": f"{MORIZON_URL}/mieszkania/"
}


class RealEstateType(str):
    FLAT = "FLAT"


class TransactionType(str):
    SALE = "SALE"
