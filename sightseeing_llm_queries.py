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


def cluster_groups_by_geographical_data(attractions_list, chat_history):
    system_instruction = system_instruction_for_clustering_attractions_geographically
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, cluster the attractions based on their geographical data. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_timings_for_attractions(attractions_list, chat_history):
    system_instruction = system_instruction_for_getting_best_times_to_visit
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, give the best times for the attractions based on the api results and google saerch and your training data. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_budget_reasoning_for_attractions(attractions_list, chat_history):
    system_instruction = system_instruction_for_budget_reasoning
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, give the budget based attractions. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_day_wise_itinerary(chat_history, geographical_reasoning, time_based_reasoning, budget_reasoning, attractions, shortlisted_attractions, duration_analysis):
    system_instruction = system_instruction_for_day_wise_planning
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history, geographical reasoning, time based reasoning ,budget reasoning, duration analysis, original(complete attractions list) and shortlisted_attraction list(done by another llm based on what it thought are user's preferences) give the day wise itinerary. \n\n chat history : {chat_history} \n\n geographical reasoning : {geographical_reasoning} \n\n time based reasoning : {time_based_reasoning} \n\n budget reasoning : {budget_reasoning} \n\n duration analysis : {duration_analysis} \n\n original attractions list : {attractions}, \n\n shortlisted attractions : {shortlisted_attractions}", history, chat, system_instruction)
    return history[-1]["parts"][0]

def summarise_attractions(attractions_list, chat_history):
    system_instruction = system_instruction_for_summarising_search_json
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, summarise the attractions. Keep in mind that your output is the input for other llm agents which will perform further analysis on the attractions so your description of the attraction must be detailed enough for it to be helpful to any and all cases of analysis. Attractions list : {attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def remove_redundant_attractions(summarised_attractions_list, chat_history):
    system_instruction = system_instruction_for_removing_redundant_attractions
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, remove the redundant attractions. Attractions list : {summarised_attractions_list} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_duration_analysis_of_attractions(summarised_attractions, chat_history):
    system_instruction = system_instruction_for_duration_analysis
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history and attractions list, give the duration analysis of the attractions. Attractions list : {summarised_attractions} \n\n chat history : {chat_history} ", history, chat, system_instruction)
    return history[-1]["parts"][0]

def get_intraday_planning(attractions, chat_history, day_wise_itinerary, duration_analysis, clustered_attractions, time_based_attrations):
    system_instruction = system_instruction_for_intraday_planning
    history, chat, _ = start_chat(system_instruction)
    history, chat = send_message(f"Based on the given chat history, attractions, day wise itinerary, duration analysis, clustered attractions, time based attractions and budget reasoned attractions, give the intraday planning. \n\n chat history : {chat_history} \n\n attractions : {attractions} \n\n day wise itinerary : {day_wise_itinerary} \n\n duration analysis : {duration_analysis} \n\n clustered attractions : {clustered_attractions} \n\n time based attractions : {time_based_attrations} \n\n", history, chat, system_instruction)
    return history[-1]["parts"][0]
summarised_attractions = summarise_attractions(attractions, chat_history)
redundancy_removed_attractions = remove_redundant_attractions(summarised_attractions, chat_history)
shortlisted_attractions = shortlist_attractions(redundancy_removed_attractions, chat_history)
# day_wise_itinerary = (get_per_day_itinerary(shortlisted_attractions, chat_history))
duration_analysis = get_duration_analysis_of_attractions(shortlisted_attractions, chat_history)
clustered_attractions = cluster_groups_by_geographical_data(shortlisted_attractions, chat_history)
time_based_attractions = get_timings_for_attractions(shortlisted_attractions, chat_history)
budget_reasoned_attractions = get_budget_reasoning_for_attractions(shortlisted_attractions, chat_history)

day_wise_itinerary = get_day_wise_itinerary(chat_history, clustered_attractions, time_based_attractions, budget_reasoned_attractions, attractions, shortlisted_attractions, duration_analysis)

intraday_planning = get_intraday_planning(attractions, chat_history, day_wise_itinerary, duration_analysis, clustered_attractions, time_based_attractions)
