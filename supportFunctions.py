# Fries' Functions
#
# Contains the functions that are called by Fries
#
# Owner: Scarlet Nguyen
# Date: Oct 18, 2017

import datetime
import random
from random import shuffle
from teacher import *
from supervision import *

#Return the number of missing/unfilling shifts for 1st, 2nd and 3rd floor
def snGetUnfilledSupervisionFloor(supervisionList, startDate=None, endDate=None):
    #if the user don't put startDate and endDate into the arguments
    if (startDate == None) and (endDate == None):
        unfilledSupervisonFloor = 0
        for x in supervisionList:
            if x.day == '1' or x.day == '2':
                #add 2 if both shifts need to be filled
                if x.prepFirst == None and x.prepSecond == None:
                    unfilledSupervisonFloor += 2
                #add 1 if only 1 shift need to be filled
                elif x.prepFirst == None or x.prepSecond == None:
                    unfilledSupervisonFloor += 1
        return unfilledSupervisonFloor
    #if the user put startDate and endDate into the arguments
    else:
        #create a list of dates from the supervisionList
        dates = []
        for x in supervisionList:
            dates.append(x.date)

        #checking if the input dates are in the dates list
        if (startDate in dates) and (endDate in dates):
            #create a sublist of supervisionList where it starts with the input startDate and ends with input endDates
            miniSupervisionList = []
            #create new variables for the startDate's and endDate's supervision
            startSup = None
            endSup = None
            #go through the supervisionList and declair the variables
            for x in supervisionList:
                if x.date == startDate:
                    startSup = x
                if x.date == endDate:
                    endSup = x
            #fill the sublist
            for i in range(supervisionList.index(startSup),supervisionList.index(endSup) + 1):
               miniSupervisionList.append(supervisionList[i])
            return snGetUnfilledSupervisionFloor(miniSupervisionList)

#Return the number of missing/unfilling shifts for the cafe
#The logic and structures are basically the same as the snGetUnfilledSupervisionFloor function
def snGetUnfilledSupervisionCafe(supervisionList, startDate=None, endDate=None):
    if (startDate == None) and (endDate == None):
        unfilledSupervisonCafe = 0
        for x in supervisionList:
            if x.day == '1' or x.day == '2': 
                if x.prepCafe1 == None and x.prepCafe2 == None:
                    unfilledSupervisonCafe += 2
                elif x.prepCafe1 == None or x.prepCafe2 == None:
                    unfilledSupervisonCafe += 1
        return unfilledSupervisonCafe
    else:
        dates = []
        for x in supervisionList:
            dates.append(x.date)
            
        if (startDate in dates) and (endDate in dates):
            miniSupervisionList = []
            startSup = None

            endSup = None
            for x in supervisionList:
                if x.date == startDate:
                    startSup = x
                if x.date == endDate:
                    endSup = x
            for i in range(supervisionList.index(startSup),supervisionList.index(endSup) + 1):
               miniSupervisionList.append(supervisionList[i])
            return snGetUnfilledSupervisionCafe(miniSupervisionList)

#Return the teacher's capacity in a year
def snGetTeacherCapacity(teacherList):
    total = 0
    #get blocksEmployed from every teacher and add them up together
    for x in teacherList:
        total += x.blocksEmployed
    #divide the total by 7 (which gives us the allocation through out the entire year)
    return total / 7

#TODO: ADD COMMENTS TO THIS FUNCTION
def snGetNumberOfTeachers(teacherList, employedBlocks):
    count = 0
    for x in teacherList:
        if x.blocksEmployed == employedBlocks:
            count += 1
    return count

def snSetAllocation(teacherList):
    for teacher in teacherList:
        if teacher.blocksEmployed == 3:
            teacher.allocation = 3
        elif teacher.blocksEmployed == 4:
            teacher.allocation = 4
        elif teacher.blocksEmployed == 6:
            teacher.allocation = 8
        else:
            teacher.allocation = 10
    return teacherList

#Function assumes allocation limits are assigned. Can be broken down by using more functions
#Magic happens and teachers are mapped to supervision blocks based on allocations,
#days available, temporal spacing and possibly prep
def snAssignSupervision(supervisionList, teacherList):
    distributedDay1 = []
    distributedDay2 = []
    for teacher in teacherList:
        if teacher.day == '1' or (teacher.prep >= 1 and teacher.prep <= 4):
            distributedDay1.append(teacher)
        elif teacher.day == '2' or (teacher.prep >= 5 and teacher.prep <= 8):
            distributedDay2.append(teacher)
        else:
            distributedDay1.append(teacher)
    teacherListDay1 = snShuffleListAllocationBased(distributedDay1)
    teacherListDay2 = snShuffleListAllocationBased(distributedDay2)
    for supervision in supervisionList:
        if snGetEmptySupervision(supervision) == True:
            if supervision.day == '1' and len(teacherListDay1) >= 4:
                for i in range(1,5):
                    teacher = teacherListDay1[0]
                    teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day,i))
                    teacher.allocated += 1
                    if i == 1:
                        supervision.prepCafe1 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 2:
                        supervision.prepCafe2 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 3:
                        supervision.prepFirst = teacher
                        teacher.allocatedPrepFirst += 1
                    else:
                        supervision.prepSecond = teacher
                        teacher.allocatedPrepSecond += 1
                    del teacherListDay1[0]   
            elif supervision.day == '2' and len(teacherListDay2) >= 4:
                for i in range(1,5):
                    teacher = teacherListDay2[0]
                    teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day,i))
                    teacher.allocated += 1
                    if i == 1:
                        supervision.prepCafe1 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 2:
                        supervision.prepCafe2 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 3:
                        supervision.prepFirst = teacher
                        teacher.allocatedPrepFirst += 1
                    else:
                        supervision.prepSecond = teacher
                        teacher.allocatedPrepSecond += 1
                    del teacherListDay2[0]
    extra = []
    for teacher in teacherList:
        if teacher.allocated < teacher.allocation:
            extra.append(teacher)
    extra.sort(key=lambda x: x.allocated, reverse=False)
    for supervision in supervisionList:
        if snGetEmptySupervision(supervision) == True and (supervision.day == '1' or supervision.day == '2'):
            if len(extra) >= 4:
                for i in range(1,5):
                    teacher = extra[0]
                    teacher.supervision.append(TeacherSupervision(supervision.seq, supervision.date, supervision.day,i))
                    teacher.allocated += 1
                    if i == 1:
                        supervision.prepCafe1 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 2:
                        supervision.prepCafe2 = teacher
                        teacher.allocatedPrepCafe += 1
                    elif i == 3:
                        supervision.prepFirst = teacher
                        teacher.allocatedPrepFirst += 1
                    else:
                        supervision.prepSecond = teacher
                        teacher.allocatedPrepSecond += 1
                    del extra[0]
                    
    return supervisionList
def snPrintSchedule(supervisionList):
    return 0

#Get stats on a completed schedule, given a teacher list
#total supervision days
#teacher allocations and amount of teachers in each category
#actual teacher assignments (max, min, average)
#spacing between assignments (average, max, min)
def snPrintScheduleMetrics(supervisionList, teacherList):
    return 0

def snGetTeacherCurrentAllocation(teacherList, teacherName):
    count = 0
    for teacher in teacherList:
        if teacher.name == teacherName:
            count += teacher.allocatedPrepCafe + teacher.allocatedPrepFirst + teacher.allocatedPrepSecond
    return count

def snGetFullTimeTeachers(teacherList):
    fullTime = []
    for teacher in teacherList:
        if teacher.blocksEmployed == 7:
            fullTime.append(teacher)
    return fullTime

#SUPPORT FUNCTIONS for <--snAssignSupervision-->  
def snGetEmptySupervision(supervision):
    if supervision.prepCafe1 == None and supervision.prepCafe2 == None and supervision.prepFirst == None and supervision.prepSecond == None:
        return True
    else:
        return False

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def snShuffleListAllocationBased(teacherList):
    allocationBased = []
    teacherDict = dict()
    for x in teacherList:
        teacherDict[x] = x.allocation - x.allocated
    while len(teacherDict) > 0:
        fragment  = []
        for teacher in teacherDict:
            if teacherDict.get(teacher) > 0:
                fragment.append(teacher)
                teacherDict[teacher] = teacherDict.get(teacher) - 1
            else:
                teacherDict = removekey(teacherDict, teacher)
        shuffle(fragment)
        allocationBased.extend(fragment)
    return allocationBased

#GRACE LOU'S FUNCTION D
#STATS
    #get number of teacher with prep on day 1, and prep on day 2     
def glGetPrepDay1(supervisionList, teacherList):
    prepDay1 = 0
    for teacher in teacherList:
        if 1 <= teacher.prep <= 4:
            prepDay1+=1
    print("Teachers with Day 1 prep:", prepDay1)

def glGetPrepDay2(supervisionList, teacherList):
    prepDay2 = 0
    for teacher in teacherList:
        if 5 <= teacher.prep <= 8:
            prepDay2+=1
    print("Teachers with Day 2 prep:", prepDay2)

    #get number of supervision days
def glTotalSupervisionDays(supervisionList):
    supervisionDays = 0
    for supervision in supervisionList:
        if supervision.day == '1' or supervision.day == '2':
            supervisionDays += 1
    print("Total number of supervision days:", supervisionDays)

def glCountTeacherAllocated(supervisionList, teacherList):
    for allocated in range(0,12):
        numOfTeachers = 0
        for teacher in teacherList:
            if teacher.allocated == allocated:
                numOfTeachers+=1
        if numOfTeachers != 0:
            print("Teachers with", allocated, "allocations:", numOfTeachers)
        
#average spacing between shifts for each category # of allocated supervision
def glCheckSpacing(supervisionList,teacherList,name):
    for supervision in supervisionList:
            if supervision.prepCafe1.name==name or supervision.prepCafe2.name==name or supervision.prepFirst.name==name or supervision.prepSecond.name==name:
                d1= supervision.seq
    #look for name
    #if name matches given, record date(sequence number?) as d1
    #continue looking for name, second time record sequence number as d2
    #calculate difference (space) between days (d2-d1) and record in a list
    #reset and continue

    
    #counter to count days until their name appears
    #once name appears, record days in between to a list
    #reset counter to zero and continue thru calendar until done
    #add up numbers in list and take average
    #output max and min numbers in list
                

#WARNINGS
def glCheckCafBlocks(supervisionList,teacherList):
    print("WARNING: Teachers with too many cafe blocks")
    for teacher in teacherList:
        if teacher.allocatedPrepCafe > (teacher.allocated/2): #check if allocated Cafe blocks is more than half of allocated
            print(teacher.name, ": ", teacher.allocatedPrepCafe, "/", teacher.allocated)


#def glCheckPrepAdjacency(supervisionList, teacherList):


#ERRORS
def glCheckLimit(supervisionList, teacherList):
    print("ERROR: Teacher assigned too many supervision blocks")
    for teacher in teacherList:
        if teacher.allocated > teacher.allocation:
            print(teacher.name, ":", teacher.allocated,"/", teacher.allocation)

        
def glCheckTeacherWorkingDay(supervisionList, teacherList):
    for teacher in teacherList: #go through teacher list
        if teacher.day != '0': #if teacher only works on 1 day
            for teacherSupervision in teacher.supervision: #go through mapped supervision schedule 
                if int(teacher.day) != int(teacherSupervision.day):#check if supervision day is on the day that they work
                     print("ERROR:", teacher.name, "only works on day", teacher.day)#KLINE day 2s only, but works 7 blocks??
                     print("Assigned", teacherSupervision.date, " day", teacherSupervision.day)
               
                    
                
def glCheckIfFull(supervisionList, teacherList):
    for supervision in supervisionList:
        if supervision.day == '1' or supervision.day== '2':
            if (supervision.prepCafe1 == None or supervision.prepCafe2 == None or supervision.prepFirst == None or supervision.prepSecond == None):
                print("ERROR: not all supervision blocks filled")
                print(supervision.date)

def glCompareAllocated(supervisionList, teacherList):
    for employedBlocks in range(1,8):
        allocated = []
        diff = 0
        maximum = 0
        minimum = 0
        maxList = []
        minList = []
        for teacher in teacherList:
            if teacher.blocksEmployed == employedBlocks:
                allocated.append(teacher.allocated)
                maximum = max(allocated)
                minimum = min(allocated)
            diff = int(maximum-minimum)

            if teacher.blocksEmployed == employedBlocks:
                if int(teacher.allocated) == int(maximum):
                    maxList.append(teacher.name)
                elif int(teacher.allocated) == int(minimum):
                    minList.append(teacher.name)
        if diff > 1:   #if difference is greater than 1, ERROR
            print("ERROR: Allocated difference too big for teachers working", employedBlocks, "blocks")
            print("MAX:", maximum, "(", maxList, ")")
            print("MIN:", minimum, "(", minList, ")")
        elif diff == 1:  #if difference is 1, WARNING
            print("WARNING: Allocated difference of 1 for teachers working", teacher.blocksEmployed, "blocks")

#MRS BRAATEN - FUNCTION D - SCHEDULE MATRIX
# print schedule metrics
def dbPrintScheduleMetrics(supervisionList, teacherList):
    print ('\n')
    print("Schedule Metrics")
    print(" Total supervision days = ", dbGetTotalSupervisionDays(supervisionList))
    print(" Total supervision blocks = ", dbGetTotalSupervisionBlocks(supervisionList))

    # Errors – summary and listing
        #Not all teachers in same category have same allocated – difference > 1
        #Not all supervision blocks filled  
        #Teacher assigned on a non-working day for them
    # Warnings – summary and listing
        #Not all teachers in same category have same allocated – difference of 1
        #Multiple supervisions within 1 week (supervisions)
        #Supervision not next to prep
        #More than half of blocks are café
    
    print ('\n')
    error1 = dbSupervisionDifferenceError(teacherList)
    print("ERRORS:", error1, "Teachers in same category differ by more than 1")

    error2 = dbSupervisionBadDay (teacherList)
    print ("ERRORS:", error2, "Teachers assigned on non-working day")

    error3 = dbSupervisionWithinX (teacherList, 5)
    print ("ERRORS:", error3, "Teachers have multiple supervisions within 5 days")

    print ('\n')
    warning1 = dbSupervisionDifferenceWarning(teacherList)
    print("WARNINGS:", warning1, "Teachers in same category differ 1")

    warning2 = dbSupervisionPrepDayWarning(supervisionList)
    print("WARNINGS:", warning2, "Teachers have supervision on non-prep day")
    
    warning3 = dbSupervisionPrepWarning(supervisionList)
    print("WARNINGS:", warning3, "Teachers have supervision not adjacent to prep")

    warning4 = dbSupervisionCafeSplit (teacherList)
    print ("WARNINGS:", warning4, "Teachers have more than half cafe supervision blocks")
    
    warning5 = dbSupervisionWithinX (teacherList, 10)
    print ("WARNINGS:", warning5, "Teachers has multiple supervisions within 10 days")
    
# get total supervision days
def dbGetTotalSupervisionDays(supervisionList):
    count = 0
    for supervision in supervisionList:
        if (supervision.day == '1' or supervision.day == '2'):
                if (supervision.prepCafe1 != None):
                    count += 1       
    return (count)

# get total supervision blocks
def dbGetTotalSupervisionBlocks(supervisionList):
    count = 0
    for supervision in supervisionList:
        if (supervision.day == '1' or supervision.day == '2'):
                if (supervision.prepCafe1 != None):
                    count += 1
                if (supervision.prepCafe2 != None):
                    count += 1
                if (supervision.prepFirst != None):
                    count += 1
                if (supervision.prepSecond != None):
                    count += 1
    return (count)

# get supervision difference by category
def dbSupervisionDifferenceError(teacherList):
    count = 0
    for teacher in teacherList:
        if ((teacher.allocation - teacher.allocated) > 1):
            print ("  Error:", teacher.name, teacher.allocated, "of", teacher.allocation)
            count += 1
    return (count)

# get supervision difference by category
def dbSupervisionDifferenceWarning(teacherList):
    count = 0
    for teacher in teacherList:
        if ((teacher.allocation - teacher.allocated) == 1):
            print ("  Warning:", teacher.name, teacher.allocated, "of", teacher.allocation)
            count += 1
    return (count)

# bad assignment
def dbSupervisionBadDay (teacherList):
    count = 0
    for teacher in teacherList:
        if (teacher.day != '0'):
            for supervision in teacher.supervision:
                if (teacher.day != supervision.day):
                    print ("  Error:", teacher.name, supervision.date.strftime("%A, %B %d"), "Day ", supervision.day)
                    count += 1
    return (count)

def dbSupervisionPrepWarning(supervisionList):
    count = 0
    for supervision in supervisionList:
        if (supervision.day == '1' or supervision.day == '2'):
            if (supervision.prepCafe1.prep != 0):
                if ((supervision.prepCafe1.prep != int (supervision.bl)) and (supervision.prepCafe1.prep != int(supervision.al))):
                    count += 1
                    #print ("  Warning:", supervision.prepCafe1.name, supervision.date.strftime("%A, %B %d"))
            if (supervision.prepCafe2.prep != 0):
                if ((supervision.prepCafe2.prep != int (supervision.bl)) and (supervision.prepCafe2.prep != int(supervision.al))):
                    count += 1
                    #print ("  Warning:", supervision.prepCafe2.name, supervision.date.strftime("%A, %B %d"))
            if (supervision.prepFirst.prep != 0):
                if ((supervision.prepFirst.prep != int (supervision.bl)) and (supervision.prepFirst.prep != int(supervision.al))):
                    count += 1
                    #print ("  Warning:", supervision.prepFirst.name, supervision.date.strftime("%A, %B %d"))
            if (supervision.prepSecond.prep != 0):
                if ((supervision.prepSecond.prep != int (supervision.bl)) and (supervision.prepSecond.prep != int(supervision.al))):
                    count += 1
                    #print ("  Warning:", supervision.prepSecond.name, supervision.date.strftime("%A, %B %d"))
    return (count)

def dbSupervisionPrepDayWarning(supervisionList):
    count = 0
    for supervision in supervisionList:
        if(supervision.prepCafe1 != None):
            if (supervision.day == '1'):
                if ((supervision.prepCafe1.prep >= 5) and (supervision.prepCafe1.prep <= 8) and (supervision.prepCafe1.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepCafe1.name, supervision.prepCafe1.prep, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepCafe2.prep >= 5) and (supervision.prepCafe2.prep <= 8) and (supervision.prepCafe2.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepCafe2.name, supervision.prepCafe2.prep, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepFirst.prep >= 5) and (supervision.prepFirst.prep <= 8) and (supervision.prepFirst.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepFirst.name, supervision.prepFirst.prep, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepSecond.prep >= 5) and (supervision.prepSecond.prep <= 8) and (supervision.prepSecond.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepSecond.name, supervision.prepSecond.prep, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
            elif (supervision.day == '2'):
                if ((supervision.prepCafe1.prep >= 1) and (supervision.prepCafe1.prep <= 4) and (supervision.prepCafe1.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepCafe1.name, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepCafe2.prep >= 1) and (supervision.prepCafe2.prep <= 4) and (supervision.prepCafe2.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepCafe2.name, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepFirst.prep >= 1) and (supervision.prepFirst.prep <= 4) and (supervision.prepFirst.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepFirst.name, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
                if ((supervision.prepSecond.prep >= 1) and (supervision.prepSecond.prep <= 4) and (supervision.prepSecond.prep != 0)):
                    count += 1
                    print("  Warning:", supervision.prepSecond.name, supervision.date.strftime("%A, %B %d"),"Day ", supervision.day)
    return (count)

def dbSupervisionWithinX (teacherList, gap):
    count = 0
    for teacher in teacherList:
        date = teacher.supervision[0].date
        for i in range (1, len(teacher.supervision)-1):
            if ((teacher.supervision[i].date - date).days <= gap):
                count += 1
                print ("  Error:", teacher.name, (teacher.supervision[i].date - date).days)
            date = teacher.supervision[i].date
    return (count)

def dbSupervisionCafeSplit (teacherList):
    count = 0
    for teacher in teacherList:
        if (teacher.allocatedPrepCafe > (teacher.allocatedPrepFirst + teacher.allocatedPrepSecond + 1)):
            print ("  Warning:", teacher.name, teacher.allocatedPrepCafe, teacher.allocatedPrepFirst + teacher.allocatedPrepSecond)
            count += 1
    return (count)

