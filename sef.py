from rasa_sdk.events import SlotSet

def entity_finder(tracker,name_entities):
    BOAT_PART, ENGINE_SERIES, BOAT_MANUFACTURER, ENGINE_MANUFACTURER, BOAT_LENGTH, BOAT_MODEL, YEAR_OF_MANUFACTURING, CONSUMABLE, PROCESS, MATERIAL = name_entities
    #BOAT_PART
    BOAT_PART_slot = tracker.get_slot(str(BOAT_PART)) # this is a list slot so we will store all entities 
                                            # extracted from an intent but if no entity is extracted
                                            # tracker returns None Type value
    
    BOAT_PART_slot=( [] if BOAT_PART_slot is None else BOAT_PART_slot) # to convert None type to empty list
    BOAT_PART_slot = [i.lower() for i in BOAT_PART_slot if len(BOAT_PART_slot) >= 1]# converting the UPPER case entity to lowercase

    # print(BOAT_PART_slot,tracker.slots)

    # ENGINE_SERIES
    ENGINE_SERIES_slot=tracker.get_slot(str(ENGINE_SERIES))

    ENGINE_SERIES_slot= ( [] if ENGINE_SERIES_slot is None else ENGINE_SERIES_slot) # to convert None type to empty list
    ENGINE_SERIES_slot = [i.lower() for i in ENGINE_SERIES_slot if len(ENGINE_SERIES_slot) >= 1]
    
    # BOAT_MANUFACTURER

    BOAT_MANUFACTURER_slot=tracker.get_slot(str(BOAT_MANUFACTURER))

    BOAT_MANUFACTURER_slot= ( [] if BOAT_MANUFACTURER_slot is None else BOAT_MANUFACTURER_slot)
    BOAT_MANUFACTURER_slot = [i.lower() for i in BOAT_MANUFACTURER_slot if len(BOAT_MANUFACTURER_slot) >= 1]

    # ENGINE_MANUFACTURER
    ENGINE_MANUFACTURER_slot=tracker.get_slot(str(ENGINE_MANUFACTURER))

    ENGINE_MANUFACTURER_slot= ( [] if ENGINE_MANUFACTURER_slot is None else ENGINE_MANUFACTURER_slot)
    ENGINE_MANUFACTURER_slot = [i.lower() for i in ENGINE_MANUFACTURER_slot if len(ENGINE_MANUFACTURER_slot) >= 1]

    # BOAT_LENGTH
    BOAT_LENGTH_slot=tracker.get_slot(str(BOAT_LENGTH))

    BOAT_LENGTH_slot= ( [] if BOAT_LENGTH_slot is None else BOAT_LENGTH_slot)
    BOAT_LENGTH_slot = [i.lower() for i in BOAT_LENGTH_slot if len(BOAT_LENGTH_slot) >= 1]

    # BOAT_MODEL_slot

    BOAT_MODEL_slot=tracker.get_slot(str(BOAT_MODEL))

    BOAT_MODEL_slot= ( [] if BOAT_MODEL_slot is None else BOAT_MODEL_slot)
    BOAT_MODEL_slot = [i.lower() for i in BOAT_MODEL_slot if len(BOAT_MODEL_slot) >= 1]

    # YEAR_OF_MANUFACTURING_slot

    YEAR_OF_MANUFACTURING_slot=tracker.get_slot(str(YEAR_OF_MANUFACTURING))

    YEAR_OF_MANUFACTURING_slot= ( [] if YEAR_OF_MANUFACTURING_slot is None else YEAR_OF_MANUFACTURING_slot)
    YEAR_OF_MANUFACTURING_slot = [i.lower() for i in YEAR_OF_MANUFACTURING_slot if len(YEAR_OF_MANUFACTURING_slot) >= 1]

    # CONSUMABLE

    CONSUMABLE_slot=tracker.get_slot(str(CONSUMABLE))

    CONSUMABLE_slot= ( [] if CONSUMABLE_slot is None else CONSUMABLE_slot)
    CONSUMABLE_slot = [i.lower() for i in CONSUMABLE_slot if len(CONSUMABLE_slot) >= 1]

    # PROCESS

    PROCESS_slot=tracker.get_slot(str(PROCESS))

    PROCESS_slot= ( [] if PROCESS_slot is None else PROCESS_slot)
    PROCESS_slot = [i.lower() for i in PROCESS_slot if len(PROCESS_slot) >= 1]

    # MATERIAL

    MATERIAL_slot=tracker.get_slot(str(MATERIAL))

    MATERIAL_slot= ( [] if MATERIAL_slot is None else MATERIAL_slot)
    MATERIAL_slot = [i.lower() for i in MATERIAL_slot if len(MATERIAL_slot) >= 1]




    total_info=BOAT_PART_slot+ENGINE_SERIES_slot+BOAT_MANUFACTURER_slot+ENGINE_MANUFACTURER_slot+BOAT_LENGTH_slot+BOAT_MODEL_slot+YEAR_OF_MANUFACTURING_slot+CONSUMABLE_slot+PROCESS_slot+MATERIAL_slot
    
    return total_info



def slot_setter(name_entities):
    BOAT_PART, ENGINE_SERIES, BOAT_MANUFACTURER, ENGINE_MANUFACTURER, BOAT_LENGTH, BOAT_MODEL, YEAR_OF_MANUFACTURING, CONSUMABLE, PROCESS, MATERIAL = name_entities

    ss = [SlotSet(str(BOAT_PART), None),SlotSet(str(ENGINE_SERIES), None),
                        SlotSet(str(BOAT_MANUFACTURER), None),SlotSet(str(ENGINE_MANUFACTURER), None),SlotSet(str(BOAT_LENGTH), None)
                        ,SlotSet(str(BOAT_MODEL), None),SlotSet(str(YEAR_OF_MANUFACTURING), None),SlotSet(str(CONSUMABLE), None)
                        ,SlotSet(str(PROCESS), None),SlotSet(str(MATERIAL), None)]

    return ss