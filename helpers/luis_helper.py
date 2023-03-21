# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails

from luis_utility import LuisApp

def predict_to_book_details(luis_recognizer : LuisApp, text: str, Intent):
    result = None
    intent = None
    try:
        prediction, intent = luis_recognizer.predict(text,get_intent=True)
        ## LuisApp => predict => result, intent
    
        if intent == Intent.BOOK_FLIGHT.value:
            result = BookingDetails()
            for k,v in prediction.items():
                if k == "dst_city":
                    result.destination = v
                elif k == "or_city":
                    result.origin = v
                elif k == "str_date":
                    if result.check_date(v):
                        result.start_date = v
                elif k == "end_date":
                    if result.check_date(v):
                        result.end_date = v
                elif k == "n_adult":
                    if result.check_n_adult_or_children(v):
                        result.n_adult = v
                elif k == "n_children":
                    if result.check_n_adult_or_children(v):
                        result.n_children = v
                elif k == "budget":
                    if result.check_budget(v):
                        result.budget = v
                elif k == "seat":
                    result.seat = v

    except Exception as exception:
        print(exception)

    return intent, result
    
class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    CANCEL = "Cancel"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisApp, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        return predict_to_book_details(luis_recognizer,turn_context.activity.text,Intent)