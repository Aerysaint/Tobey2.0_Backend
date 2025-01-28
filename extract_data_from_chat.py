from geminiFunctions import *

# from sightseeing_llm_queries import *
# from tbo_general import *
from tbo_sightseeing_queries import *
from prompts_and_sys_instructions import *
from make_json_searchable import *
###for testing

# print("Starting")
# with open("init_chat_history.txt", "r") as f:
#     history = eval(f.read())
# print(history)

# print(type(history))
# print(history)

attractions_list = None
def get_country_code(history, chat=None):
    country_list = get_country_list()
    system_instruction = system_instruction_for_getting_country_code
    newHistory, newChat, __ = start_chat(system_instruction)
    newHistory,chat = send_message(f"Based on this chat history, and the given json, extract the country code. json : {country_list}. \n\n chat history : {history}", newHistory, newChat, system_instruction)
    return newHistory[-1]["parts"][0]["text"]

# country_code = get_country_code(history, chat)
# print(country_code)

def create_user_detail_json(history, chat=None):
    system_instruction = system_instruction_for_creating_user_detail_json
    newHistory, newChat, _ = start_chat(system_instruction)
    newHistory, newChat = send_message("Populate the json with the given history as expected. Here's the chat history : \n\n" + str(history), newHistory, newChat, system_instruction)
    country_code = get_country_code(history, chat)
    country_code = country_code.strip()
    print(country_code)
    city_list = get_city_list(country_code)
    print(city_list)
    newHistory, newChat = send_message(f"Based on the given country code, and the city list, give me the final json. You're supposed to check if the country code is correctly populated, and the CityId is correctly populated.Note that Country Code is a two letter word, for example AE for Dubai. City code is a 6 digit numeric string, for example 148767 for Yelagiri, Tamil Nadu. In case there are multiple cities, add them as a list and in case there are multiple countries, add them as a list too. Country code : {country_code}, CityList : {city_list}", newHistory, newChat, system_instruction)
    return newHistory[-1]["parts"][0]["text"]

def get_user_json(history):
    chat = None
    js = create_user_detail_json(history, chat)


    if(js[0] == '`'):
        js = js[7:]
        js = js[:-4]

    js  = convert_string_to_json(js)
    # print(js)
    js = handle_multi_country(js)
    js = handle_multi_city(js)
    js = handle_child_ages(js)
    lst = get_attractions_list_for_multiple_destinations(js)
    attractions_list = lst
    return attractions_list