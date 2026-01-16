import os
import argparse
from glob import glob
import shutil
from tqdm import tqdm

def my_queue():
    os.system("squeue --format=\"%.18i %.9p %.30j %.10u %.8T %.10M %.10l %.6D %.10R %Z\" --me")

def copy_file_pattern(file_pattern,directory_location):
    if not os.path.exists(directory_location):
        print(f"making directory {directory_location}")
        os.mkdir(directory_location)
    for file in tqdm(glob(file_pattern),desc=f"files matching {file_pattern} coppied to {directory_location}."):
        copy_location = directory_location + file.split("/")[-1].split("\\")[-1]
        shutil.copyfile(file,copy_location)

def sort_from_folders():
    parser = argparse.ArgumentParser(prog="pysff")
    parser.add_argument("-i",action="store_true",help="Copy Gaussian/ORCA input files to ./infiles/")
    parser.add_argument("-o",action="store_true",help="Copy Gaussian/ORCA output files to ./outfiles/")
    parser.add_argument("-b",action="store_true",help="Copy batch files (*.s) to ./batchfiles/")

    args = parser.parse_args()

    if args.i:
        print("SORTING INPUT FILES")
        copy_file_pattern("*/*.inp","./infiles/")
        copy_file_pattern("*/*.gjf","./infiles/")
    
    if args.o:
        print("SORTING OUTPUT FILES")
        copy_file_pattern("*/*.log","./outfiles/")
        copy_file_pattern("*/*.out","./outfiles/")

    if args.b:
        print("SORTING OUTPUT FILES")
        copy_file_pattern("*/*.s","./batchfiles/")
