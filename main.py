# Project Fries
#
# Taking a teacher list and a supervision calendar, create an array of teachers
# and an array of supervision objects, map teachers to supervision blocks and
# print a master supervision schedule.
#
# Also be able to take in an existing supervision schedule and populate the teacher
# and supervision arrays.
#
# Owner: Scarlet Nguyen

import csv
import datetime
import operator
import sys
from teacher import *
from supervision import *

from supportFunctions import *

#Get the list of populated teacher objects
teacherList = populateTeachers('text files/teachersV1.txt')

#Get the list of populated supervision objects
supervisionList = populateSupervision('text files/supervisionV1.txt')

#Get total number of supervision blocks for 2017
totalSupervision = snGetUnfilledSupervisionCafe(supervisionList)+ snGetUnfilledSupervisionFloor(supervisionList)

##############################################################################
##
##  You now have a populated array of teachers and supervision objects that
##  you can use in other defined functions that you will create in a separate
##  file and call from a main fries file. Prefix your files with your initials.
##
##  For example, my fries file would be called dbFries.py.
##
##  All functions should be written in a separate file and imported into
##  your xxFries.py file.
##
##  For example, my fries functions file would be called dbFriesFunctions.py
##
##############################################################################

#Get the teacher capacity - # of full-time teacher equivalents
teacherCapacity = snGetTeacherCapacity (teacherList)

#Get the number of unfilled floor and cafe supervisions
floorAllocationPerTeacher = snGetUnfilledSupervisionFloor(supervisionList)/ snGetTeacherCapacity (teacherList)
cafeAllocationPerTeacher = snGetUnfilledSupervisionCafe(supervisionList)/ snGetTeacherCapacity (teacherList)

#Print out the number of teachers of each employed block category and their pro-rated
#amount of supervision blocks
for i in range (1, 8):
    numTeachers = snGetNumberOfTeachers(teacherList, i)
    if (numTeachers != 0):
        print (repr(numTeachers).rjust(2), repr(i).rjust(2), "Block Teacher Allocation is ",
               "%.2f" % (i*(floorAllocationPerTeacher+cafeAllocationPerTeacher)/7))
    
#TODO: Assignment A - xxSetAllocation(teacherList, blocksEmployed, limit)
#Using the above pro-rated calculations, determine the actual allocations (round up or down)
#this data can be prompted for and then call a function that sets allocation limits
teacherList = snSetAllocation(teacherList)

#Read in an existing supervision-teacher mapping from file and make the assignments
#in the current supervisionList and teacherList(updating teacher currentCounts)
updateExistingSupervisions("text files/baseline.txt", teacherList, supervisionList)
print("Total unfilled supervision blocks is", totalSupervision)

#TESTING
sum = 0
for teacher in teacherList:
    print (teacher.name, teacher.blocksEmployed, teacher.allocation, teacher.allocated)
    sum = sum + teacher.allocation
#print("number of blocks filled =", sum)

#TO DO:  Assignment B - xxAssignSupervision(supervisionList, teacherList)
#Function assumes allocation limits are assigned. Can be broken down by using more functions
#Magic happens and teachers are mapped to supervision blocks based on allocations,
#days available, temporal spacing and possibly prep
#supervisionList = xxAssignSupervision(supervisionList, teacherList)
supervisionList = snAssignSupervision(supervisionList, teacherList)

#TESTING
for teacher in teacherList:
    print (teacher.name)
    for teacherSupervision in teacher.supervision:
        print (teacherSupervision.superSeq, teacherSupervision.date.strftime("%A, %B %d"), teacherSupervision.prep)

#TO DO:  Assignment C - xxPrintSchedule(supervisionList)
#Print completed schedule (function that prettys this up)
for supervision in supervisionList:
    
    if (supervision.day == '1' or supervision.day == '2'):

        print ("\n", supervision.date.strftime("%A, %B %d"), "( Day", supervision.day, ")")
            
        if (supervision.prepCafe1 != None):
            print ("  Cafeteria - person #1:", supervision.prepCafe1.name, "(11:40 am - 12:10 pm)")
        else:
            print ("  Cafeteria - person #1: None")
        if (supervision.prepCafe2 != None):
            print ("  Cafeteria - person #2:", supervision.prepCafe2.name, "(11:40 am - 12:10 pm)")
        else:
            print ("  Cafeteria - person #2: None")
        if (supervision.prepCafe2 != None):
            print ("              1st Floor:", supervision.prepFirst.name, "(11:40 am - 12:10 pm)")
        else:
            print ("              1st Floor: None")
        if (supervision.prepCafe2 != None):
            print ("     2nd and 3rd Floors:", supervision.prepSecond.name, "(11:40 am - 12:10 pm)")
        else:
            print ("     2nd and 3rd Floors: None")

#Prompt user to see if schedule should be saved
fileName = input("Name of file to be saved? ")
with open(fileName, 'w') as f_obj:
    for supervision in supervisionList:
        if (supervision.prepCafe1 != None):
            line = str(supervision.seq) + ","+ supervision.prepCafe1.name+","+ supervision.prepCafe2.name+","+ supervision.prepFirst.name+","+ supervision.prepSecond.name+",\n"
            print (line)
            f_obj.write(line)
f_obj.close

#TO DO:  Assignment D - xxPrintScheduleMetrics(supervisionList, teacherList)
#Get stats on a completed schedule, given a teacher list
#   total supervision days
#   teacher allocations and amount of teachers in each category
#   actual teacher assignments (max, min, average)
#   spacing between assignments (average, max, min)
print("STATS")
glGetPrepDay1(supervisionList, teacherList)
glGetPrepDay2(supervisionList, teacherList)
glTotalSupervisionDays(supervisionList)
glCheckCafBlocks(supervisionList,teacherList)

glCompareAllocated(supervisionList, teacherList)
glCountTeacherAllocated(supervisionList, teacherList)
glCheckLimit(supervisionList, teacherList)
glCheckTeacherWorkingDay(supervisionList, teacherList)
glCheckIfFull(supervisionList, teacherList)

#MRS. BRAATEN FUNCTION D
#TO DO:  Assignment D - xxPrintScheduleMetrics(supervisionList, teacherList)
#Get stats on a completed schedule, given a teacher list
dbPrintScheduleMetrics(supervisionList, teacherList)

