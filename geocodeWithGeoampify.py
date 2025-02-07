def geocodeWithGeoampify(data_path: str, api_key: str, address_col: str):
    """Geocodes a csv using Geoampify API
    
    Input:
        data_path = the path to the csv file
        api_key = Goeampify API key
        address_col = the name of the column of the csv with address. Note that the whole address must be in a single column.
    Out:
        df = the original data with two new columns: "Lat" and "Long", as a Pandas DataFrame object
    """
    import pandas as pd
    import requests
    import chardet
    import time

    # Detect file encoding
    with open(data_path, "rb") as f:
        result = chardet.detect(f.read())

    # Read csv as dat frame
    df = pd.read_csv(data_path, sep = ",", encoding = result["encoding"] or "ISO-8859-1")

    # Create list for latitude and longitude values
    latitudes = []
    longitudes = []

    # Pull address column from data frame
    addresses = df[[address_col]]

    # Print number of addresses to geocode
    n = len(addresses)
    print(f"addresses to geocode: {n}")

    # Iterate over addresses
    for i in range(n):
        # Build the API URL
        address_value = addresses.iloc[i, 0]
        url = f"https://api.geoapify.com/v1/geocode/search?text={address_value}&limit=1&apiKey={api_key}"

        # Send the API request and get the response
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Extract the first result from the data
            result = data["features"][0]

            # Extract the latitude and longitude of the result
            latitude = result["geometry"]["coordinates"][1]
            longitude = result["geometry"]["coordinates"][0]

        else:
            # Handle geocoding error
            print(f"{addresses[i]}: Request failed with status code {response.status_code}")
            latitude, longitude = None, None

        # Append latitude and longitude values to lists
        latitudes.append(latitude)
        longitudes.append(longitude)

        # Wait one second to process next query
        time.sleep(1)

    # Create latitude and longitude columns in data frame
    df["Lat"] = latitudes
    df["Long"] = longitudes

    return df