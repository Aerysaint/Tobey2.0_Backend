from geminiFunctions import *
from prompts_and_sys_instructions import *
from tbo_hotel_queries import *
def sort_hotels_for_user(city_code, chat_history):
    hotels_list = get_hotels_list(city_code)
    hotels_list = hotels_list["Hotels"]
    system_instruction = system_instruction_for_sorting_hotels
    history, chat, __ = start_chat(system_instruction)
    while True:
        try:
            history, chat = send_message(f"Based on this chat history, and the given json, sort the hotels. json : {hotels_list}. \n\n chat history : {chat_history} \n\n. Remember your response must be a valid python list as your response will be fed directly to eval function in python.", history, chat, system_instruction)

            response = history[-1]["parts"][0]["text"]
            if response[0] == '`':
                response = response[7:]
                response = response[:-4]
            lst = eval(response)
            return lst
        except Exception as e:
            print("Something went wrong in the sorting")
            print(e)
            continue

