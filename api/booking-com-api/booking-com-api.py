from fastapi import FastAPI, Query
from pydantic import BaseModel
import http.client
from urllib.parse import urlencode
import os
import json

API_KEY = "7e61bd4762msh662536c53d5845ep10b48bjsn6d7fdecfa09f"
API_HOST = "booking-com.p.rapidapi.com"


# For GPT !!!
# Function to build category filters dynamically
def build_category_filters(categories):
    return ",".join([f"class::{category}" for category in categories])

# Example categories you want to filter by (e.g., 3-star, 4-star, and free cancellation)
# selected_categories = ["free_cancellation::1", "parking::1"]

# Build category filter string dynamically
# category_filter_string = build_category_filters(selected_categories)


# For GPT Ends Here!!!


def get_destination_id(location_name: str):
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    conn.request("GET", f"/v1/hotels/locations?locale=en-gb&name={location_name}", headers=headers)
    
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    return data[0]['dest_id']


def search_booking(filters: dict) -> dict:
    """Call Booking.com API using extracted filters."""
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    conn = http.client.HTTPSConnection(API_HOST)

    dest_id = get_destination_id(filters['destination'])

    query_params = {
        'page_number': 0,
        'order_by': 'popularity',
        'categories_filter_ids': build_category_filters(filters['categories']),
        'adults_number': filters['adults_number'],
        'units': 'metric',
        'dest_id': dest_id,  # example destination ID
        'room_number': 1,
        'checkin_date': filters['checkin_date'],#'2025-06-16'
        'include_adjacency': 'true',
        'filter_by_currency': 'GBP',
        'locale': 'en-gb',
        'children_number': filters['children_number'],
        'dest_type': 'city' if int(dest_id) < 0 else 'country',
        'checkout_date': filters['checkout_date']
        }

    
    # Encode parameters for the request
    query_string = urlencode(query_params)

    # Send request with query string
    conn.request("GET", f"/v1/hotels/search?{query_string}", headers=headers)

    search_res = conn.getresponse()
    search_data = search_res.read()
    parsed_json_search_data = json.loads(search_data.decode("utf-8"))

    # get dictionary of the first page of results with only necessary info
    result = dict()
    for i in range(len(parsed_json_search_data['result'])):
        result[i] = {
            'hotel_name': parsed_json_search_data['result'][i]['hotel_name'],
            'hotel_id': parsed_json_search_data['result'][i]['hotel_id'],
            'url': parsed_json_search_data['result'][i]['url'],
            'gross_amount': parsed_json_search_data['result'][i]['composite_price_breakdown']['gross_amount'],
            'accommodation_type_name': parsed_json_search_data['result'][i]['accommodation_type_name'],
            'unit_configuration_label': parsed_json_search_data['result'][i]['unit_configuration_label'],
            'address': parsed_json_search_data['result'][i]['address'],
            'distances': parsed_json_search_data['result'][i]['distances'],
            'is_city_center': parsed_json_search_data['result'][i]['is_city_center'],
            'hotel_facilities': parsed_json_search_data['result'][i]['hotel_facilities'],
            'soldout': parsed_json_search_data['result'][i]['soldout'],
            'children_not_allowed': parsed_json_search_data['result'][i]['children_not_allowed']          
        }

        # add reviews to dictionary
        review_query_params = {
            'page_number': 0,
            'language_filter': 'en-gb',
            'hotel_id': parsed_json_search_data['result'][i]['hotel_id'],
            'locale': 'en-gb',
            'sort_type': 'SORT_MOST_RELEVANT'
        }
        # Encode parameters for the request
        review_query_string = urlencode(review_query_params)
        # Send request with query string
        conn.request("GET", f"/v1/hotels/reviews?{review_query_string}", headers=headers)
        review_res = conn.getresponse()
        review_data = review_res.read()
        parsed_json_review_data = json.loads(review_data.decode("utf-8"))

        pros = []
        cons = []
        if 'result' in parsed_json_review_data:
            for j in range(len(parsed_json_review_data['result'])):
                pros_str = parsed_json_review_data['result'][j]['pros']
                cons_str = parsed_json_review_data['result'][j]['cons']
                if pros_str:
                    pros.append(pros_str)
                if cons_str:
                    cons.append(cons_str)
        else:
            print("Warning: 'result' key missing or not a list")

        result[i]['review'] = {}
        result[i]['review']['pros'] = pros
        result[i]['review']['cons'] = cons

    
    return result

# example input and result
filters = {
    'adults_number': 5,
    'destination': "Italy",
    'children_number': 1,
    'checkin_date': '2025-06-16',
    'checkout_date': '2025-06-19',
    'categories': ["facility::16","facility::2","facility::17"]
}

print(search_booking(filters))
