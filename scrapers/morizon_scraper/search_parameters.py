from scrapers.morizon_scraper.consts import TransactionType, RealEstateType


class SearchParameters:
    def __init__(self, northeast_node, southwest_node,
                 transaction_type: TransactionType, real_estate_types: [RealEstateType],
                 locations: [str] = None):
        self.northeast_node = northeast_node
        self.southwest_node = southwest_node
        self.transaction_type = transaction_type
        self.real_estate_types = real_estate_types
        self.locations = locations

    def to_dictionary(self):
        dictionary = {
            "location": {
                "mapBounds": {
                    "northeast": dict(self.northeast_node),
                    "southwest": dict(self.southwest_node)
                }
            },
            "transaction": self.transaction_type,
            "type": self.real_estate_types
        }

        if self.locations is not None:
            dictionary["locations"] = self.locations

        return dictionary
