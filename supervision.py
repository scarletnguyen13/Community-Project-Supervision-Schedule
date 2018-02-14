# Project Fries
# Create a supervision object and populate an array of supervision objects
# by reading an input file
#


import csv
import datetime
from teacher import *


class Supervision(object):
   
    def __init__(self, seq, date, day, bl, al, prepCafe1=None, prepCafe2=None, prepFirst=None, prepSecond=None):
        """__init__() functions as the class constructor"""
        self.seq = seq                 #probably redudant since we have actual date (integer)
        self.date = date               #actual date (Python object)
        self.day = day                 #character '0', '1', '2', 'S'-Statutory, 'V'-Minitsry Vacation, 'D'-Days not in session, 'N'-Non Instruction Day, 'A'-Admin Day
        self.bl = bl                   #block before lunch (char)
        self.al = al                   #block after lunch (char)
        self.prepCafe1 = prepCafe1     #teacher assigned
        self.prepCafe2 = prepCafe2     #teacher assigned
        self.prepFirst = prepFirst     #teacher assigned
        self.prepSecond = prepSecond   #teacher assigned
      
# make a list of supervision days
def populateSupervision(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()

    supervisionList = []
    
    for line in lines:
        mList = line.split(",")
        month = int(mList[1])
        day = int(mList[2])
        year = int(mList[3])
        supervisionList.append(Supervision(int(mList[0]), datetime.datetime(year, month, day), mList[4], mList[5], mList[6]))
        #teacherList.append(Teacher(mList[1], mList[2], mList[3], mList[4]))
    return (supervisionList)

# get a supervision instance given a sequence number
def getSupervisionInstanceBySeq(supervisionList, seq):
    supervision = None
    for supervision in supervisionList:
        if (supervision.seq == seq):
            return (supervision)

# update the current supervision mappings from a text file.  Update both supervisionList and teacherList
def updateExistingSupervisions(filename, teacherList, supervisionList):

    with open(filename) as file_object:
        lines = file_object.readlines()
      
    for line in lines:
        mList = line.split(",")
                
        # Get the supervision object instance given the sequence number
        seq = int(mList[0])
        supervision = getSupervisionInstanceBySeq(supervisionList, seq)

        if (supervision != None):
            # Get the teacher object instance given the teacher name
            teacherName = mList[1]
            teacher = getTeacherInstanceByName(teacherList, teacherName)
            if (teacher != None):
                supervision.prepCafe1 = teacher
                #update the teacherSupervision list in the teacher instance
                teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day,1))
                teacher.allocated += 1
                teacher.allocatedPrepCafe += 1

            teacherName = mList[2]
            teacher = getTeacherInstanceByName(teacherList, teacherName)
            if (teacher != None):
                supervision.prepCafe2 = teacher
                #update the teacherSupervision list in the teacher instance
                teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day,2))
                teacher.allocated += 1
                teacher.allocatedPrepCafe += 1

            teacherName = mList[3]
            teacher = getTeacherInstanceByName(teacherList, teacherName)
            if (teacher != None):
                supervision.prepFirst = teacher
                #update the teacherSupervision list in the teacher instance
                teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day, 3))
                teacher.allocated += 1
                teacher.allocatedPrepFirst += 1

            teacherName = mList[4]
            teacher = getTeacherInstanceByName(teacherList, teacherName)
            if (teacher != None):
                supervision.prepSecond = teacher
                #update the teacherSupervision list in the teacher instance
                teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day, 4))
                teacher.allocated += 1
                teacher.allocatedPrepSecond += 1

