"""Ziraat Bank Eurobond API provider.

Fetches Turkish sovereign Eurobond data from Ziraat Bank's API.
Includes USD and EUR denominated bonds with bid/ask prices and yields.
"""

from datetime import datetime

from bs4 import BeautifulSoup

from borsapy._providers.base import BaseProvider
from borsapy.cache import TTL

# Ziraat Bank Eurobond API endpoint
ZIRAAT_URL = "https://www.ziraatbank.com.tr/tr/_layouts/15/Ziraat/FaizOranlari/Ajax.aspx/GetZBBonoTahvilOran"


class ZiraatEurobondProvider(BaseProvider):
    """Provider for Eurobond data from Ziraat Bank."""

    def _parse_turkish_number(self, text: str) -> float | None:
        """Parse Turkish number format (comma as decimal separator).

        Examples:
            "101,613667" -> 101.613667
            "22,48" -> 22.48
            "0,00" -> 0.0
        """
        text = text.strip()
        if not text or text == "-":
            return None
        try:
            return float(text.replace(",", "."))
        except ValueError:
            return None

    def _parse_date(self, text: str) -> datetime | None:
        """Parse Ziraat date format.

        Examples:
            "26.01.2026 " -> datetime(2026, 1, 26)
            "14.04.2026 " -> datetime(2026, 4, 14)
        """
        text = text.strip()
        if not text:
            return None

        try:
            return datetime.strptime(text, "%d.%m.%Y")
        except ValueError:
            return None

    def get_eurobonds(self, currency: str | None = None) -> list[dict]:
        """Get all Turkish Eurobonds.

        Args:
            currency: Optional filter by currency ("USD" or "EUR").

        Returns:
            List of Eurobond dicts with isin, maturity, days_to_maturity,
            currency, bid_price, bid_yield, ask_price, ask_yield.

        Example:
            [
                {
                    "isin": "US900123DG28",
                    "maturity": datetime(2033, 1, 19),
                    "days_to_maturity": 2562,
                    "currency": "USD",
                    "bid_price": 120.26,
                    "bid_yield": 6.55,
                    "ask_price": 122.19,
                    "ask_yield": 6.24,
                },
                ...
            ]
        """
        cache_key = "ziraat_eurobonds"
        cached = self._cache_get(cache_key)

        if cached is None:
            # Fetch from API
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://www.ziraatbank.com.tr",
                "Referer": "https://www.ziraatbank.com.tr/tr/bireysel/yatirim/eurobond",
            }

            payload = {
                "kiymetTipi": "EURO",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "hideIfStartWith": "",
            }

            response = self._post(ZIRAAT_URL, json=payload, headers=headers)
            data = response.json()

            # Extract HTML from response
            html = data.get("d", {}).get("Data", "")
            if not html:
                return []

            # Parse HTML table
            soup = BeautifulSoup(html, "lxml")
            table = soup.find("table")
            if not table:
                return []

            bonds = []
            rows = table.find_all("tr")

            for row in rows[1:]:  # Skip header row
                cols = row.find_all("td")
                if len(cols) < 8:
                    continue

                bond = {
                    "isin": cols[0].text.strip(),
                    "maturity": self._parse_date(cols[1].text),
                    "days_to_maturity": int(cols[2].text.strip()) if cols[2].text.strip().isdigit() else 0,
                    "currency": cols[3].text.strip(),
                    "bid_price": self._parse_turkish_number(cols[4].text),
                    "bid_yield": self._parse_turkish_number(cols[5].text),
                    "ask_price": self._parse_turkish_number(cols[6].text),
                    "ask_yield": self._parse_turkish_number(cols[7].text),
                }
                bonds.append(bond)

            # Cache for 5 minutes
            self._cache_set(cache_key, bonds, TTL.FX_RATES)
            cached = bonds

        # Apply currency filter if specified
        if currency:
            currency = currency.upper()
            return [b for b in cached if b["currency"] == currency]

        return cached

    def get_eurobond(self, isin: str) -> dict | None:
        """Get single Eurobond by ISIN.

        Args:
            isin: ISIN code (e.g., "US900123DG28")

        Returns:
            Eurobond dict or None if not found.
        """
        isin = isin.upper()
        bonds = self.get_eurobonds()

        for bond in bonds:
            if bond["isin"] == isin:
                return bond

        return None


# Singleton instance
_provider: ZiraatEurobondProvider | None = None


def get_eurobond_provider() -> ZiraatEurobondProvider:
    """Get the singleton Eurobond provider instance."""
    global _provider
    if _provider is None:
        _provider = ZiraatEurobondProvider()
    return _provider
