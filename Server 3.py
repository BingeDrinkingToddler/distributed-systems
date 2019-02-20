import Pyro4
import xlrd
import random

movies = {}
ratings = {}

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

servers = ["Server2","Server1"]
@Pyro4.expose
class functions(object):
    def getReview(self,movie):
        try:
            movieId = movies[movie]
            return ratings[movieId]
        except:
            return("movie not found")

    def addReview(self,userId, movie, review, update):
        try:
            movieId = movies[movie]
            for i in ratings[movieId]:
                if i[0] == int(userId):
                    raise Exception
            ratings[movieId].append([int(userId), float(review)])
        except:
            return("an error occured, user review already exists or movie not found")
        else:
            if update == "1":
                for i in servers:
                    Function = Pyro4.Proxy("PYRONAME:"+i)
                    Function.addReview(userId,movie,review,"0")

            return("Success")

    def updateReview(self,userId,movie, review, update):
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
            if update == "1":
                for i in servers:
                    Function = Pyro4.Proxy("PYRONAME:"+i)
                    Function.updateReview(userId,movie,review,"0")
            return("Succes")
        
    def getStatus(self):
        rand = random.randint(1,3)
        options = {1:"active",
                   2:"over-loaded",
                   3:"offline"
                   }
        return options[rand]


    
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(functions)
ns.register("Server3" , uri)


print("ready")
daemon.requestLoop()
