import pandas as pd
import numpy as np
from datetime import *
import networkx as nx
import networkx.drawing
from collections import *
from tqdm.notebook import tqdm
from multiprocessing.dummy import Pool
import multiprocessing
import matplotlib.pyplot as plt
import pickle

def dateparse(time_as_a_unix_timestamp):
    return pd.to_datetime(time_as_a_unix_timestamp, unit="s").strftime("%Y-%m-%d %H")

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        
def read_object(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data
    
    
def make_dataframes():
    #Answers to questions
    a2q = pd.read_csv("data/sx-stackoverflow-a2q.txt", sep=" " ,header=None, names=["user_a", "user_b", "time"], parse_dates=["time"], date_parser=dateparse)
    
    print("a2q dataframe created!")
    
    #Comments to answers
    c2a = pd.read_csv("data/sx-stackoverflow-c2a.txt", sep=" " ,header=None, names=["user_a", "user_b", "time"], parse_dates=["time"], date_parser=dateparse)
    
    print("c2a dataframe created!")
    
    #Comments to questions
    c2q = pd.read_csv("data/sx-stackoverflow-c2q.txt", sep=" " ,header=None, names=["user_a", "user_b", "time"], parse_dates=["time"], date_parser=dateparse)
    
    print("c2q dataframe created!")
    
    print("start writing into files...")
    a2q.to_csv("data/a2q.csv", index=False)
    c2q.to_csv("data/c2q.csv", index=False)
    c2a.to_csv("data/c2a.csv", index=False)
    
    print("writing into files completed")