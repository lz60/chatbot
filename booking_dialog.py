# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions, NumberPrompt, DateTimePrompt
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from botbuilder.schema import InputHints, Attachment
from .bot_messages import BotSentences
import re, os, json
from botbuilder.core.bot_telemetry_client import Severity

SEVERITY_LEVEL = {
    0: "DEBUG",
    1: "INFO",
    2: "WARNING",
    3: "ERROR",
    4: "CRITICAL",
}



class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client

        
        self.logger = logging.getLogger(__name__)

        text_prompt = TextPrompt(TextPrompt.__name__)

        number_prompt = NumberPrompt(NumberPrompt.__name__)

        date_prompt = DateTimePrompt(DateTimePrompt.__name__)

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.start_date_step,
                self.end_date_step,
                self.n_adult_step,
                self.n_children_step,
                self.budget_step,
                self.seat_step,
                self.confirm_step,
                self.final_step,
            ],
        )

        self.add_dialog(text_prompt)
        self.add_dialog(number_prompt)
        self.add_dialog(date_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        # waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__
         
        # Load the string corresponding to booking confirmation card
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "../cards/card_booking.json")
        with open(path) as card_file:
            self.booking_details_card = card_file.read()
        patterns = ['{dst_city}', '{or_city}', '{str_date}', '{end_date}', '{budget}', '{adult}', '{children}', '{seat_class}'] # placeholders de la card
        self.booking_details_card_regex = re.compile("(%s)" % "|".join(map(re.escape, patterns)))
        
        # Define user_messages, a list of all messages that a client wrote during a conversation
        self.user_messages = []
        
        # Defines performances log file
        self.performance_path = "performance_logs.csv"

        
    async def display_booking_details_summary(self, context, booking_details):
        """Display booking details"""
        details_dict = booking_details.to_dict()
        # Check placeholders and replace them by booking details
        card_text = self.booking_details_card_regex.sub(lambda mo: str(details_dict.get(mo.string[mo.start()+1:mo.end()-1], "")), 
                                                        self.booking_details_card)
        card = json.loads(card_text)
        attachment= Attachment(content_type="application/vnd.microsoft.card.adaptive", content=card)
        response = MessageFactory.attachment(attachment)
        await context.context.send_activity(response)        

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        booking_details = step_context.options
        booking_details.reset_turns()
        
        if booking_details.destination is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_DST_CITY)
                        
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_DST_CITY)
                ),
            )  # pylint: disable=line-too-long,bad-continuation
        
        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        
        if booking_details.origin is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_DST_CITY)
            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_OR_CITY)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def start_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        booking_details = step_context.options
        
        # Capture the response to the previous step's prompt
        booking_details.origin = step_context.result

        if booking_details.start_date is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_STR_DATE_1)
            
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_STR_DATE_1)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.start_date)

    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        booking_details = step_context.options
        
        # Capture the response to the previous step's prompt
        booking_details.start_date = step_context.result

        if booking_details.end_date is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_END_DATE_1)
            
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_END_DATE_1)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.end_date)

    async def n_adult_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        booking_details = step_context.options
        
        # Capture the response to the previous step's prompt
        booking_details.end_date = step_context.result

        if booking_details.n_adult is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_ADULT)
            
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_ADULT)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.n_adult)

    async def n_children_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        booking_details = step_context.options
        
        # Capture the response to the previous step's prompt
        booking_details.n_adult = step_context.result

        if booking_details.n_children is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_CHILDREN)
            
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_CHILDREN)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.n_children)


    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        booking_details = step_context.options
                
        booking_details.n_children = step_context.result

        if booking_details.budget is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_BUDGET)
            
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_BUDGET)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)


    async def seat_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        booking_details = step_context.options
                
        booking_details.budget = step_context.result

        if booking_details.seat is None:
            # Append user message in the user_message list and in the turn list
            booking_details.turns.append(step_context.context.activity.text)
            self.user_messages.append(step_context.context.activity.text)
            booking_details.turns.append(BotSentences.BOOK_REQUEST_CLASS)
            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(BotSentences.BOOK_REQUEST_CLASS)
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        
        return await step_context.next(booking_details.seat)


    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""

        booking_details = step_context.options

        booking_details.seat = step_context.result
        # Append user message in the user_message list and in the turn list
        booking_details.turns.append(step_context.context.activity.text)
        self.user_messages.append(step_context.context.activity.text)
        
        # Allows you to correctly format the date entered
        if type(booking_details.start_date) is str:
            start_date = booking_details.start_date
        else:
            start_date = booking_details.start_date[-1].value

        if type(booking_details.end_date) is str:
            end_date = booking_details.end_date
        else:
            end_date = booking_details.end_date[-1].value
        msg = (
            f"Please confirm you requested a flight from {booking_details.origin} to {booking_details.destination}. Your departure is on {start_date}. \
            and the return on {end_date}. Your budget is {booking_details.budget}$ and you need {booking_details.seat} class seats for {booking_details.n_adult} \
            adults and {booking_details.n_children} children."
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        
        booking_details = step_context.options
        
        if type(booking_details.start_date) is str:
            start_date = booking_details.start_date
        else:
            start_date = booking_details.start_date[-1].value

        if type(booking_details.end_date) is str:
            end_date = booking_details.end_date
        else:
            end_date = booking_details.end_date[-1].value
                          
        properties = {}
        properties["Turns"] = booking_details.turns
        properties["Destination"] = booking_details.destination
        properties["Origin"] = booking_details.origin
        properties["Start_date"] = start_date
        properties["End_date"] = end_date
        properties["Budget"] = float(booking_details.budget)
        properties["N_adult"] = int(booking_details.n_adult)
        properties["N_children"] = int(booking_details.n_children)
        properties["Seat"] = booking_details.seat

        if step_context.result:
            self.logger.setLevel(logging.INFO)
            self.logger.info('Good answer!')
            
            # If everything is OK, only track the metric that indicates the number of good confirmations
            self.telemetry_client.track_metric('BOOKING_CONFIRMATION', 1.0)
            print("Good answer")
            
            # Log datas in the performance file
            self.log_performances(properties, success="1")
                        
            # If everything is OK, send the summary to the user
            await self.display_booking_details_summary(step_context, booking_details)
            
            return await step_context.end_dialog(booking_details)

        
        self.logger.error("Bad answer!",extra={'custom_dimensions':properties})
        print("Bad answer")
        
        # Log datas in the performance file
        self.log_performances(properties, success="0")
        
        # If there is a problem and the user didn't confirm, track the metric and set a trace for further anlalysis        
        self.telemetry_client.track_trace('BOOKING_CONFIRMATION_NO', properties = properties, severity=Severity.warning)
        self.telemetry_client.track_metric('BOOKING_CONFIRMATION', 0.0)

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
        
    
    def log_performances(self, properties: dict, success:str):
        
        """Log performance datas for local analysis"""
        
        if not os.path.exists(self.performance_path):
            with open(self.performance_path, "w") as f:
                f.write("turns, dst_city, or_city, dep_date, ret_date, budget, adults, children, seat_class, success\n")
        
        with open(self.performance_path, "a") as f:
            f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(" | ".join(properties["Turns"]), properties["Destination"], properties["Origin"], properties["Start_date"], properties["End_date"], properties["Budget"], properties["N_adult"], properties["N_children"], properties["Seat"], success))
