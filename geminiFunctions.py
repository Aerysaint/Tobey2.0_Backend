import json
import time
import prompts_and_sys_instructions
from google import genai
from google.genai import types
import re
from prompts_and_sys_instructions import *
creds = json.load(open("credentials.json"))

client = genai.Client(api_key=creds["GEMINI_API_KEY"])

safety_settings = [types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH")]

def convert_string_to_json(input):
    match = re.search(r'\{', input)
    input = input[match.start():]
    input = input.replace("false", "False")
    input = input.replace("true", "True")
    input = input.replace("null", "None")
    return eval(input)
def getGeminiResponse(system_instructions, prompt, history, chat):
    # print("prompt is ",prompt)
    generation_config = types.GenerateContentConfig(system_instruction=system_instructions, safety_settings=safety_settings)
    if chat is None:
        # print("creating new chat with \n", history)
        chat = client.chats.create(model="gemini-2.0-flash-exp", history=history, config=generation_config)
    while True:
        try:
            response = chat.send_message(prompt)
            break
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            print("Retrying...")
            continue
    return response.text, chat

def start_chat(system_instructions):
    """Initializes a new chat and returns an empty history and chat object."""
    history = []
    chat = None
    return history, chat, system_instructions


def format_history(history):
    formatted_history = []
    for turn in history:
        if turn["role"] == "user":
            formatted_history.append({"parts": [{"text":turn["parts"][0]}]})
        elif turn["role"] == "model":
            formatted_history.append({"parts": [{"text": turn["parts"][0]}]})
    return formatted_history
def send_message(prompt, history, chat, system_instructions):

    """Sends a message to the chat and updates the history."""
    # print(formatted_history)
    # time.sleep(5)
    # history.append({"role": "user", "parts": [{"text" : prompt}]})
    try:
        response, chat = getGeminiResponse(system_instructions, prompt,history, chat)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return history, chat  # Return original history and chat in case of error

    history.append({"role": "user", "parts": [{"text": prompt}]})
    history.append({"role": "model", "parts": [{"text" : response}]})
    return history, chat

def next_message_for_initial_chat(history):
    message = history[-1]["parts"][0]["text"]
    system_instruction = system_instructions_for_initial_chat
    chat = client.chats.create(model="gemini-2.0-flash-exp", history=history, config=types.GenerateContentConfig(system_instruction=system_instruction, safety_settings=safety_settings))
    response = chat.send_message(message)
    return response.text

def next_message_for_ai_chat(history, curr_itinerary, attractions):
    message = history[-1]["parts"][0]["text"]
    system_instruction = system_instruction_for_ai_chat
    system_instruction += "here is the current complete itinerary\n\n" + str(curr_itinerary) + "\n\n"
    system_instruction += "here is the complete list of attractions\n\n" + str(attractions) + "\n\n"
    chat = client.chats.create(model="gemini-2.0-flash-exp", history=history, config=types.GenerateContentConfig(system_instruction=system_instruction, safety_settings=safety_settings))
    while True:
        try:
            response = chat.send_message(message)
            break
        except Exception as e:
            print("Something when wrong in the summoning")
            print(e)
            continue
    return response.text

def get_attraction_llm_description(attraction, curr_itinerary, chat_history):
    system_instruction = system_instruction_for_llm_description
    system_instruction += "Here is the current complete itinerary\n\n" + str(curr_itinerary) + "\n\n"
    system_instruction += "Here is the chat history\n\n" + str(chat_history) + "\n\n"
    chat = client.chats.create(model="gemini-2.0-flash-exp", history=chat_history, config=types.GenerateContentConfig(system_instruction=system_instruction, safety_settings=safety_settings))
    while True:
        try:
            response = chat.send_message(attraction)
            break
        except Exception as e:
            print("Something went wrong in the descriptioning")
            print(e)
            continue
    return response.text

def get_search_result(query, curr_itinerary, attractions):
    system_instruction = system_instruction_for_search
    system_instruction += "Here is the current complete itinerary\n\n" + str(curr_itinerary) + "\n\n"
    system_instruction += "Here is the complete list of attractions\n\n" + str(attractions) + "\n\n"
    chat = client.chats.create(model="gemini-2.0-flash-exp", history=[], config=types.GenerateContentConfig(system_instruction=system_instruction, safety_settings=safety_settings))
    result = []
    while True:
        try:
            response = chat.send_message(query)
            resp = response.text
            if resp[0] == "`":
                resp = resp[7:]
                resp = resp[:-4]
            result = convert_string_to_json(resp)
            lst = []
            for i in result:
                lst.append(i)
            result = lst
            break
        except Exception as e:
            print("Something went wrong in the search")
            print(e)
            continue
    return result


# Example usage:
# system_instructions = prompts.base_system_instruction + prompts.system_instruction_for_sorting_attractions_based_on_time
# history, chat, system_instructions = start_chat(system_instructions)  # Start a new chat

# First message
# history, chat = send_message("This is the list of attractions : Qutub Minar, Nehru Place Market, Jama Masjid, Red Fort, Lotus Temple, Kalkaji Market, Humayun's Tomb, Select City Walk Saket. I want to go somewhere in the morning, around 10am. Keep in mind that I'm a Hindu and a tech fanatic.", history, chat, system_instructions)

# Second message (continuing the conversation)
# history, chat = send_message("Are there any other places I should consider?", history, chat, system_instructions)

# Third message
# history, chat = send_message("How much time will each take?", history, chat, system_instructions)
