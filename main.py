#Implemented in Python Programming Language
#Main Function for running the code for Project 2
#Solves increasingly complex Tower of Hanoi problems using the A* Final Algorithm and then Recursive Best First Search Algorithm
#Code runs for a set number of time 
#Code outputs the results to a file
#
#Authors: Robert Perry, Swarna Chakraborty, Chris Shaner
#

#---------------------------------------------------------------------------------------------------------------------------------

#Notes from development
#Robert Perry - Created the initial main file and initial function layouts
#Robert Perry - started the outlines for the two search algorithms
#Robert Perry - Implementing the Data logging and output files for the algorithms
#Robert Perry - Implementing the skeleton for the GUI
#Robert Perry - Created the GUI


#Swarna Chakraborty - Created and implemented the initial Recursive Best First Search Algorithm
#Swarna Chakraborty - Merged  A* and RBFS to the main
#Swarna Chakraborty - Worked on bug fix for both algorithms
#Chris Shaner - Created and implemented  A* Final Algorithm
#Shris Shaner - Worked on bug fix for both algorithms

#---------------------------------------------------------------------------------------------------------------------------------

#Imports

#---------------------------------------------------------------------------------------------------------------------------------

#Import the necessary libraries
import time
import sys
import os
import psutil
from tkinter import *
import time
import heapq # provides an implementation fo the heap queue algorithm (priority queue algorithm)
from tabulate import tabulate
import SwarnaHeuristic as hueristic #import the team member Hueuristic Function
import A_Star_Final_Algorithm
from datetime import datetime
import RBFS_Algorithm

try:
    import matplotlib.pyplot as plt
    import matplotlib.figure as fig
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    print("Matplotlib is not installed. Please install matplotlib to run the code. \n pip install matplotlib") 
    sys.exit()

try:
    import numpy as np
except ImportError:
    print("Numpy is not installed. Please install numpy to run the code. \n pip install numpy") 
    sys.exit()

#Import the team member Hueuristic Function
cwd = os.getcwd()
sys.path.append(cwd)
# No changes needed, removing the import statement since it is not being used
#---------------------------------------------------------------------------------------------------------------------------------

#Classes

#---------------------------------------------------------------------------------------------------------------------------------        
class GUI:

        #initialize the class
        def __init__(self):
            #set the algorithm
            self.algorithm = ""
            #set the time to run the algorithm
            self.runtime = 0
            #set the run button state
            self.runButtonState = "disabled"

        def exit(self):
            sys.exit()

        def updateAlgorithm(self, algorithm):
            self.algorithm = algorithm
        
        def updateRuntime(self, runtime):
            self.runtime = runtime
        
        def updateRunButtonState(self, runButtonState):
            self.runButtonState = runButtonState
            
        #read config file and update the variables
        def readConfig(self):
            config = open("config.txt", "r")
            configlines = config.readlines()
            config.close()

            #stip the newline character from the end of the line
            count = 0
            for line in configlines:
                count += 1
                line = "Line{}: {}".format(count, line.strip())

            #get the time to run the algorithm
            self.runtime = configlines[0]

            #remove the text before = and the = sign
            self.runtime = self.runtime[self.runtime.find("=")+1:]
            #convert the time to an integer
            try:
                self.runtime = float(self.runtime)
            except ValueError:
                self.runtime = "Invalid runtime"

            if self.runtime < 0:
                self.runtime = "Invalid runtime"
            
            #get the algorithm to run
            self.algorithm = configlines[1]
            #remove the text before = and the = sign
            self.algorithm = self.algorithm[self.algorithm.find("=")+1:]

            #get the run button state
            self.runButtonState = configlines[2]
            #remove the text before = and the = sign
            self.runButtonState = self.runButtonState[self.runButtonState.find("=")+1:]

            return self.runtime, self.algorithm
        
        #write to config file
        def writeConfig(self, request, value):
            #open a config file to read and write the program settings

            #overwrite the time to run the algorithm
            if request == "runtime":
                self.runtime = value
                self.updateRuntime(value)
        
            if request == "algorithm":
                self.algorithm = value
                self.updateAlgorithm(value)

            if request == "runButtonState":
                self.runButtonState = value
                self.updateRunButtonState(value)

            #rewrite the config file with new values
            config = open("config.txt", "w")
            config.write("runtime =" + str(self.runtime) + "\n" + "algorithm =" + str(self.algorithm) + "\n" + "runButtonState =" + str(self.runButtonState) + "\n")

            print("The config file has been updated with the following values: \n" + "runtime =" + str(self.runtime) + "\n" + "algorithm =" + str(self.algorithm) + "\n" + "runButtonState =" + str(self.runButtonState) + "\n")

            #save and close the config file
            config.close()
            
        def settings(self, root):
            
            #function to submit the new time to run the algorithm
            def submitTime():
                #get the value from the entry box
                entryvalue = entry.get()
                #convert the value to a float
                try:
                    entryvalue = float(entryvalue)
                except ValueError:
                    entryvalue = "Invalid runtime"
                    label1.config(text = "Invalid runtime. Please input a valid runtime in seconds: \n", fg = "red", font = "Times 12 bold underline")
                    entry.delete(0, END)
                    entry.insert(0, self.runtime)

                if entryvalue < 0:
                    entryvalue = "Invalid runtime"
                    label1.config(text = "Invalid runtime. Please input a valid runtime in seconds: \n", fg = "red", font = "Times 12 bold underline")
                    entry.delete(0, END)
                    entry.insert(0, self.runtime)

                #write the new time to the config file
                if entryvalue != "Invalid runtime":
                    self.writeConfig("runtime", entryvalue)
                    timeframe.destroy()
                    self.rootmenu()

            #destroy the root window
            root.destroy()

            #create a prompt the user for the amount of time to run the algorithm using the GUI
            timeframe = Tk()
            timeframe.geometry("640x400")
            frame = Frame(timeframe)
            frame.pack()
            label1 = Label(frame, text = "\n 1800 seconds = 30 min \n \n")
            label1.pack()
            label2 = Label(frame, text = "Please input the amount of time to run the algorithm in seconds: \n", fg = "red", font = "Times 12 bold underline")
            label2.pack()

            #create a text box for the user to input the amount of time to run the algorithm
            entry = Entry(frame)
            entry.insert(0, self.runtime)
            entry.pack()

            button1 = Checkbutton(frame, text = "A* Final Algorithm", fg = "black", activebackground = "blue", command = lambda: self.writeConfig("algorithm", "A* Final Algorithm"))
            button1.pack(padx = 1, pady = 15)
            button2 = Checkbutton(frame, text = "Recursive Best First Search Algorithm", fg = "black", activebackground="blue", command=lambda: self.writeConfig("algorithm", "Recursive Best First Search Algorithm"))
            button2.pack(padx = 1, pady = 15)

            #create a button for the user to submit the amount of time to run the algorithm
            button = Button(frame, text = "Submit ", fg = "blue", command = lambda: submitTime())
            button.pack()
            
            timeframe.title("Tower of Hanoi AI - Settings")
            timeframe.mainloop()

        def rootmenu(self):
                
                #open a window for the user to select which algorithm to run
                root = Tk()
                root.geometry("640x480")
                root.protocol("WM_DELETE_WINDOW", self.exit)
                frame = Frame(root)
                frame.pack()

                self.runtime, self.algorithm = self.readConfig()
                
                label = Label(frame, text = "\n Tower of Hanoi AI \n \n  Advanced Artificial Intelligence November 2023 \n Robert Perry, Swarna Chakraborty, Chris Shaner \n")
                label.pack()
    
                #label for the time to run the algorithm
                label2 = Label(frame, text = "Time to run the algorithm in minutes: " + str(self.runtime))
                label2.pack()
    
                label3 = Label(frame, text = "Search Algorithm: " + self.algorithm)
                label3.pack()
    
                label4 = Label(frame, text = "Hueristic Function: " + hueristic.hueristicSummary)
                label4.pack()
                    
                label1 = Label(frame, text = "Please select which algorithm to run:", fg = "red", font = "Times 12 bold underline")
                label1.pack()
                
                button3 = Button(frame, text = "Change Settings", fg = "black", activebackground="blue", command=lambda: self.settings(root))
                button3.pack(padx = 1, pady = 15)
                button4 = Button(frame, text = "Run Algorithm", fg = "black", activebackground="blue", command=lambda: root.destroy())
                button4.pack(padx = 1, pady = 15)

                #button to exit the program
                button = Button(frame, text = "Exit", fg = "red", command = sys.exit)
    
                #run the GUI
                root.title("Tower of Hanoi AI")
                root.mainloop()

#---------------------------------------------------------------------------------------------------------------------------------

#Functions

#---------------------------------------------------------------------------------------------------------------------------------
    

#Function to get the memory used to solve for every disk
def memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_full_info()
    peak_memory = mem_info.uss # USS (Unique Set Size) 
    return peak_memory / (1024 * 1024) # Convert bytes to megabytes

#---------------------------------------------------------------------------------------------------------------------------------

#Main function

def main():

#Setup for the Algorithms start ----------------------------------------------------------------------------------------

    #create and populate the config value with default values if it does not exist
    if os.path.exists("config.txt"):
        print("The config file already exists. Reading the config file...")
    else:
        print("The config file does not exist. Creating the config file...")
        config = open("config.txt", "w")
        config.write("runtime =1800\n")
        config.write("algorithm =A* Final Algorithm\n")
        config.write("runButtonState =disabled\n")
        config.close()

    #create the GUI
    Gui = GUI()

    #run the root menu
    Gui.rootmenu()

    #read the config file
    seconds, algorithm = Gui.readConfig()

    #gets the current working directory
    cwd = os.getcwd()

    if algorithm == "A* Final Algorithm\n":
        textfile = str("output-AStar_" + (str(datetime.now())).replace(":", "-") + ".txt")
        algorithmfunction = A_Star_Final_Algorithm.A_Star_Final

    if algorithm == "Recursive Best First Search Algorithm\n":
        textfile = str("output-RBFSearch_" + str(datetime.now()).replace(":", "-") + ".txt")
        algorithmfunction = RBFS_Algorithm.rbfs_tower_of_hanoi


    #initialize the output file in the current working directory
    outputFile = open(textfile, "w")

    #initialize the number of disks
    numDisks = 8

    #get the current system time
    startTime = time.time()
    #find the time after 30 minutes ----- 1800 seconds
    ### - SET TO 5 SECONDS FOR TESTING
    endTime = startTime + seconds

#Setup for the Algorithms end ----------------------------------------------------------------------------------------

#Algorithm Start -----------------------------------------------------------------------------------------------------


    #output the data to the output file

    outputFile.write("Data Logging for " + str(algorithm))
    #outputFile.write("Number Of Disks, Path Cost, Path Hueristic, Nodes Expanded, Nodes Generated, Time Elapsed, Memory Usage\n")

    #create a list to store the data
    data = [["Number of Disks", "Nodes Generated", "Nodes Expanded", "Memory Usage", "Time Elapsed", "Total Time Elapsed"]]

    
    #Create the initial Tower of Hanoi object

    #run the code for the specified amount of time
    while time.time() < endTime:
        #track the elapsed time
        
        #run the chosen Algorithm
        start_time = time.time() # Record the start time
        start_memory = memory_usage() # Record the memory usage at start
        paths, nodesGenerated, nodesExpanded = algorithmfunction(numDisks, endTime)
        
        end_time = time.time() # Record the end time
        end_memory = memory_usage() # # Record the memory usage at the end
        execution_time = end_time - start_time # Calculate the total execution time
        memory_used = end_memory - start_memory # Calculate the total memory used
        totalTime = time.time() - startTime
        
        #print the moves wwhich led to the solution
        if paths is not None:
            for path in paths:
                print(path)

        #append the data to the data output text file
        
        outputFile.write(str(numDisks) + ", " + str(nodesExpanded) + ", " + str(nodesGenerated) + ", " + str(execution_time) + ", " + str(memory_used) + "\n")
        
        #append the data to the data list
        data.append([numDisks, nodesGenerated, nodesExpanded, memory_used, execution_time, totalTime])
        
        #print to console in real time
        print("Number of Disks: " + str(numDisks) + ", Nodes Expanded: " + str(nodesExpanded) + ", Nodes Generated: " + str(nodesGenerated) + ", Time Elapsed: " + str(execution_time) + ", Memory Usage: " + str(memory_used), ", Total Time Elapsed: " + str(totalTime))
        numDisks += 1
    #print the path of the output file

    #remove the last line of the data list
    data.pop()

    outputFile.write(tabulate(data, headers="firstrow", tablefmt="grid"))
    print("The output file is located at: " + cwd + "/" + textfile)

    #close the output file
    outputFile.close()

# Data analysis GUI ---------------------------------------------------------------------------------------------------

    #set x axis to the total amount of time elapsed
    x = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        x[i] = data[i+1][5]

    #set y1 axis to the number of disks
    y1 = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        y1[i] = data[i+1][0]

    #set y3 axis to the nodes expanded
    y3 = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        y3[i] = data[i+1][1]

    #set y4 axis to the nodes generated
    y4 = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        y4[i] = data[i+1][2]

    #set y5 axis to the time elapsed per disk
    y5 = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        y5[i] = data[i+1][5]
    
    #set y6 axis to the memory usage
    y6 = np.zeros(len(data)-1)
    for i in range(0, (len(data)-1)):
        y6[i] = data[i+1][3]
    
    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 3, figsize=(10, 8))

    # Plot data on each subplot
    axs[0, 0].plot(x, y1, color='r')
    axs[0, 0].set_title('Number of Disks')

    axs[0, 1].plot(x, y3, color='b')
    axs[0, 1].set_title('nodes expanded')

    axs[0, 2].plot(x, y4, color='purple')
    axs[0, 2].set_title('nodes generated')

    axs[1, 0].plot(x, y5, color='orange')
    axs[1, 0].set_title('time elapsed')

    axs[1, 1].plot(x, y6, color='black')
    axs[1, 1].set_title('memory usage')

    axs[1,2].axis('off')


    # Add a common title for all subplots
    fig.suptitle('Tower of Hanoi AI - All Graphs Vs Total Time \n ' + hueristic.hueristicSummary, fontsize=16)

    # Adjust layout to prevent clipping of titles
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Show the plot
    plt.show()


#Algorithm End -------------------------------------------------------------------------------------------------------

#Main Function End

#---------------------------------------------------------------------------------------------------------------------------------

#Run the main function
main()

#---------------------------------------------------------------------------------------------------------------------------------

#End of File
