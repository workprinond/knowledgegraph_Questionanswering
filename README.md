Biological data and knowledge bases increasingly rely on semantic Web technologies and the use of knowledge graphs for data in-tegration, retrieval and federated queries. People cannot answer verybasic questions related to key data assets in the domain. Eventually,this leads to lots of redundant work and unnecessary long developmentcycles. Alexa, a voice-enabled user interface was used on DisGeNET (abiological knowledge graph), to access information about the increasing amount of Semantic Web-based knowledge bases in biology.

Questions such as the following were asked to Alexa:
"what is melanoma?"
or 
"what causes melanoma?"

The reply was resolved through RDF queries implemented in the custom handlers, which returned back the results through SPARQL endpoint, and Alexa returned the results in SSML voice format.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Instructions:

Before diving into the architecture the user must use the invocation name to call the skill, in this case "language team". So to open our skill user must say, "Hey Alexa! open language team!"
and then ask questions like, "What are the top genes associated with Leukemia?"
Alexa will give a prompt reply.
There are currently the definition and the causation intent which is fully functionable. In future versions, more kinds of complex intents will be integrated.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Architecture of the knowledge graph skill

The architecture of ours skill is described in the following steps:
1.  In the beginning, the user asks the voice-enabled interface(Alexa) for a query related to medical database,The request is activated through an invocation name mentioned by the user.
2.  This  activates  the  lambda  function  associated  with  the  skill  in  the  back-ground.
3.  The request enters the language model of the model of the Alexa where it isconverted from speech to text.
4.  The text is structured in the form of proper JSON format.
5.  The JSON format then flows to our customized handler code where the coderecognizes which intent is appropriate to handle the query.
6.  The appropriate handler has the RDF query, which calls the API throughSPARQL and gets back the appropriate reason.
7.  The return result is formatted properly and converted to proper JSON out-put.
8.  The output is converted to SSML(Speech Synthesis Markup Language) whichis the synthetic audio of the result. This is an XML-based markup language for speech synthesis applications.
9.  Finally the synthetic audio is played back through Alexa to the user giving the appropriate answer.


# knowledgegraph_Questionanswering
# knowledgegraph_Questionanswering
