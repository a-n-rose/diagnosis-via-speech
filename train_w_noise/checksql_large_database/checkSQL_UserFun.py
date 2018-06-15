"""
Functions that allow user and program to 'communicate' for accessing SQL databases
"""

from checkSQL_db_edit import User_Input

def show_options(datacont_instance):
    data_cont = datacont_instance.datacont_type
    data_list = datacont_instance.item_list
    print("\nAvailable {}:".format(data_cont))
    for item in range(len(data_list)):
        print("{}) ".format(item+1), data_list[item])
    print("\nWhich {} would you like to explore?".format(data_cont))
    return None

def getDataCont_Name(input_instance,datacont_instance):
    ii = input_instance
    di = datacont_instance
    data_cont = di.datacont_type
    while ii.stop == False:
        ii.text = input('Please enter the number corresponding to the {}: '.format(data_cont))
        datacont_name, ii.stop = ii.str2index(di.item_list)
    return(datacont_name)
    
def stop_OR_go(data_container):
    cont_input = User_Input()
    while cont_input.stop == False:
        cont_input.text = input("\nWould you like to explore data from additional {}? (yes or no): ".format(data_container))
        if 'yes' or 'no' in cont_input.text.lower():
            cont_input.stop = True
            return(cont_input.text)
        else:
            print("\nPlease enter 'yes' or 'no'\n")
    return None  

def no_items(data_container1, data_container2):
    print("\n!! No %s found in %s !!\n" % (data_container1,data_container2))
    return None
 
