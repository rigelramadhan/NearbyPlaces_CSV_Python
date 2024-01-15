import csv
import googlemaps
import time

API_KEY = "YOUR_API_KEY"

maps = googlemaps.Client(key=API_KEY)

latitude = -6.171106
longitude = 106.822898

radius = 5000
keywords = ["hotel", "food", "restaurant", "cafe", "hospital", "medical"]

max_results_per_keyword = 20
max_total_results = 9999999

all_results = []

for keyword in keywords:
    next_page_token = None

    while len(all_results) < max_total_results:
        try:
            results = maps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=keyword,
                page_token=next_page_token
            )
        except googlemaps.exceptions.ApiError as e:
            print(f"Error in places_nearby for keyword '{keyword}': {e}")
            break

        if "results" in results:
            all_results.extend(results["results"])

        next_page_token = results.get("next_page_token")

        if not next_page_token:
            break

        time.sleep(2)

all_results = all_results[:max_total_results]

csv_file_path = "places.csv"

count = 0
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['Place ID', 'Name', 'Address', 'Rating', 'Types']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for result in all_results:
        try:
            place_id = result["place_id"]
            name = result["name"]
            address = result.get("vicinity", "")
            rating = result.get("rating", "")
            types = result.get("types", [])

            count += 1
            writer.writerow({'Place ID': place_id, 'Name': name, 'Address': address, 'Rating': rating, 'Types': types})

        except Exception as e:
            print(f"Error processing result: {e}")

print(f"{count} Results exported to {csv_file_path}")