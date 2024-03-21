# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from urllib.request import urlopen
import json
from string import Template
import requests
import logging
logging.getLogger().setLevel(logging.INFO)
from string import Template
import functools

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
         return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to LANGUAGE team prototype lab, you can say any disease name."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class DiseaseQueryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DiseaseQuery")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        diseaseName = handler_input.request_envelope.request.intent.slots.LSQuery.value
        logging.info(handler_input.request_envelope.request.intent.slots)
        response_disease = requests.post('http://137.226.232.26:8080/api/v1/category/6', json={
         "diseaseName": diseaseName,
         "limit": 3
           })
        response_answer = response_disease.json()['genes']
        return handler_input.response_builder.speak(response_answer).reprompt(response_answer).response


#class DiseaseQueryIntentHandler(AbstractRequestHandler):
#    """Handler for Question Inyent."""

#    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
#        return ask_utils.is_intent_name("DiseaseQueryIntent")(handler_input)


#    def handle(self, handler_input):
#        # type: (HandlerInput) -> Response
 #       diseaseName = handler_input.request_envelope.request.intent.slots.LSQuery.value
  #      logging.info(handler_input.request_envelope.request.intent.slots)
#
 #       #country = slots["name"].value

  #      response = requests.post('http://137.226.232.26:8080/api/v1/category/6', json={
   #         "diseaseName": diseaseName,
    #        "limit": 3
     #   })
        # response.status_code,
      #  response_disease = json['genes']
        #return response.json()


        #template = Template("""
#
 #               http://137.226.232.26:8080/$country/capital
  #              """)

   #     link = template.substitute(country=''.join(country))
    #    response = urlopen(link)

        # Convert bytes to string type and string type to dict
        #string = response.read().decode('utf-8')
        #json_obj = json.loads(string)
        #capital = json_obj['capital']
        #capital = "The capital of" + link + " is " + capital


        # cids = get_disease(name, 'name')
        # if not cids:
        #     speech_text = "Sorry, I could not find {} on the database. What else can I do for you?".format(name)
        # else:
        #     Disease = get_parameters(cids)
        #
        #     if Disease is None:
        #         speech_text = "Sorry, I could not find the details of {} on Databse. What else can I do for you?".format(
        #             name)
        #     else:
        #         speech_text = "Yes, this is the disease of {} and you can ask details about it. What else can I do for you?".format(
        #             name)

       # return handler_input.response_builder.speak(response_disease).reprompt(response_disease).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DiseaseQueryIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
