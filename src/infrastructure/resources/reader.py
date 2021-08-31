import pickle
from .paths import *

# read model from pickle file
processor = pickle.load(open(path_processor_pkl, "rb"))