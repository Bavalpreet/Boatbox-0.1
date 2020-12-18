from rasa_sdk.events import SlotSet

def entity_finder(tracker,name_entities):
    boat_part, engine_series, boat_manufacturer, engine_manufacturer, boat_length, boat_model, year_of_manufacturing, consumable, process, material = name_entities
    #boat_part
    boat_part_slot = tracker.get_slot(str(boat_part)) # this is a list slot so we will store all entities 
                                            # extracted from an intent but if no entity is extracted
                                            # tracker returns None Type value
    
    boat_part_slot=( [] if boat_part_slot is None else boat_part_slot) # to convert None type to empty list
    boat_part_slot = [i.lower() for i in boat_part_slot if len(boat_part_slot) >= 1]# converting the UPPER case entity to lowercase

    # print(boat_part_slot,tracker.slots)

    # engine_series
    engine_series_slot=tracker.get_slot(str(engine_series))

    engine_series_slot= ( [] if engine_series_slot is None else engine_series_slot) # to convert None type to empty list
    engine_series_slot = [i.lower() for i in engine_series_slot if len(engine_series_slot) >= 1]
    
    # boat_manufacturer

    boat_manufacturer_slot=tracker.get_slot(str(boat_manufacturer))

    boat_manufacturer_slot= ( [] if boat_manufacturer_slot is None else boat_manufacturer_slot)
    boat_manufacturer_slot = [i.lower() for i in boat_manufacturer_slot if len(boat_manufacturer_slot) >= 1]

    # engine_manufacturer
    engine_manufacturer_slot=tracker.get_slot(str(engine_manufacturer))

    engine_manufacturer_slot= ( [] if engine_manufacturer_slot is None else engine_manufacturer_slot)
    engine_manufacturer_slot = [i.lower() for i in engine_manufacturer_slot if len(engine_manufacturer_slot) >= 1]

    # boat_length
    boat_length_slot=tracker.get_slot(str(boat_length))

    boat_length_slot= ( [] if boat_length_slot is None else boat_length_slot)
    boat_length_slot = [i.lower() for i in boat_length_slot if len(boat_length_slot) >= 1]

    # boat_model_slot

    boat_model_slot=tracker.get_slot(str(boat_model))

    boat_model_slot= ( [] if boat_model_slot is None else boat_model_slot)
    boat_model_slot = [i.lower() for i in boat_model_slot if len(boat_model_slot) >= 1]

    # year_of_manufacturing_slot

    year_of_manufacturing_slot=tracker.get_slot(str(year_of_manufacturing))

    year_of_manufacturing_slot= ( [] if year_of_manufacturing_slot is None else year_of_manufacturing_slot)
    year_of_manufacturing_slot = [i.lower() for i in year_of_manufacturing_slot if len(year_of_manufacturing_slot) >= 1]

    # consumable

    consumable_slot=tracker.get_slot(str(consumable))

    consumable_slot= ( [] if consumable_slot is None else consumable_slot)
    consumable_slot = [i.lower() for i in consumable_slot if len(consumable_slot) >= 1]

    # process

    process_slot=tracker.get_slot(str(process))

    process_slot= ( [] if process_slot is None else process_slot)
    process_slot = [i.lower() for i in process_slot if len(process_slot) >= 1]

    # material

    material_slot=tracker.get_slot(str(material))

    material_slot= ( [] if material_slot is None else material_slot)
    material_slot = [i.lower() for i in material_slot if len(material_slot) >= 1]




    total_info=boat_part_slot+engine_series_slot+boat_manufacturer_slot+engine_manufacturer_slot+boat_length_slot+boat_model_slot+year_of_manufacturing_slot+consumable_slot+process_slot+material_slot
    
    return total_info



def slot_setter(name_entities):
    boat_part, engine_series, boat_manufacturer, engine_manufacturer, boat_length, boat_model, year_of_manufacturing, consumable, process, material = name_entities

    ss = [SlotSet(str(boat_part), None),SlotSet(str(engine_series), None),
                        SlotSet(str(boat_manufacturer), None),SlotSet(str(engine_manufacturer), None),SlotSet(str(boat_length), None)
                        ,SlotSet(str(boat_model), None),SlotSet(str(year_of_manufacturing), None),SlotSet(str(consumable), None)
                        ,SlotSet(str(process), None),SlotSet(str(material), None)]

    return ss