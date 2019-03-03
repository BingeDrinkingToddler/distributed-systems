import Pyro4
import xlrd
import random

#initialise dictionaries for local data storage
movies = {}
ratings = {}

#list of update requests to update another server if needed 
updatelist = []

#reading data file and populatin dictionaries
loc = ("movies.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for i in range(1,sheet.nrows):
    movies[sheet.cell_value(i,1)[:-7].lower()] = sheet.cell_value(i,0)

loc = ("ratings.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

movieid = 0
for i in range(1,sheet.nrows):
    if sheet.cell_value(i,1) == movieid:
        ratings[sheet.cell_value(i,1)].append([int(sheet.cell_value(i,0)),sheet.cell_value(i,2)])
    else:
        ratings[sheet.cell_value(i,1)] = [[int(sheet.cell_value(i,0)),sheet.cell_value(i,2)]]
        movieid = sheet.cell_value(i,1)

#list of other servers
servers = ["Server1","Server3"]

#function
#add review called by self
def addReview(userId, movie, review):
        try:
            movieId = movies[movie]
            for i in ratings[movieId]:
                if i[0] == int(userId):
                    raise Exception
            ratings[movieId].append([int(userId), float(review)])
        except:
            return("an error occured, user review already exists or movie not found")
        else:
            return("Success")

#function
#update review called by self
def updateReview(userId,movie, review):
    try:
        movieId = movies[movie]
        userfound = False
        for i in ratings[movieId]:
            if i[0] == int(userId):
                userfound = True
                i[1] = float(review)
        if userfound == False:
            raise Exception
    except:
        return("an error occured, userId not found, movie not found")
    else:
        return("Succes")



options = {"add":addReview,
           "update":updateReview
           }
#on start get updates from another server and update self
found = False
for i in servers:
    try:
        Function = Function = Pyro4.Proxy("PYRONAME:"+i)
        updates = Function.updatelist()
        found = True
        for i in updates:
            options[i[0]](i[1],i[2],i[3])
        if found == True:
            break
    except:
        next

#functions registered in RMI
@Pyro4.expose
class functions(object):
    #function
    #get review from data
    def getReview(self,movie):
        try:
            movieId = movies[movie]
            return ratings[movieId]
        except:
            return("movie not found")
    #function
    #add review to data
    def addReview(self,userId, movie, review, update):
        try:
            movieId = movies[movie]
            for i in ratings[movieId]:
                if i[0] == int(userId):
                    raise Exception
            updatelist.append(["add",userId,movie,review])
            ratings[movieId].append([int(userId), float(review)])
        except:
            return("an error occured, user review already exists or movie not found")
        else:
            if update == "1":
                for i in servers:
                    try:
                        Function = Pyro4.Proxy("PYRONAME:"+i)
                        Function.addReview(userId,movie,review,"0")
                    except:
                        next

            return("Success")
    #function
    #update review in data
    def updateReview(self,userId,movie, review, update):
        try:
            movieId = movies[movie]
            userfound = False
            for i in ratings[movieId]:
                if i[0] == int(userId):
                    userfound = True
                    updatelist.append(["add",userId,movie,review])
                    i[1] = float(review)
            if userfound == False:
                raise Exception
        except:
            return("an error occured, userId not found, movie not found")
        else:
            if update == "1":
                for i in servers:
                    try:
                        Function = Pyro4.Proxy("PYRONAME:"+i)
                        Function.updateReview(userId,movie,review,"0")
                    except:
                        next
            return("Succes")

    #function
    #get status from server
    def getStatus(self):
        rand = random.randint(1,3)
        options = {1:"active",
                   2:"over-loaded",
                   3:"offline"
                   }
        return options[rand]
    #function
    #return list of updates
    def updatelist(self):
        return updatelist

#register server object in RMI
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(functions)
ns.register("Server2" , uri)


print("ready")
daemon.requestLoop()
