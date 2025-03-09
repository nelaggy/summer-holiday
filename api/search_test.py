from search import search

sample_input = {"place"  : "Italy", "checkin_date"  : "2025-06-16", "checkout_date"  : "2025-06-19", "adults_number"  : 5, "children_number"  : 1, "dyanamic_filters" : {"toilets" : "yes", "non-smoking" : "yes", "swimming pool" : "yes"}}

output = search(sample_input, full_results = True)

