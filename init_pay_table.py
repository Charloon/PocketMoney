import pandas as pd
import copy
from SendGetDataFrameS3 import *

# This script is to generate teh dataframe with the list of tasks and cost, and store it in the S3.
# define data
tasks = ["Dress the table", "Clean the table", "Fill/empty dishwasher", "Take out the trash", "Put clothes to wash", \
    "Put clothes to dry", "Water the plants", "Help for non-routine task", "Finish a real book", "Clean the car", "Talk badly", \
    "Leave clothes on the floor", "Bad behavior in school", "Did not brush teeth", "Resist bathing", "Interrupt talking adults", \
    "Bad behavior at the table", "Scream for nothing", "Resist going to bed", "Fighting with sibling", "talk badly"]
df = pd.DataFrame(columns=["task", "count", "cost (eur)"], index=range(len(tasks)))
df["task"] = tasks
df["count"] = [0]*len(df["task"].values)
df["cost (eur)"] = [0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1, 3, 5, -1, -0.5, -1, -0.5, -0.5, -0.2, -0.5, -0.2, -0.5, -0.5, -0.2]

df1 = copy.deepcopy(df) # dataframe for kid 1
df2 = copy.deepcopy(df) # dataframe for kid 2
df0 = copy.deepcopy(df) # dataframe for reset

# send dataframe
sendDataframeToS3(df1, "df1.csv", "s3")
sendDataframeToS3(df2, "df2.csv", "s3")
sendDataframeToS3(df0, "df0.csv", "s3")