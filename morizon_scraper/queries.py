from models.search_parameters import SearchParameters


def create_search_map_query(search_parameters: SearchParameters, number_of_markers):
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