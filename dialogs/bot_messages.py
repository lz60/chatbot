# contains the bot's display strings (not all because some are built on the heap)

class BotSentences:
    """Sentences of the booking bot"""

    # messages d'accueil
    WELCOME = "How can I help you with today?"
    WELCOME_AGAIN = "What else can I do for you?"

    # Intent detection message
    INTENT_NONE = "Sorry, I didn't get that. Please try asking in a different way"

    # booking inquiry messages
    BOOK_REQUEST_DST_CITY = "Where would you like to travel to?"
    BOOK_REQUEST_OR_CITY = "From what city will you be travelling?"
    BOOK_REQUEST_STR_DATE_1 = "On what date would you like to start your travel?"
    BOOK_REQUEST_STR_DATE_2 = "I'm sorry, for best results, please enter the start date of your travel including the month, day and year."
    BOOK_REQUEST_END_DATE_1 = "On what date would you like to end your travel?"
    BOOK_REQUEST_END_DATE_2 = "I'm sorry, for best results, please enter the end date of your travel including the month, day and year."
    BOOK_REQUEST_BUDGET = "What will be the budget for your trip?"
    BOOK_REQUEST_ADULT = "How many adult will attend your trip?"
    BOOK_REQUEST_CHILDREN = "How many children will attend your trip?"
    BOOK_REQUEST_CLASS = "What seat class would you like : business or premiere or economic ?"
    BOOK_FINAL_CONFIRMATION = "Do you want to confirm your booking details?"
    BOOK_COMPLETED_BOOKING = "Great ! Your flight is booked. What else can I do for you ?"

    # messages asking for confirmation of the information detected by LUIS
    LUIS_CONFIRMATION_INTRO = "Please confirm if the following informations are correct :"
    LUIS_CONFIRMATION_USER_NO = "Sorry for the inconvenience and thank you for the feedback. Can I do something else for you ?"
    LUIS_CONFIRMATION_INTENT_BOOK = "You want to book a flight"

    # messages acknowledging the non-confirmation
    BOOK_CONFIRMATION_NO = "Ok, giving up the booking process."

    # messages validating the reservation
    BOOK_VALIDATE_REQUEST = "Validating your request: checking database..."

    # Cancel message
    CANCEL = "Cancelling..."

    # Help message
    HELP = "Type 'cancel' or 'quit' to cancel current process."

    # generic date request messages
    DATE_REQUEST = "Enter a date"
    DATE_REQUEST_2 = "Please, enter a date, including the month, day and year."  

    # generic error messages
    ERROR_BUG = "The bot encountered an error or bug."
    ERROR_FIX = "To continue to run this bot, please fix the bot source code."