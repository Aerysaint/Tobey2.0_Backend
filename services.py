import sightseeing_llm_queries as llm
import firebase_handler as fh


def convertLlmActivityToActivity(llm_activity):
    ans = {}
    ans["Name"] = llm_activity["SightseeingName"]
    ans['Price'] = llm_activity["price"]
    ans['Currency'] = llm_activity['currency']
    ans['ImageList'] = llm_activity["image_url"]
    ans['FromDate'] = llm_activity["FromDate"]
    ans['ToDate'] = llm_activity["ToDate"]
    ans['tbo_description'] = llm_activity["tbo_description"]
    ans['llm_description'] = llm_activity["llm_description"]
    ans['rating'] = llm_activity["ai_rating"]
    ans["CityName"] = llm_activity["city_name"]
    return ans


def convert_llm_itinerary(llm_itinerary):
    ans = []
    for k, v in llm_itinerary.items():
        for curr in v:
            ans.append(convertLlmActivityToActivity(curr))
    return ans


def convertTboToActivity(tbo_activity):
    ans = {}
    ans["Name"] = tbo_activity["SightseeingName"]
    ans["CityName"] = tbo_activity["CityName"]
    ans['ImageList'] = tbo_activity["ImageList"]
    ans['Price'] = tbo_activity["Price"]['BasePrice']
    ans['Currency'] = tbo_activity["Price"]['CurrencyCode']
    return ans


def convertTboToActivities(tbo_activities):
    ans = []
    for curr in tbo_activities:
        for activity in curr['Response']['SightseeingSearchResults']:
            ans.append(convertTboToActivity(activity))
    return ans


def additinerary(hist, sessionid):
    final = llm.get_itinerary_after_chat(hist, sessionid)
    final = convert_llm_itinerary(final)
    for activity in final:
        fh.add_activity_to_itinerary(sessionid, activity)


def addAllAttractions(attractions, sessionid):
    ans = convertTboToActivities(attractions)
    fh.add_activities(sessionid, ans)
    print("added attractions")


def addTimeToActivity(activity, fromdate, todate):
    activity['FromDate'] = fromdate
    activity['ToDate'] = todate
    return activity
