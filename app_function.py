from general_functions import *
from graphs_functions import *
from functionality_1 import *
from functionality_2 import *
from functionality_3 import *
from test_data import *



def app(data1, data2, data3, dataTOT):
    end = 0
    while (end == 0):

        #choose what functionality
        user = int(input("Welcome user, what functionality do you want: "))

        if (user == 1):

            #choose what file
            scelta = input("What file do you want to analyze?: ")
            if scelta == "a2q":

                number_nodes_1, number_edges_1, directed_1, mean_1, density_1, sparse_1, degree_1, table_1 = functionality_1(data1)
                print(tabulate(table_1, headers='firstrow', tablefmt='fancy_grid'))
                print("We want to visualize how many users have a certain degree")
                fun_1.fig(degree_1)
                print("We want to go deeper in the density distribution")
                fun_1.fig_hist(degree_1)
                print("We want to visualize for each user how many degree it has")
                fun_1.fig_plot(degree_1)

            elif scelta == "c2a":

                number_nodes_2, number_edges_2, directed_2, mean_2, density_2, sparse_2, degree_2, table_2 = functionality_1(data2)
                print(tabulate(table_2, headers='firstrow', tablefmt='fancy_grid'))
                print("We want to visualize how many users have a certain degree")
                fig(degree_2)
                print("We want to go deeper in the density distribution")
                fig_hist(degree_2)
                print("We want to visualize for each user how many degree it has")
                fig_plot(degree_2)


            else:

                number_nodes_3, number_edges_3, directed_3, mean_3, density_3, sparse_3, degree_3, table_3 = functionality_1(data3)
                print(tabulate(table_3, headers='firstrow', tablefmt='fancy_grid'))
                print("We want to visualize how many users have a certain degree")
                fig(degree_3)
                print("We want to go deeper in the density distribution")
                fig_hist(degree_3)
                print("We want to visualize for each user how many degree it has")
                fig_plot(degree_3)

            end = 1



        if (user == 2):

            print("result of func_2")
            print("Functionality 2 - Find the best users!")
            end = 1

        if (user == 3):
            print("Functionality 3 - Shortest Ordered Route")
            print("result of func_3")
            end = 1