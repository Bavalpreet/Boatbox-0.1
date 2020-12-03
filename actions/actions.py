# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd


from sentence_transformers import SentenceTransformer, util
# class ActionRepair(Action):

#     def name(self) -> Text:
#         return "action_repair"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         parts= tracker.get_slot("boat_info")

#         part=parts[0] # we have extracted a list so extracting just the first entity
#         if part=='hull':
         
#             dispatcher.utter_message(text="""There are two scenarios where a %s can be damaged – one is when the
#       hull is damaged above the waterline, the second when it is damaged below the
#       waterline.For first scenario take it out and dry it thoroughly.For hull repair,
#       a basic fibreglass repair kit is used, using which the damaged section is removed
#       in a circular cut. The part can be then patched using either fibreglass and
#       the proper adhesives or the putties available."""%(part))
#         elif part=='core':
#             dispatcher.utter_message(text="""%s damage needs a professional help I would say pls visit a boat 
#             repair shop near you"""%(part))

#         return [SlotSet("boat_info", None)]



class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

            dispatcher.utter_message(text="Hi how can i help you with your boat")

            return []

    def loader(self):
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
        df=pd.read_csv('/home/bavalpreet/Downloads/boatbox/faq-rasa.csv')
        sentences=df['Questions'].str.replace("\n", "", case = False).tolist()
        solutions=df['Answers'].str.replace("\n", "", case = False).tolist()

        embeddings = model.encode(sentences)

        return [model,embeddings,solutions]


class Action_SpecificQ(ActionGreet):

    def name(self) -> Text:
        return "action_specificq"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]: 


            model,embeddings,solutions = ActionGreet.loader(self)

            message=tracker.latest_message['text']

            test=model.encode(message)

            #boat_part
            boat_part_slot = tracker.get_slot("boat_part") # this is a list slot so we will store all entities 
                                                    # extracted from an intent but if no entity is extracted
                                                    # tracker returns None Type value

            boat_part_slot=( [] if boat_part_slot is None else boat_part_slot)  # to convert None type to empty list

            # print(boat_part_slot,tracker.slots)

            # engine_series
            engine_series_slot=tracker.get_slot("engine_series")

            engine_series_slot= ( [] if engine_series_slot is None else engine_series_slot) # to convert None type to empty list

            
            # boat_manufacturer

            boat_manufacturer_slot=tracker.get_slot("boat_manufacturer")

            boat_manufacturer_slot= ( [] if boat_manufacturer_slot is None else boat_manufacturer_slot)


            # engine_manufacturer
            engine_manufacturer_slot=tracker.get_slot("engine_manufacturer")

            engine_manufacturer_slot= ( [] if engine_manufacturer_slot is None else engine_manufacturer_slot)

            # boat_length
            boat_length_slot=tracker.get_slot("boat_length")

            boat_length_slot= ( [] if boat_length_slot is None else boat_length_slot)

            # boat_model_slot

            boat_model_slot=tracker.get_slot("boat_model")

            boat_model_slot= ( [] if boat_model_slot is None else boat_model_slot)

            # year_of_manufacturing_slot

            year_of_manufacturing_slot=tracker.get_slot("year_of_manufacturing")

            year_of_manufacturing_slot= ( [] if year_of_manufacturing_slot is None else year_of_manufacturing_slot)

            # consumable

            consumable_slot=tracker.get_slot("consumable")

            consumable_slot= ( [] if consumable_slot is None else consumable_slot)

            # process

            process_slot=tracker.get_slot("process")

            process_slot= ( [] if process_slot is None else process_slot)

            # material

            material_slot=tracker.get_slot("material")

            material_slot= ( [] if material_slot is None else material_slot)




            total_info=boat_part_slot+engine_series_slot+boat_manufacturer_slot+engine_manufacturer_slot+boat_length_slot+boat_model_slot+year_of_manufacturing_slot+consumable_slot+process_slot+material_slot
            

                
     
            # Now after getting all diffrent types of slots No we have added them to boat_part_slot variable 
            # and then will make pattern to see any of these are available in our answers file
            
            # total_info=boat_part_slot+engine_series_slot
            
            print(total_info)
            sols_temp=pd.DataFrame(solutions) # converting our series to datatframe
             
            sols_temp.rename(columns = {0:'solutions'},  inplace = True)  # renaming the column
           
            try: # to handle any kind of exceptions in code
                if len(total_info)!=0 : # if an entity is extracted from user intent

                    
                    # to search all the strings in a list wthether in column or not                                     
                    # https://stackoverflow.com/questions/17972938/check-if-a-string-in-a-pandas-dataframe-column-is-in-a-list-of-strings
                    pattern = '|'.join(total_info)

                    checker= sols_temp[sols_temp['solutions'].str.contains(pattern,na=False)]  # checking if the extracted entity
                    # is present or not and if yes in which answers
                    
                    checker_index=list(checker.index.values) # storing the indexes of rows that were having our entity

                    sols_temp=sols_temp.iloc[checker_index] # now storing only those solutions that are shortlisted

                    if len(sols_temp) !=0: # if no solution is found after cosine similarity that can be because some 
                        # entities will not be present in your solution set

                        sols_temp.reset_index(level=0, inplace=True) # setting indexes again to normal

                        sols_temp.drop(columns=['index'],inplace=True) # dropping that unnecessary index column

                        emb= [embeddings[i] for i in checker_index] # stroing list of only those embeddings of questions 
                        # whose corresponding answer had the entity

                        cos_sim = util.pytorch_cos_sim(test, emb) #  cosine similarity
                            
                        cos_sim=cos_sim.tolist()
                        
                        sol_index=cos_sim[0].index(max(cos_sim[0])) # to get the index of maximum cosine similarity

                        # # p=pd.DataFrame(list(zip(cos_sim,solutions)),columns=['similarity','solutions'])
                        solution=sols_temp.iloc[[sol_index]]['solutions'][0]

                        dispatcher.utter_message(text=solution)
                        return [SlotSet("boat_part", None),SlotSet("engine_series", None),
                        SlotSet("boat_manufacturer", None),SlotSet("engine_manufacturer", None),SlotSet("boat_length", None)
                        ,SlotSet("boat_model", None),SlotSet("year_of_manufacturing", None),SlotSet("consumable", None)
                        ,SlotSet("process", None),SlotSet("material", None)]
                    else:
                        dispatcher.utter_message(text="Sorry  But can you Rephrase it again")

                        return [SlotSet("boat_part", None),SlotSet("engine_series", None),
                        SlotSet("boat_manufacturer", None),SlotSet("engine_manufacturer", None),SlotSet("boat_length", None)
                        ,SlotSet("boat_model", None),SlotSet("year_of_manufacturing", None),SlotSet("consumable", None)
                        ,SlotSet("process", None),SlotSet("material", None)]
                


                else:
                    dispatcher.utter_message(text="""Hey Really sorry but I couldn't find a Perfect Solution in my dictionary
                     for your query. But you can rephrase and Try It Again :) """)

                    return [SlotSet("boat_part", None),SlotSet("engine_series", None),
                        SlotSet("boat_manufacturer", None),SlotSet("engine_manufacturer", None),SlotSet("boat_length", None)
                        ,SlotSet("boat_model", None),SlotSet("year_of_manufacturing", None),SlotSet("consumable", None)
                        ,SlotSet("process", None),SlotSet("material", None)]
            
            except:

                dispatcher.utter_message(text="""Hey Really sorry but I couldn't find a Perfect Solution for
                    your query. But you can rephrase and Try It Again :) """)

                return [SlotSet("boat_part", None),SlotSet("engine_series", None),
                        SlotSet("boat_manufacturer", None),SlotSet("engine_manufacturer", None),SlotSet("boat_length", None)
                        ,SlotSet("boat_model", None),SlotSet("year_of_manufacturing", None),SlotSet("consumable", None)
                        ,SlotSet("process", None),SlotSet("material", None)]

    
