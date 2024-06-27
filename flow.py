#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
flow.py
Program to create an LP file of constraints to balance loads equally across links
    - Each load must be split over exactly 2 paths
    
Note: This program only runs on Linux systems with CPLEX - check directories in CPLEX function
"""
# Author: Blake Manson
# Date Created: 02/05/2024
# Date Modified: 29/05/2024

import time
import subprocess


def createLPFileName() -> str:
    """
    Creates the name for an lp file with inputs for X, Y and Z
    Returns: 
        Inputted values for X, Y and Z
        The name for the file of form XYZ.lp
    """
    X = int(input("Number of source nodes (X): "))
    Y = int(input("Number of transit nodes (Y): "))
    Z = int(input("Number of destination nodes (Z): "))
    filename = f"{X}{Y}{Z}.lp"
    return X, Y, Z, filename

def writeContraints(X: int, Y: int, Z: int, filename: str):
    """
    Writes all constraints and bounds of minimization formula to XYZ.lp
    """
    f = open(filename, 'w')
    f.write(f"Minimize\n    r\nSubject to\n")
    f.write(demandVolume(X, Y, Z))
    f.write(binaryVariable(X, Y, Z))
    f.write(demandFlow(X, Y, Z))
    f.write(sourceTransitCap(X, Y, Z))
    f.write(transitDestinationCap(X, Y, Z))
    f.write(loadBalancing(X, Y, Z))
    f.write("Bounds\n")
    f.write(bounds(X, Y, Z))
    f.write("    r >= 0\n")
    f.write("Binaries\n")
    f.write(binaries(X, Y, Z))
    f.write("End")
    f.close()
    return

def CPLEX(X: int, Y: int, Z: int, filename: str):
    """
    Runs CPLEX optimisation on the LP file
    Saves STDOUT as a file in of form XYZOut.txt
    """
    # Create output filename for CPLEX
    outputFile = f"{X}{Y}{Z}CPLEX.txt"
    
    # Paths for CPLEX and the LP file - Change if relevant
    CPLEXPath = "/csse/users/bma206/cplex/cplex/bin/x86-64_linux/cplex"
    filePath = "/media/bma206/8C0D-21E5/COSC364/PlanningAssignment/flow-planning/"
    
    # Generate command from file paths and filename
    command = [CPLEXPath, "-c", "read " + filePath + filename, "optimize", "display solution variables -"]
    
    # Starts a timer to measure execution time
    startTime = time.time()
    
    # Run CPLEX as a subprocess and wait for finish, then stop timer
    process = subprocess.Popen(command, stdout=open(outputFile, "wb"))
    process.wait()
    endTime = time.time()
    
    # Calculate and print execution time to 3dp
    timeTaken = endTime - startTime
    print(f"CPLEX Execution Time: {timeTaken:.3f}s")
    
    return

def demandVolume(X: int, Y: int, Z: int) -> str:
    """Returns demand volume constraints"""
    output = ""
    for i in range(1, X+1):
        for j in range(1, Z+1):
            output += "    "
            for k in range(1, Y+1):
                if k != (Y):
                    output += f"x{i}{k}{j} + "
                else:
                    output += f"x{i}{k}{j} = {i+j}\n"
    return output

def binaryVariable(X: int, Y: int, Z: int) -> str:
    """Returns binary variable constraints"""
    output = ""
    for i in range(1, X+1):
        for j in range(1, Z+1):
            output += "    "
            for k in range(1, Y+1):
                if k != (Y):
                    output += f"u{i}{k}{j} + "
                else:
                    output += f"u{i}{k}{j} = 2\n"
    return output

def demandFlow(X: int, Y: int, Z: int) -> str:
    """Returns demand flow constraints"""
    output = ""
    for i in range(1, X+1):
        for j in range(1, Z+1):
            for k in range(1, Y+1):
                output += f"    2 x{i}{k}{j} - {i+j} u{i}{k}{j} = 0\n"
    return output

def sourceTransitCap(X: int, Y: int, Z: int) -> str:
    """Returns source-transit capacity constraints"""
    output = ""
    for i in range (1, X+1):
        for k in range (1, Y+1):
            output += "    "
            for j in range(1, Z+1):
                if j != (Z):
                    output += f"x{i}{k}{j} + "
                else:
                    output += f"x{i}{k}{j} - c{i}{k} <= 0\n"
    return output
    
def transitDestinationCap(X: int, Y: int, Z: int) -> str:
    """Returns transit-destination capacity constraints"""
    output = ""
    for k in range(1, Y+1):
        for j in range(1, Z+1):
            output += "    "
            for i in range(1, X+1):
                if i != (X):
                    output += f"x{i}{k}{j} + "
                else:
                    output += f"x{i}{k}{j} - d{k}{j} <= 0\n"
    return output

def loadBalancing(X: int, Y: int, Z: int) -> str:
    """Returns load balancing constraints"""
    output = ""
    for k in range(1, Y+1):
        output += "    "
        for j in range(1, Z+1):
            for i in range(1, X+1):
                if i != (X) or j != (Z):
                    output += f"x{i}{k}{j} + "
                else:
                    output += f"x{i}{k}{j} - r <= 0\n"
    return output

def bounds(X: int, Y: int, Z: int) -> str:
    """Returns the bounds of x, c and d"""
    output = ""
    for i in range(1, X+1):
        for k in range(1, Y+1):
            for j in range(1, Z+1):
                output += f"    x{i}{k}{j} >= 0\n"   
    for i in range(1, X+1):
        for k in range(1, Y+1):
            output += f"    c{i}{k} >= 0\n"
    for k in range(1, Y+1):
        for j in range(1, Z+1):
            output += f"    d{k}{j} >= 0\n"
    return output

def binaries(X: int, Y: int, Z: int) -> str:
    """Returns binary constraints"""
    output = ""
    for i in range(1, X+1):
        for k in range(1, Y+1):
            for j in range(1, Z+1):
                output += f"    u{i}{k}{j}\n"
    return output

def main():
    """
    Main function: Creates file with inputted X, Y, and Z
    Writes constraints formula to XYZ.lp
    Runs CPLEX optimization on file and saves to XYZCPLEX.txt
    """
    X, Y, Z, filename = createLPFileName()
    writeContraints(X, Y, Z, filename)
    CPLEX(X, Y, Z, filename)
    
if (__name__ == "__main__"):
    main()
