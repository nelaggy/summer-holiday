from fastapi import APIRouter
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import booking_com_api.booking_com_api as bca
import os
import re

# Load environment varialbes from .env file
load_dotenv()

# Router for modular design - imported into main.py
router = APIRouter()

# Load an OpenAI API key and activate client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment variables
client = OpenAI(api_key=OPENAI_API_KEY)

# Filters type validation received from POST endpoint
class Filters(BaseModel):
    location: str | None
    budget: float | None
    num_people: int | None
    start_date: str | None
    end_date: str | None
    dynamic_filters: dict[str,] | None

# Indices -> various filters in booking.com (redundant)
indices_filters = {
'1': 'Swimming pool',
'2': 'Parking',
'3': 'Restaurant',
'4': 'Pet friendly',
'5': 'Room service',
'6': 'Meeting/Banquet facilities',
'7': 'Bar',
'8': '24-hour front desk',
'9': 'Tennis court',
'10': 'Sauna',
'11': 'Fitness center',
'12': 'Golf course (within 2 miles)',
'13': 'Newspapers',
'14': 'Garden',
'15': 'Terrace',
'16': 'Non-smoking rooms',
'17': 'Airport shuttle',
'19': 'Fishing',
'20': 'Business center',
'21': 'Babysitting/Child services',
'22': 'Laundry',
'23': 'Dry cleaning',
'24': 'Continental breakfast',
'25': 'Facilities for disabled guests',
'26': 'Skiing',
'27': 'Hair/Beauty salon',
'28': 'Family rooms',
'29': 'Game room',
'30': 'Casino',
'41': 'VIP room facilities',
'43': 'Breakfast in the room',
'44': 'Ironing service',
'45': 'Honeymoon suite',
'46': 'Free parking',
'47': 'Internet',
'48': 'Elevator',
'49': 'Express check-in/out',
'50': 'Solarium',
'51': 'Safe',
'52': 'Valet parking',
'53': 'Currency exchange',
'54': 'Spa',
'55': 'Massage',
'56': 'Playground',
'57': 'Pool table',
'58': 'Ping-pong',
'59': 'Karaoke',
'60': 'Gift shop',
'61': 'Windsurfing',
'62': 'Darts',
'63': 'Hot tub/Jacuzzi',
'64': 'Soundproof rooms',
'65': 'Bicycle rental (additional charge)',
'66': 'Library',
'67': 'Shoeshine',
'69': 'Canoeing',
'70': 'Hiking',
'71': 'Chapel/Shrine',
'72': 'BBQ facilities',
'73': 'Packed lunches',
'75': 'Car rental',
'76': 'Cycling',
'77': 'Bowling',
'78': 'Tour desk',
'79': 'Turkish/Steam Bath',
'80': 'Heating',
'81': 'Fax/Photocopying',
'82': 'Diving',
'86': 'Horseback riding',
'87': 'Racquetball',
'88': 'Designer Hotel',
'89': 'Ticket service',
'90': 'Snorkeling',
'91': 'Baggage storage',
'92': 'Shops on site',
'96': 'WiFi',
'97': 'Mini golf',
'98': 'Gay Friendly',
'99': 'Ski storage',
'100': 'Ski school',
'101': 'Hypoallergenic room available',
'102': 'Breakfast Buffet',
'103': 'Indoor pool',
'104': 'Outdoor pool',
'107': 'Free WiFi',
'108': 'Smoke-free property',
'109': 'Air conditioning',
'110': 'Designated smoking area',
'111': 'ATM on site',
'114': 'Private beach area',
'115': 'Restaurant',
'116': 'Buffet',
'117': 'Snack bar',
'118': 'Sun deck',
'119': 'Outdoor pool (year-round)',
'120': 'Outdoor pool (seasonal)',
'121': 'Indoor pool (year-round)',
'122': 'Indoor pool (seasonal)',
'123': 'Bikes available (free)',
'124': 'Concierge',
'125': 'Entertainment staff',
'126': 'Nightclub/DJ',
'127': 'Private check-in/out',
'128': 'Shuttle service (free)',
'129': 'Shuttle service (additional charge)',
'130': 'Ski rental on site',
'131': 'Ski pass vendor',
'132': 'Ski-in, ski-out access',
'133': 'Special diet meals (on request)',
'134': 'Suit press',
'135': 'Vending machine (drinks)',
'136': 'Vending machine (snacks)',
'137': 'Water sports facilities on site',
'138': 'Hot spring bath',
'139': 'Airport shuttle (free)',
'140': 'Airport shuttle (additional charge)',
'141': 'Shared kitchen',
'142': 'Lockers',
'143': 'Shared lounge/TV area',
'144': "Kids' club", '145': 'Convenience store on site',
'146': 'Beachfront',
'147': 'Evening entertainment',
'148': 'Water park',
'149': 'Adults only',
'150': 'Detached - Entire property',
'151': 'Semi-detached',
'152': 'Privately-owned apartment',
'153': 'Ground floor (private access)',
'154': 'Ground floor (shared access)',
'155': 'Upper floor - elevator',
'156': 'Upper floor - stairs',
'157': 'Wheelchair accessible',
'158': 'Daily housekeeping',
'159': 'Grocery deliveries',
'160': 'Parking on site',
'161': 'Private Parking',
'162': 'Misc parking',
'163': 'WiFi in all areas',
'164': 'Paid WiFi',
'165': 'Michelin-star Dining',
'166': 'Open-air bath',
'167': 'Public Bath',
'168': 'Waterslide',
'169': 'Swimming pool toys',
'170': 'Board games/Puzzles',
'171': 'Books, DVDs & music for kids',
'172': 'Indoor play area',
'173': 'Outdoor play equipment for kids',
'174': 'Baby safety gates',
'175': "Kids' TV channels", '176': "Kids' meals", '177': 'Kid-friendly buffet',
'178': 'Sofa Bed',
'179': 'Secure parking',
'180': 'Street parking',
'181': 'Parking garage',
'182': 'Electric vehicle charging station',
'183': 'Public transit tickets',
'184': 'Accessible parking',
'185': 'Wheelchair accessible',
'186': 'Toilet with grab rails',
'187': 'Raised toilet',
'188': 'Lowered sink',
'189': 'Bathroom emergency cord',
'192': 'Rooftop pool',
'193': 'Infinity pool',
'194': 'Pool with view',
'195': 'Heated pool',
'196': 'Saltwater pool',
'197': 'Plunge pool',
'198': 'Pool/Beach towels',
'199': 'Pool bar',
'200': 'Shallow end',
'201': 'Pool cover',
'203': 'Wine/Champagne',
'204': 'Bottle of water',
'205': 'Fruit',
'206': 'Chocolate/Cookies',
'207': 'Tickets to shows/attractions',
'209': 'Airport pickup',
'210': 'Airport drop-off',
'211': 'Visual aids (Braille)',
'212': 'Visual aids (tactile signs)',
'213': 'Auditory guidance',
'214': 'Strollers',
'215': 'Tennis equipment',
'216': 'Badminton equipment',
'217': 'Pet basket',
'218': 'Pet bowls',
'219': 'Coffee house on site',
'220': 'Beach chairs/Loungers',
'221': 'Beach umbrellas',
'222': 'Outdoor furniture',
'223': 'Fenced pool',
'224': 'Picnic area',
'225': 'Outdoor fireplace',
'226': 'Beauty services',
'227': 'Facial treatments',
'228': 'Waxing services',
'229': 'Makeup services',
'230': 'Hair treatments',
'231': 'Manicure',
'232': 'Pedicure',
'233': 'Haircut',
'234': 'Hair coloring',
'235': 'Hairstyling',
'236': 'Body treatments',
'237': 'Body scrub',
'238': 'Body wrap',
'239': 'Light therapy',
'240': 'Spa facilities',
'241': 'Steam room',
'242': 'Spa lounge/Relaxation area',
'243': 'Foot bath',
'244': 'Spa/Wellness packages',
'245': 'Back massage',
'246': 'Neck massage',
'247': 'Foot massage',
'248': "Couples' massage", '249': 'Head massage',
'250': 'Hand massage',
'251': 'Full-body massage',
'252': 'Massage chair',
'253': 'Fitness',
'254': 'Yoga classes',
'255': 'Fitness classes',
'256': 'Personal trainer',
'257': 'Locker rooms',
'258': "Kids' pool", '301': 'Swimming pool',
'302': 'Beach',
'303': 'Special baths',
'304': 'Shuttle service',
'305': 'Breakfast options',
'306': 'Game drives',
'307': 'The Big Five',
'308': 'Walking Safari',
'309': 'Bush Dinner',
'310': 'Game Drives',
'311': 'The Big Five',
'312': 'Walking Safari',
'313': 'Bush Dinner',
'400': 'Temporary art galleries',
'401': 'Bar crawls',
'402': 'Stand-up comedy',
'403': 'Movie nights',
'404': 'Walking tours',
'405': 'Bike tours',
'406': 'Themed dinners',
'407': 'Happy hour',
'408': 'Tour or class about local culture',
'409': 'Cooking class',
'410': 'Live music/Performance',
'411': 'Live sports events (broadcast)',
'412': 'Archery',
'413': 'Aerobics',
'414': 'Bingo',
'415': 'Downhill Skiing',
'418': '24-hour security',
'419': 'Key access',
'420': 'Key card access',
'421': 'Security alarm',
'422': 'Smoke alarms',
'423': 'CCTV in common areas',
'424': 'CCTV outside property',
'425': 'Fire extinguishers',
'426': 'Bicycle parking',
'427': 'Telephone',
'428': 'Postal service',
'429': 'Laundry room',
'430': 'Ski shuttle',
'431': 'Bath/Hot spring',
'432': 'Private bath',
'433': 'Swimming pool',
'434': 'No single-use plastics',
'435': 'Have you removed (or never offered) all single-use plastic miniature shampoo, conditioner, and body wash bottles?',
'436': 'Guests have the option to reuse towels',
'437': 'Carbon monoxide detector',
'438': 'Carbon monoxide sources',
'439': 'Have you removed (or never offered) all plastic straws?',
'440': 'Have you removed (or never offered) all plastic cups?',
'441': 'Have you removed (or never offered) all plastic water bottles?',
'442': 'Have you removed (or never offered) all plastic bottles for other drinks?',
'443': 'Have you removed (or never offered) all plastic cutlery and tableware?',
'444': 'Key card or motion-controlled electricity for guests',
'445': 'Guests can opt out of daily cleaning service',
'446': 'Water cooler/dispenser',
'447': 'Bicycle rental',
'448': 'Have you removed (or never offered) all plastic stirrers?',
'449': 'Use of cleaning chemicals that are effective against coronavirus',
'450': 'Linens, towels, and laundry washed in accordance with local authority guidelines',
'451': 'Guest accommodation disinfected between stays',
'452': 'Guest accommodation sealed after cleaning',
'453': 'Physical distancing in dining areas',
'454': 'Food can be delivered to guest accommodation',
'455': 'Staff follow all safety protocols as directed by local authorities',
'456': 'Shared stationery (e.g. printed menus, magazines, pens, paper) removed',
'457': 'Hand sanitizer in guest accommodation and common areas',
'458': 'Process in place to check health of guests',
'459': 'First aid kits available',
'460': 'Contactless check-in/out',
'461': 'Cashless payment available',
'462': 'Physical distancing rules followed',
'463': 'Mobile app for room service',
'464': 'Screens or physical barriers between staff and guests in appropriate areas',
'465': 'Invoice provided',
'466': 'Property cleaned by professional cleaning companies',
'467': 'All plates, cutlery, glasses, and other tableware sanitized',
'468': 'Guests have the option to cancel any cleaning services for their accommodation during their stay',
'470': 'Passport/ID info collected online before you arrive',
'471': 'Check-in kiosk in the lobby',
'472': 'Lockbox key collection at the property',
'473': 'Lockbox key collection near the property',
'474': 'Digital key access',
'484': 'Breakfast to-go containers',
'485': 'Delivered food covered securely',
'486': 'Access to healthcare professionals',
'487': 'Thermometers for guests provided by property',
'488': 'Face masks for guests available',
'489': "Wild (non-domesticated) animals aren't displayed or interacted with while kept at the property, nor are they harvested, consumed, or sold.", '490': 'Recycling bins are available to guests and waste is recycled',
'491': 'At least 80% of food is sourced from your region',
'492': 'At least 80% of lighting uses energy-efficient LED bulbs',
'493': 'Only using water-efficient toilets (e.g. low-flow toilets, dual flush toilets)',
'494': 'Only using water-efficient showers (e.g smart showers, low-flow shower heads)',
'495': 'All windows are double-glazed',
'496': 'Food waste policy in place that includes education, food waste prevention, reduction, recycling, and disposal',
'497': 'A percentage of revenue is invested back into community or sustainability projects',
'498': 'Compensate for at least 10% of total annual carbon emissions by purchasing certified carbon offsets',
'499': 'Tours and activities organized by local guides and businesses',
'500': 'Vegetarian menu options available',
'501': 'Vegan menu options available',
'502': 'Green spaces like (rooftop) gardens at the property',
'503': 'At least 80% of provided food is organic',
'504': '100% renewable electricity used throughout the property',
'505': 'Local artists are offered a platform to display their talents',
'506': 'Provide guests with info about local ecosystems, history, culture, and visitor etiquette',
'507': '100% renewable energy is used throughout the property',
'508': 'Local artists are offered a platform to display their talents',
'509': 'Provide guests with information regarding local ecosystems, heritage and culture, as well as visitor etiquette',
'510': 'Provide guests with information regarding local ecosystems, heritage and culture, as well as visitor etiquette',
'511': 'Indoor fireplace',
'512': 'Breakfast to go',
'513': 'Breakfast to go',
'514': 'Breakfast to go',
'other': ''
}
# Filters -> indices in booking.com
filters_indices = {
'Swimming pool': '1',
'Parking': '2',
'Restaurant': '3',
'Pet friendly': '4',
'Room service': '5',
'Meeting/Banquet facilities': '6',
'Bar': '7',
'24-hour front desk': '8',
'Tennis court': '9',
'Sauna': '10',
'Fitness center': '11',
'Golf course (within 2 miles)': '12',
'Newspapers': '13',
'Garden': '14',
'Terrace': '15',
'Non-smoking rooms': '16',
'Airport shuttle': '17',
'Fishing': '19',
'Business center': '20',
'Babysitting/Child services': '21',
'Laundry': '22',
'Dry cleaning': '23',
'Continental breakfast': '24',
'Facilities for disabled guests': '25',
'Skiing': '26',
'Hair/Beauty salon': '27',
'Family rooms': '28',
'Game room': '29',
'Casino': '30',
'VIP room facilities': '41',
'Breakfast in the room': '43',
'Ironing service': '44',
'Honeymoon suite': '45',
'Free parking': '46',
'Internet': '47',
'Elevator': '48',
'Express check-in/out': '49',
'Solarium': '50',
'Safe': '51',
'Valet parking': '52',
'Currency exchange': '53',
'Spa': '54',
'Massage': '55',
'Playground': '56',
'Pool table': '57',
'Ping-pong': '58',
'Karaoke': '59',
'Gift shop': '60',
'Windsurfing': '61',
'Darts': '62',
'Hot tub/Jacuzzi': '63',
'Soundproof rooms': '64',
'Bicycle rental (additional charge)': '65',
'Library': '66',
'Shoeshine': '67',
'Canoeing': '69',
'Hiking': '70',
'Chapel/Shrine': '71',
'BBQ facilities': '72',
'Packed lunches': '73',
'Car rental': '75',
'Cycling': '76',
'Bowling': '77',
'Tour desk': '78',
'Turkish/Steam Bath': '79',
'Heating': '80',
'Fax/Photocopying': '81',
'Diving': '82',
'Horseback riding': '86',
'Racquetball': '87',
'Designer Hotel': '88',
'Ticket service': '89',
'Snorkeling': '90',
'Baggage storage': '91',
'Shops on site': '92',
'WiFi': '96',
'Mini golf': '97',
'Gay Friendly': '98',
'Ski storage': '99',
'Ski school': '100',
'Hypoallergenic room available': '101',
'Breakfast Buffet': '102',
'Indoor pool': '103',
'Outdoor pool': '104',
'Free WiFi': '107',
'Smoke-free property': '108',
'Air conditioning': '109',
'Designated smoking area': '110',
'ATM on site': '111',
'Private beach area': '114',
'Buffet': '116',
'Snack bar': '117',
'Sun deck': '118',
'Outdoor pool (year-round)': '119',
'Outdoor pool (seasonal)': '120',
'Indoor pool (year-round)': '121',
'Indoor pool (seasonal)': '122',
'Bikes available (free)': '123',
'Concierge': '124',
'Entertainment staff': '125',
'Nightclub/DJ': '126',
'Private check-in/out': '127',
'Shuttle service (free)': '128',
'Shuttle service (additional charge)': '129',
'Ski rental on site': '130',
'Ski pass vendor': '131',
'Ski-in, ski-out access': '132',
'Special diet meals (on request)': '133',
'Suit press': '134',
'Vending machine (drinks)': '135',
'Vending machine (snacks)': '136',
'Water sports facilities on site': '137',
'Hot spring bath': '138',
'Airport shuttle (free)': '139',
'Airport shuttle (additional charge)': '140',
'Shared kitchen': '141',
'Lockers': '142',
'Shared lounge/TV area': '143',
"Kids' club": '144',
'Convenience store on site': '145',
'Beachfront': '146',
'Evening entertainment': '147',
'Water park': '148',
'Adults only': '149',
'Detached - Entire property': '150',
'Semi-detached': '151',
'Privately-owned apartment': '152',
'Ground floor (private access)': '153',
'Ground floor (shared access)': '154',
'Upper floor - elevator': '155',
'Upper floor - stairs': '156',
'Wheelchair accessible': '185',
'Daily housekeeping': '158',
'Grocery deliveries': '159',
'Parking on site': '160',
'Private Parking': '161',
'Misc parking': '162',
'WiFi in all areas': '163',
'Paid WiFi': '164',
'Michelin-star Dining': '165',
'Open-air bath': '166',
'Public Bath': '167',
'Waterslide': '168',
'Swimming pool toys': '169',
'Board games/Puzzles': '170',
'Books, DVDs & music for kids': '171',
'Indoor play area': '172',
'Outdoor play equipment for kids': '173',
'Baby safety gates': '174',
"Kids' TV channels": '175', "Kids' meals": '176',
'Kid-friendly buffet': '177',
'Sofa Bed': '178',
'Secure parking': '179',
'Street parking': '180',
'Parking garage': '181',
'Electric vehicle charging station': '182',
'Public transit tickets': '183',
'Accessible parking': '184',
'Toilet with grab rails': '186',
'Raised toilet': '187',
'Lowered sink': '188',
'Bathroom emergency cord': '189',
'Rooftop pool': '192',
'Infinity pool': '193',
'Pool with view': '194',
'Heated pool': '195',
'Saltwater pool': '196',
'Plunge pool': '197',
'Pool/Beach towels': '198',
'Pool bar': '199',
'Shallow end': '200',
'Pool cover': '201',
'Wine/Champagne': '203',
'Bottle of water': '204',
'Fruit': '205',
'Chocolate/Cookies': '206',
'Tickets to shows/attractions': '207',
'Airport pickup': '209',
'Airport drop-off': '210',
'Visual aids (Braille)': '211',
'Visual aids (tactile signs)': '212',
'Auditory guidance': '213',
'Strollers': '214',
'Tennis equipment': '215',
'Badminton equipment': '216',
'Pet basket': '217',
'Pet bowls': '218',
'Coffee house on site': '219',
'Beach chairs/Loungers': '220',
'Beach umbrellas': '221',
'Outdoor furniture': '222',
'Fenced pool': '223',
'Picnic area': '224',
'Outdoor fireplace': '225',
'Beauty services': '226',
'Facial treatments': '227',
'Waxing services': '228',
'Makeup services': '229',
'Hair treatments': '230',
'Manicure': '231',
'Pedicure': '232',
'Haircut': '233',
'Hair coloring': '234',
'Hairstyling': '235',
'Body treatments': '236',
'Body scrub': '237',
'Body wrap': '238',
'Light therapy': '239',
'Spa facilities': '240',
'Steam room': '241',
'Spa lounge/Relaxation area': '242',
'Foot bath': '243',
'Spa/Wellness packages': '244',
'Back massage': '245',
'Neck massage': '246',
'Foot massage': '247',
"Couples' massage": '248',
'Head massage': '249',
'Hand massage': '250',
'Full-body massage': '251',
'Massage chair': '252',
'Fitness': '253',
'Yoga classes': '254',
'Fitness classes': '255',
'Personal trainer': '256',
'Locker rooms': '257', "Kids' pool": '258',
'Beach': '302',
'Special baths': '303',
'Shuttle service': '304',
'Breakfast options': '305',
'Game drives': '306',
'The Big Five': '311',
'Walking Safari': '312',
'Bush Dinner': '313',
'Game Drives': '310',
'Temporary art galleries': '400',
'Bar crawls': '401',
'Stand-up comedy': '402',
'Movie nights': '403',
'Walking tours': '404',
'Bike tours': '405',
'Themed dinners': '406',
'Happy hour': '407',
'Tour or class about local culture': '408',
'Cooking class': '409',
'Live music/Performance': '410',
'Live sports events (broadcast)': '411',
'Archery': '412',
'Aerobics': '413',
'Bingo': '414',
'Downhill Skiing': '415',
'24-hour security': '418',
'Key access': '419',
'Key card access': '420',
'Security alarm': '421',
'Smoke alarms': '422',
'CCTV in common areas': '423',
'CCTV outside property': '424',
'Fire extinguishers': '425',
'Bicycle parking': '426',
'Telephone': '427',
'Postal service': '428',
'Laundry room': '429',
'Ski shuttle': '430',
'Bath/Hot spring': '431',
'Private bath': '432',
'No single-use plastics': '434',
'Guests have the option to reuse towels': '436',
'Carbon monoxide detector': '437',
'Carbon monoxide sources': '438',
'Key card or motion-controlled electricity for guests': '444',
'Guests can opt out of daily cleaning service': '445',
'Water cooler/dispenser': '446',
'Bicycle rental': '447',
'Use of cleaning chemicals that are effective against coronavirus': '449',
'Linens, towels, and laundry washed in accordance with local authority guidelines': '450',
'Guest accommodation disinfected between stays': '451',
'Guest accommodation sealed after cleaning': '452',
'Physical distancing in dining areas': '453',
'Food can be delivered to guest accommodation': '454',
'Staff follow all safety protocols as directed by local authorities': '455',
'Shared stationery (e.g. printed menus, magazines, pens, paper) removed': '456',
'Hand sanitizer in guest accommodation and common areas': '457',
'Process in place to check health of guests': '458',
'First aid kits available': '459',
'Contactless check-in/out': '460',
'Cashless payment available': '461',
'Physical distancing rules followed': '462',
'Mobile app for room service': '463',
'Screens or physical barriers between staff and guests in appropriate areas': '464',
'Invoice provided': '465',
'Property cleaned by professional cleaning companies': '466',
'All plates, cutlery, glasses, and other tableware sanitized': '467',
'Guests have the option to cancel any cleaning services for their accommodation during their stay': '468',
'Passport/ID info collected online before you arrive': '470',
'Check-in kiosk in the lobby': '471',
'Lockbox key collection at the property': '472',
'Lockbox key collection near the property': '473',
'Digital key access': '474',
'Breakfast to-go containers': '484',
'Delivered food covered securely': '485',
'Access to healthcare professionals': '486',
'Thermometers for guests provided by property': '487',
'Face masks for guests available': '488',
"Wild (non-domesticated) animals aren't displayed or interacted with while kept at the property, nor are they harvested, consumed, or sold.": '489',
'Recycling bins are available to guests and waste is recycled': '490',
'At least 80% of food is sourced from your region': '491',
'At least 80% of lighting uses energy-efficient LED bulbs': '492',
'Only using water-efficient toilets (e.g. low-flow toilets, dual flush toilets)': '493',
'Only using water-efficient showers (e.g smart showers, low-flow shower heads)': '494',
'All windows are double-glazed': '495',
'Food waste policy in place that includes education, food waste prevention, reduction, recycling, and disposal': '496',
'A percentage of revenue is invested back into community or sustainability projects': '497',
'Compensate for at least 10% of total annual carbon emissions by purchasing certified carbon offsets': '498',
'Tours and activities organized by local guides and businesses': '499',
'Vegetarian menu options available': '500',
'Vegan menu options available': '501',
'Green spaces like (rooftop) gardens at the property': '502',
'At least 80% of provided food is organic': '503',
'100% renewable electricity used throughout the property': '504',
'Local artists are offered a platform to display their talents': '508',
'Provide guests with info about local ecosystems, history, culture, and visitor etiquette': '506',
'100% renewable energy is used throughout the property': '507',
'Provide guests with information regarding local ecosystems, heritage and culture, as well as visitor etiquette': '510',
'Indoor fireplace': '511',
'Breakfast to go': '514',
'': 'other'
}
filters_values = list(filters_indices.keys())
unused_filters = filters_values.copy()

# Asks ChatGPT which city is appropriate, and which preferences correspond to hard filters.
def GPT_enquiry(item: dict) -> tuple[str, list[str]]:  
    prompt_message = f"""
    Preferences:
    {item}

    Hard Filters:
    {filters_values}

    Based on the preferences, please suggest the most suitable city. Respond strictly in the following format:

    "City Name: [City Name]"

    Also, match the hard filters to the user input and create a dictionary of relevant filters in the following format:

    "[Filter Name]: [True/False]"

    Ensure the response contains only the required information and no additional text.
    """

    messages = [{"role": "user", "content": prompt_message}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

    response_content = response.choices[0].message.content
    print(response_content)
    # Extract City Name
    match = re.search(r'City Name:\s*(.+)', response_content)
    location = match.group(1).strip() if match else ""

    # Extract and collate which filters (corresponding keys) are requested
    bool_dict = {True: [], False: []}
    for filter in filters_values:
        match = re.search(rf"\[{re.escape(filter)}\]:\s*(True|False)", response_content)
        if match:
            bool_dict[match.group(1).strip() == "True"].append(filter)
    category_filter_string = []
    for filter in bool_dict[True]:
        category_filter_string.append(f"facility::{filters_indices[filter]}" for filter in bool_dict[True])
        unused_filters.remove(filter)
    for filter in bool_dict[False]:
        unused_filters.remove(filter)
    return location, category_filter_string

def GPT_filter_suggestion(results, unused_filters):
    prompt_message = f"""
    Results:
    {results}

    Available Filters:
    {unused_filters}

    Based on the results and available filters above, suggest 5 filters that would best refine the search. Provide the filter names in the following format:

    "[Filter Name],"

    Do not include any extra text or explanation.
    """
    messages = [{"role": "user", "content": prompt_message}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

    response_content = response.choices[0].message.content
    print(response_content)
    return response_content.split(",")

@router.get("/search")
async def search(item: Filters, full_results: bool = False) -> list[dict] | tuple[int, list[str]]:
    loc, category_filter_string = GPT_enquiry(item)
    bcomIn = {}
    bcomIn["destination"] = loc
    bcomIn["categories"] = category_filter_string
    bcomIn["checkin_date"] = item["checkin_date"] # Double check the JSON contents of a query
    bcomIn["checkout_date"] = item["checkout_date"]
    bcomIn["adults_number"] = item["adults_number"]
    bcomIn["children_number"] = item["children_number"]
    
    results = list(bca.search_booking(bcomIn).values())
    num_results = len(results)
    suggested_filters = GPT_filter_suggestion(results, unused_filters)
    if full_results:
        return {"results": results}
    else:
        return {"num_results": num_results, "suggested_filters": suggested_filters}