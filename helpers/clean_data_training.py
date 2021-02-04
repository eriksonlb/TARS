import shutil
import os
path ="data/training"
folder = shutil.rmtree(path)
os.mkdir(path)