from search import search, nights_counter
import asyncio

sample_input = {"place"  : "Germany", "budget"  : 1000.00,"checkin_date"  : "2025-06-16", "checkout_date"  : "2025-06-19", "adults_number"  : 5, "children_number"  : 1, "dyanamic_filters" : {"non-smoking" : "yes", "swimming pool" : "yes"}}

output = asyncio.run(search(sample_input, full_results = True))
