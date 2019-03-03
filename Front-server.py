import Pyro4
import xlrd

#list of servers
servers = ["Server1","Server2","Server3"]


#functions registered in RMI
@Pyro4.expose
class functions(object):
    #function
    #get status from each server and choose the best to use
    def chooseServer(self,request,userId,movie,review):
        statuslst = []
        for i in servers:
            found = False
            try:
                Function = Pyro4.Proxy("PYRONAME:"+i)
                status = Function.getStatus()
                found = True
                options = {"active":1,
                           "over-loaded":2,
                           "offline":3
                           }
                statuslst.append(options[status])
                if options[status] == 1:
                    break
            except:
                if found == False:
                    statuslst.append(3)
                    next
        lowest = 0
        server = 0
        count = 0
        for i in statuslst:
            if i < lowest or lowest == 0:
                lowest = i
                server = servers[count]
                count += 1
        if lowest == 3:
            return "no servers available"
        else:
            print(server)
            options = {"get":get,
                       "add":add,
                       "update":update
                       }
            return options[request](userId,movie,review,server)
        
#functions to call server to execute request
def add(userId, movie, review,server):
    Function = Pyro4.Proxy("PYRONAME:"+server)
    return Function.addReview(userId,movie,review,"1")

def get(userId, movie, review,server):
    Function = Pyro4.Proxy("PYRONAME:"+server)
    return Function.getReview(movie)

def update(userId, movie, review,server):
    Function = Pyro4.Proxy("PYRONAME:"+server)
    return Function.updateReview(userId,movie,review,"1")

#register server object in RMI
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(functions)
ns.register("frontServer" , uri)


print("ready")
daemon.requestLoop()
