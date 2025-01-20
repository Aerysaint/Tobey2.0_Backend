from geminiFunctions import *
from prompts_and_sys_instructions import *
import json

with open("delhi_attractions.json") as f:
    attractions = json.load(f)

with open("init_chat_history.txt") as f:
    chat_history = (f.read())
def shortlist_attractions(attractions_list, chat_history):
    system_instruction = system_instruction_for_shortlisting_attractions
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, shortlist the attractions. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_per_day_itinerary(attractions_list, chat_history):
    system_instruction = system_instruction_for_geographical_contraint_planning_inter_day
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, plan the itinerary. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

# shortlisted_attractions = shortlist_attractions(attractions, chat_history)
# day_wise_itinerary = (get_per_day_itinerary(shortlisted_attractions, chat_history))
# intraday_itinerary = get_intraday_itinerary(day_wise_itinerary, chat_history)