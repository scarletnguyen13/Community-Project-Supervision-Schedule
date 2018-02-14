# Project Fries
# Create a teacher object and populate an array of teacher objects
# by reading info from an input file 
#

class Teacher(object):
   
    def __init__(self, ID, name, email, prep, blocksEmployed, day, limit = None, allocation=None, allocatedPrepCafe=None, allocatedPrepFirst=None, allocatedPrepSecond=None, supervision=None):
        """__init__() functions as the class constructor"""
        self.ID = ID                         #unique ID given to each teacher (integer)
        self.name = name                     #text that identifies the teacher's name to be used for printing
        self.email = email                   #test that incudes the teacher email
        self.prep = prep                     #blocks represented by 1 to 8 (1.1, 1.2, 1.3, ..., 2.4) (integer)
        self.blocksEmployed = blocksEmployed #how many blocks a teacher works, full time is 7 (integer)
        self.day = day                       #represents which days teacher works 0=both days, 1 or 2 char
        self.allocation = 0                  #how many blocks they should have, initialized to 0
        self.allocated = 0                   #how many blocks they currently have, initialized to 0
        self.allocatedPrepCafe = 0           #how many cafe blocks they currently have
        self.allocatedPrepFirst = 0          #how many 1st Floor blocks they currently have
        self.allocatedPrepSecond = 0         #how many 2nd/3rd Floor blocks they currently have
        self.supervision = []                #list of teacher supervision blocks for this teacher
   
class TeacherSupervision(object):
    
    def __init__(self, superSeq, date, day, prep):
        """__init__() functions as the class constructor"""
        self.superSeq = superSeq             #unique sequential id of the supervision schedule
        self.date = date                     #date of the assigned supervision
        self.day = day                       #day of supervision (1 or 2) char
        self.prep = prep                     #type of prep (1-cafe1, 2-cafe2, 3-first floor, 4-second and third floor
       
# make a list of class Teacher(s)
def populateTeachers(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()

    teacherList = []
    for line in lines:
        mList = line.split(",")
        teacherList.append(Teacher(int(mList[0]), mList[1], mList[2], int (mList[3]), int(mList[4]), mList[5]))
    return (teacherList)

# get a teacher instance given a teacher name
def getTeacherInstanceByName(teacherList, teacherName):
    teacher = None
    for teacher in teacherList:
        if (teacher.name == teacherName):
            return (teacher)
        
# print out the list of teachers and their assigned supervisions
def printTeacherSupervisions (teacherList):
    for teacher in teacherList:
        if (teacher.prep == 0):
            prep = "no prep"
        elif (teacher.prep == 1):
            prep = "1-1"
        elif (teacher.prep == 2):
            prep = "1-2"
        elif (teacher.prep == 3):
            prep = "1-3"
        elif (teacher.prep == 4):
            prep = "1-4"
        elif (teacher.prep == 5):
            prep = "2-1"
        elif (teacher.prep == 6):
            prep = "2-2"
        elif (teacher.prep == 7):
            prep = "2-3"
        elif (teacher.prep == 8):
            prep = "2-4"
            
        print ("\n", teacher.name, "Prep (", prep, ") has", teacher.allocated, "of", teacher.allocation, "cafe:", teacher.allocatedPrepCafe,", 1st floor:", teacher.allocatedPrepFirst,", 2nd-3rd floor:",teacher.allocatedPrepSecond)
        for teacherSupervision in teacher.supervision:
            if (teacherSupervision.prep == 1):
                prepType = "Cafe 1"
            elif (teacherSupervision.prep == 2):
                prepType = "Cafe 2"
            elif (teacherSupervision.prep == 3):
                prepType = "1st Floor"
            elif (teacherSupervision.prep == 4):
                prepType = "2nd and 3rd Floors"
            else:
                prepType = "NA"
            print ("   ", teacherSupervision.date.strftime("%A, %B %d"), "Day (", teacherSupervision.day, ")", prepType)


