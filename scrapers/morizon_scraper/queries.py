from scrapers.morizon_scraper.search_parameters import SearchParameters


def create_search_map_query(search_parameters: SearchParameters, number_of_markers: int):
    return {
        "query": """
          query searchMap($parameters: ListingParametersInput!, $configuration: MarkerConfigurationInput!) {
            searchMap(parameters: $parameters, configuration: $configuration) {
              markers {
                label
                southwest { latitude longitude }
                northeast { latitude longitude }
                position { latitude longitude }
                clustered
                count
                ids { id idOnFrontend }
                price
                url
                size { width height }
              }
            }
        }
        """,
        "variables": {
            "parameters": {
                "searchParameters": search_parameters.to_dictionary(),
                "searchOrder": {"sortKey": "RANK", "sortOrder": "DESC"},
                "mode": "PROPERTY"
            },
            "configuration": {
                "numberOfMarkers": number_of_markers,
                "propertyIds": []
            }
        }
    }


def create_get_property_cluster_data_query(cluster_url: str):
    return {
        "query": """
          query getPropertyClusterData($url: String!) {
            searchResult: searchProperties(url: $url) {
              hasTopPromoted
              properties {
                nodes {
                  addedAt(format: "dd.MM.y")
                  area
                  contact {
                    company {
                      name
                      phones
                    }
                    person {
                      name
                      phones
                    }
                  }
                  location {
                    location
                    street
                  }
                  numberOfRooms
                  price {
                    amount
                    currency
                  }
                  priceM2 {
                    amount
                    currency
                  }
                  title
                  url
                }
                totalCount
              }
            }
        }
        """,
        "variables": {
            "url": f"{cluster_url}"
        }
    }


def create_get_property_details_query(property_url: str):
    return {
        "query": """
        query getPropertyDetails($url: String!) {
          propertyData: getProperty(url: $url) {
            adKeywords
            advertisementText
            area
            buildingDetailedInformation { label value url }
            contact {
              company {
                address
                faxes
                logo { id name alt }
                name
                phones
                type
              }
              contactComment
              person {
                faxes
                name
                phones
                photo { id name alt }
                type
              }
            }
            dataLayer
            description
            detailedInformation(dateFormat:"dd.MM.y") { label value url }
            environmentalData {
              dataType
              description
              value
            }
            equipments {
              icon
              label
            }
            facilities {
              icon
              label
            }
            floorFormatted
            headerTitle
            id
            idOnFrontend
            location {
              countryCode
              location
              map {
                center { latitude longitude }
                zoom
              }
              number
              street
              county
              commune
            }
            marketType
            numberOfRooms
            offerDetailedInformation(dateFormat:"dd.MM.y") { label value }
            photos {
              id
              name
              alt
            }
            plans {
              id
              name
              alt
              originUrl
            }
            presentationType
            price { amount currency }
            priceM2 { amount currency }
            priceFormatted
            priceM2Formatted
            promotionPoints
            reference
            status
            title
            transaction
            types {
              primaryType
              primaryTypeRoot
              mainType
              mainTypeRoot
            }
            url
            utilities {
              icon
              label
            }
            view3D
            videos
          }
        }
        """,
        "variables": {
            "url": property_url
        }
    }
