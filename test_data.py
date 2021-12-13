from graphs_functions import *

"""
===================================================================================================

DATAFRAMES

===================================================================================================
"""


a2q = pd.read_csv("data/a2q.csv", parse_dates=["time"], infer_datetime_format=True)
c2q = pd.read_csv("data/c2q.csv", parse_dates=["time"], infer_datetime_format=True)
c2a = pd.read_csv("data/c2a.csv", parse_dates=["time"], infer_datetime_format=True)

#Answers to questions
a2q["weights"] = 1

#Comments to answers
c2a["weights"] = 0.4

#Comments to questions
c2q["weights"] = 0.7

totDataframe = pd.concat([a2q, c2a, c2q])

totDataframe_2y = totDataframe[totDataframe.time.between("2015","2017")]
a2q_2y = a2q[a2q.time.between("2015","2017")]
c2q_2y = c2q[c2q.time.between("2015","2017")]
c2a_2y = c2a[c2a.time.between("2015","2017")]



"""
===================================================================================================

GRAPHS

===================================================================================================
"""

test_g = make_graph(totDataframe_2y[totDataframe_2y.time.between("2015-01-01","2015-01-01")].iloc[:1000])


t = GRAPH()
t.add_edge(from_n=1,to_n=2, time="438", w=57)
t.add_edge(from_n=1,to_n=3, time="438", w=12)
t.add_edge(from_n=3,to_n=2, time="438", w=2)
t.add_edge(from_n=2,to_n=4, time="438", w=24)
t.add_edge(from_n=2,to_n=6, time="438", w=45)
t.add_edge(from_n=3,to_n=5, time="438", w=6)
t.add_edge(from_n=5,to_n=4, time="438", w=31)


t2 = GRAPH()
t2.add_edge(from_n=1,to_n=3, time="438", w=2)
t2.add_edge(from_n=1,to_n=2, time="438", w=4)
t2.add_edge(from_n=3,to_n=4, time="438", w=1)
t2.add_edge(from_n=4,to_n=2, time="438", w=6)
t2.add_edge(from_n=2,to_n=5, time="438", w=1)
t2.add_edge(from_n=4,to_n=5, time="438", w=5)


t3 = GRAPH()
t3.add_edge(from_n=1,to_n=2, time="438", w=1)
t3.add_edge(from_n=1,to_n=3, time="438", w=1)
t3.add_edge(from_n=3,to_n=4, time="438", w=1)
t3.add_edge(from_n=2,to_n=4, time="438", w=1)
t3.add_edge(from_n=4,to_n=5, time="438", w=1)
t3.add_edge(from_n=1,to_n=6, time="438", w=1)
t3.add_edge(from_n=6,to_n=4, time="438", w=1)
t3.add_edge(from_n=4,to_n=7, time="438", w=1)
t3.add_edge(from_n=7,to_n=9, time="438", w=1)
t3.add_edge(from_n=8,to_n=9, time="438", w=1)
t3.add_edge(from_n=4,to_n=8, time="438", w=1)