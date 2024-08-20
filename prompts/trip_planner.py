trip_planner_system_message = """
Your task is to produce a detailed itinerary for the user. 

Please prepare a report in a form of a markdown file, with the following sections:
1. Trip Details - detailed day split with destination, activities.
2. Getting there - flights, transportation.

Do NOT include any cost calculations in the report. 

Produce everything in .md format. 

"""


trip_planner_user_message = """
{traveler_info}

The trip is to {destination_country} and will last from {start_date} to {end_date}. The origin country is {origin_country}.

The user has following expectations and requirements:
{expectations}
"""

trip_booker_system_message = """
Your task is to produce a list of bookings for the user, with the rough cost simulation of the trip.

Include the following:
- flights + any transportation
- accommodation
- additional attractions

Do NOT include the itinerary in the output. Focus only on the costs and bookings.
Include the rough cost, as well as summarize it all.
Produce everything in .md format. 

"""


trip_booker_user_message = """
{traveler_info}

The trip is to {destination_country} and will last from {start_date} to {end_date}. The origin country is {origin_country}.

The user has following expectations and requirements:
{expectations}

The itinerary is as follows:
{itinerary}
"""