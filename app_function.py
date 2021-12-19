from general_functions import *
from graphs_functions import *
from functionality_1 import *
from functionality_2 import *
from functionality_3 import *
from test_data import *



def app():
    end = 0
    while (end == 0):

        #choose what functionality
        user = int(input("Welcome user, what functionality do you want: "))

        if (user == 1):

            funz_1()

            end = 1



        if (user == 2):
            
            functionality_2_visual()
            
            print("End of functionality 2")
            
            end = 1

        if (user == 3):
            print("Functionality 3 - Shortest Ordered Route")
            
            out_g, _, lenght = func_3()
            
            out_g.print_graph(pos="planar")
            
            print("result of func_3")
            end = 1