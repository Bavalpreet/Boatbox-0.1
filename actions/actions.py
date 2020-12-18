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

from spellcheck import correction
from sef import entity_finder,slot_setter
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
    
    # sols_temp --> Dataframe, checker_index ---> index, embeddings ---> embeddings of questions, 
    # user_emb_msg--> embeddings of user input
    def Answer_finder(self,sols_temp,checker_index,embeddings,user_msg_emb):
        sols_temp.reset_index(level=0, inplace=True) # setting indexes again to normal
        sols_temp.drop(columns=['index'],inplace=True) # dropping that unnecessary index column

        emb= [embeddings[i] for i in checker_index] # stroing list of only those embeddings of questions 
        # whose corresponding answer had the entity

        cos_sim = util.pytorch_cos_sim(user_msg_emb, emb) #  cosine similarity
            
        cos_sim=cos_sim.tolist()
        print(cos_sim)
        
        sol_index=cos_sim[0].index(max(cos_sim[0])) # to get the index of maximum cosine similarity
        print(sol_index)
        solution=sols_temp.iloc[[sol_index]]['solutions'][sol_index]

        return solution
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]: 


            model,embeddings,solutions = ActionGreet.loader(self)

            message=tracker.latest_message['text']
           
            print(message)
            user_msg_emb=model.encode(message)
            
            #name of entities we have to update when increse entities
            name_entities = ['boat_part', 'engine_series', 'boat_manufacturer', 'engine_manufacturer', 'boat_length', 'boat_model', 'year_of_manufacturing', 'consumable', 'process', 'material']
            total_info = entity_finder(tracker,name_entities)    
     
            # Now after getting all diffrent types of slots No we have added them to boat_part_slot variable 
            # and then will make pattern to see any of these are available in our answers file
            
            print(total_info)
            sols_temp=pd.DataFrame(solutions) # converting our series to datatframe
             
            sols_temp.rename(columns = {0:'solutions'},  inplace = True)  # renaming the column
           
            try: # to handle any kind of exceptions in code
                if len(total_info)!=0 : # if an entity is extracted from user intent

                    total_info=[correction(i) for i in total_info]
                    print("New total info is ",total_info)
                    # to search all the strings in a list wthether in column or not                                     
                    # https://stackoverflow.com/questions/17972938/check-if-a-string-in-a-pandas-dataframe-column-is-in-a-list-of-strings
                    pattern = '|'.join(total_info)

                    checker= sols_temp[sols_temp['solutions'].str.contains(pattern,na=False)]  # checking if the extracted entity
                    # is present or not and if yes in which answers
                    
                    checker_index=list(checker.index.values) # storing the indexes of rows that were having our entity

                    sols_temp=sols_temp.iloc[checker_index] # now storing only those solutions that are shortlisted

                    if len(sols_temp) !=0: # if some sol is found after entity matching.

                        solution=self.Answer_finder(sols_temp,checker_index,embeddings,user_msg_emb)
                       
                        dispatcher.utter_message(text=solution)

                        return slot_setter(name_entities)
                    else:
                        dispatcher.utter_message(text="Sorry could not find perfect solution pls try again")
                        return slot_setter(name_entities)
                else:
                    dispatcher.utter_message(text="""Hey Really sorry but I couldn't find a Perfect Solution in my dictionary
                     for your query. But you can rephrase and Try It Again :) """)

                    return slot_setter(name_entities)
                       
            except:

                dispatcher.utter_message(text="""Hey Really sorry but I couldn't find a Perfect Solution for
                    your query. But you can rephrase and Try It Again :) """)
                return slot_setter(name_entities)