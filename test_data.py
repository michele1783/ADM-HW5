from graphs_functions import *

"""
===================================================================================================

DATAFRAMES

===================================================================================================
"""

print("Starting to read the csv files...")

a2q = pd.read_csv("data/a2q.csv", parse_dates=["time"], infer_datetime_format=True)
print("        a2q read")

c2q = pd.read_csv("data/c2q.csv", parse_dates=["time"], infer_datetime_format=True)
print("        c2q read")

c2a = pd.read_csv("data/c2a.csv", parse_dates=["time"], infer_datetime_format=True)
print("        c2a read")


#Answers to questions
a2q["weights"] = 0.4

#Comments to answers
c2a["weights"] = 1

#Comments to questions
c2q["weights"] = 0.7

totDataframe = pd.concat([a2q, c2a, c2q])

totDataframe_2y = totDataframe[totDataframe.time.between("2008-08-01", "2008-09-01")]
a2q_2y = a2q[a2q.time.between("2008-08-01", "2008-09-01")]
c2q_2y = c2q[c2q.time.between("2008-08-01", "2008-09-01")]
c2a_2y = c2a[c2a.time.between("2008-08-01", "2008-09-01")]

print("Starting to create the graphs...")

a2q_2y_g = make_graph(a2q_2y)
print("        a2q graph created")

#c2q_2y_g = make_graph(c2q_2y)
print("        c2q graph created")

#c2a_2y_g = make_graph(c2a_2y)
print("        c2a graph created")

totDataframe_2y_g = make_graph(totDataframe_2y)
print("        totDataframe graph created")



"""
===================================================================================================

GRAPHS

===================================================================================================
"""


t = GRAPH()

n1 = NODE(1)
n2 = NODE(2)
n3 = NODE(3)
n4 = NODE(4)
n5 = NODE(5)
n6 = NODE(6)

t.add_edge(from_n=n1,to_n=n2, time="438", w=57)
t.add_edge(from_n=n1,to_n=n3, time="438", w=12)
t.add_edge(from_n=n3,to_n=n2, time="438", w=2)
t.add_edge(from_n=n2,to_n=n4, time="438", w=24)
t.add_edge(from_n=n2,to_n=n6, time="438", w=45)
t.add_edge(from_n=n3,to_n=n5, time="438", w=6)
t.add_edge(from_n=n5,to_n=n4, time="438", w=31)


t2 = GRAPH()

n1 = NODE(1)
n2 = NODE(2)
n3 = NODE(3)
n4 = NODE(4)
n5 = NODE(5)

t2.add_edge(from_n=n1,to_n=n3, time="438", w=2)
t2.add_edge(from_n=n1,to_n=n2, time="438", w=4)
t2.add_edge(from_n=n3,to_n=n4, time="438", w=1)
t2.add_edge(from_n=n4,to_n=n2, time="438", w=6)
t2.add_edge(from_n=n2,to_n=n5, time="438", w=1)
t2.add_edge(from_n=n4,to_n=n5, time="438", w=5)


t3 = GRAPH()

n1 = NODE(1)
n2 = NODE(2)
n3 = NODE(3)
n4 = NODE(4)
n5 = NODE(5)
n6 = NODE(6)
n7 = NODE(7)
n8 = NODE(8)
n9 = NODE(9)

t3.add_edge(from_n=n1,to_n=n2, time="438", w=1)
t3.add_edge(from_n=n1,to_n=n3, time="438", w=1)
t3.add_edge(from_n=n3,to_n=n4, time="438", w=1)
t3.add_edge(from_n=n2,to_n=n4, time="438", w=1)
t3.add_edge(from_n=n4,to_n=n5, time="438", w=1)
t3.add_edge(from_n=n1,to_n=n6, time="438", w=1)
t3.add_edge(from_n=n6,to_n=n4, time="438", w=1)
t3.add_edge(from_n=n4,to_n=n7, time="438", w=1)
t3.add_edge(from_n=n7,to_n=n9, time="438", w=1)
t3.add_edge(from_n=n8,to_n=n9, time="438", w=1)
t3.add_edge(from_n=n4,to_n=n8, time="438", w=1)