# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model import Response

from dicts import prefixes, disease_dict
from helpers import dataframe_formatter, dataFrame_extractor, definition_printer, casuation_printer, formate_name, association_printer, definition_name_formatter

from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template
import pandas as pds

sparql = SPARQLWrapper("http://rdf.disgenet.org/sparql/")


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



########################################################################################
# Extracts the sting of the slot from the intent input
def get_value(handler_input, slot_name):
    return get_slot_value(handler_input = handler_input, slot_name = slot_name)


############### specific intent helpers and api callers ########################################
def definitionApi(name):
    #name formating to remove apostrophe s
    name = definition_name_formatter(name)
        
    # using disease_dict mapper to get the DOID 
    ids = disease_dict[name]
    
    # using stinrg template we can make our queries dynamic
    template = Template(
        """
    $prefix

    SELECT DISTINCT ?umls ?umlsTerm ?l ?comment ?doid
    WHERE { 
	?gda sio:SIO_000628 ?umls .
	?umls dcterms:title ?umlsTerm ;
		skos:exactMatch ?doid;
        rdfs:comment ?comment;
      rdfs:label ?l.
	FILTER regex(?umls, "umls/id")
    FILTER (?doid=obo:DOID_$id)
  
    }
    LIMIT 20
        """
    )
    
    
    # setting our querey variables
    s = template.substitute(prefix=''.join(prefixes), id=ids)

    # going on our API 
    sparql.setQuery(s)
    
    # setting the result as a JSON
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if(len(results) == 0):
        return 'Sorry I dont have any results'


    # the following 4 lines are for formating the JSON into a Dataframe structure
    vars = results['head']['vars']
    bindings = results['results']['bindings']

    df = pds.DataFrame(list(map(lambda x: dataframe_formatter(x, vars), bindings)))
    
    # For the cols given, we remove the link part of the string and get the final ID
    df = dataFrame_extractor(df, ['umls', 'doid'], '/')
    

    # we use our printer function to formulate the output
    
    ### NOTE !!!!!
    # return only the first one, can be looped
    ## DONT FORGET 
    # return definition_printer(df, name)[0]
    return {
        'printer': definition_printer(df, name)[0],
        'dataframe': df
    }
########################################################################################
def causationApi(name):
    
    name = formate_name(name)
    
    template = Template(
        """
    $prefix

    SELECT DISTINCT ?gene str(?geneName) as ?name ?score 
    WHERE { 
	?gda sio:SIO_000628 ?gene,?disease ; 
		sio:SIO_000216 ?scoreIRI . 
	?gene rdf:type ncit:C16612 ;
		dcterms:title ?geneName . 
	?disease rdf:type ncit:C7057 ; 
		dcterms:title "$name"@en . 
	?scoreIRI sio:SIO_000300 ?score . 
	FILTER (?score >= 0.4) 
    } ORDER BY DESC(?score) 

    LIMIT 20
        """
    )

    s = template.substitute(prefix=''.join(prefixes), name = name)

    sparql.setQuery(s)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    vars = results['head']['vars']
    bindings = results['results']['bindings']

    df = pds.DataFrame(list(map(lambda x: dataframe_formatter(x, vars), bindings)))
    
    if (len(df) == 0):
        return 'Sorry coundnt find any genes associated with ' + name
    
    df = dataFrame_extractor(df, ['gene'], '/')
    df = df.sort_values(by=['score'], ascending=False)[:5]

    return {
        'printer': casuation_printer(df, name),
        'dataframe': df
    }
################################################################################################################################################
def get_associates(disease):
    
    diseaseUMLS = definitionApi(disease)['dataframe']['umls'][0]
    geneUMLS = causationApi(disease)['dataframe']['gene'][1]
    
    template = Template(
        """
    $prefix
    
    SELECT DISTINCT ?gda
    <http://linkedlifedata.com/resource/umls/id/$diseaseUMLS> as ?disease
    <http://identifiers.org/ncbigene/$geneUMLS> as ?gene 
    ?score ?source ?associationType	?pmid  ?sentence
    WHERE {
	        ?gda sio:SIO_000628
		        <http://linkedlifedata.com/resource/umls/id/$diseaseUMLS>,
		        <http://identifiers.org/ncbigene/$geneUMLS> ;
		        rdf:type ?associationType ;
		        sio:SIO_000216 ?scoreIRI ;
		        sio:SIO_000253 ?source .
	        ?scoreIRI sio:SIO_000300 ?score .
	        OPTIONAL {
		        ?gda sio:SIO_000772 ?pmid .
		        ?gda dcterms:description ?sentence .
	        }
    }
    
    LIMIT 2
        """
    )
    
    s = template.substitute(prefix=''.join(prefixes), diseaseUMLS = diseaseUMLS, geneUMLS = geneUMLS)
    sparql.setQuery(s)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    

    vars = results['head']['vars']
    bindings = results['results']['bindings']


    df = pds.DataFrame(list(map(lambda x: dataframe_formatter(x, vars), bindings)))

    if (len(df) == 0):
        return 'Sorry coundnt find any genes associated with ' + disease

    df = dataFrame_extractor(df, ['gene', 'disease', 'associationType', 'source', 'pmid', 'gda'], '/')
    #df = df.sort_values(by=['score'], ascending=False)[:5]

    return association_printer(df.head(min(2, len(df))), disease)


######################################## We use different intent hanlder for each intent in our skill ###############################################
class definitionHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("definition")(handler_input)

    def handle(self, handler_input):
        
        ## get the input value
        slot_value = get_value(handler_input , "diseaseDefinition")
        
        ## pass it to our helper function
        speach = definitionApi(slot_value)['printer']
        
        ## return the result as speach
        return (
            handler_input.response_builder
                .speak(speach)
                .ask(speach)
                .response
        )
######################################## 
class causationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("causation")(handler_input)

    def handle(self, handler_input):
        
        slot_value = get_value(handler_input , "deaseasCause")
        
        speach = causationApi(slot_value)['printer']

        return (
            handler_input.response_builder
                .speak(speach)
                .ask(speach)
                .response
        )
######################################## 
class associationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("association")(handler_input)

    def handle(self, handler_input):
        
        disease = get_value(handler_input , "diseaseAssociation")
        #rows = get_value(handler_input , "rows")
        
        #speach = get_associates(disease, rows)
        speach = get_associates(disease)
        return (
            handler_input.response_builder
                .speak(speach)
                .ask(speach)
                .response
        )

######################################## 
class variationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("variationIntent")(handler_input)

    def handle(self, handler_input):
        
        slot_value = get_value(handler_input , "diseaseVariation")
        
        speech = diseasevariantApi(slot_value)['printer']

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response
        )
######################################## 

class publicationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("publicationIntent")(handler_input)

    def handle(self, handler_input):
        
        slot_value = get_value(handler_input , "genediseaseass")
        
        speech = publicationApi(slot_value)['printer']

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response
        )
######################################## 

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello and Welcome to the bio KG skill! please, ask me a question!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



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
sb.add_request_handler(definitionHandler())
sb.add_request_handler(causationHandler())
sb.add_request_handler(variationHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()