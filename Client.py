import Pyro4

#functions to get inputs from the user and check that the user input is valid

#function
#asks user for movie name and sets to lower case
def getMovie():
    movie = input("what movie?")
    movie = movie.lower()
    return movie

#function
#asks user for user id until valid id is input
def getId():
    while True:
        try:
            userId = input("what is your user id?")
            if checkId(userId) == Exception:
                raise Exception
            return userId
        except:
            print("userId must be an integer")

#function
#asks user for a review until a valid input
def getReview():
    while True:
        try:
            review = input("give a review out of 5")
            if checkReview(review) == Exception:
                raise Exception
            return review
        except:
            print("review must be a value between 0 and 5")


#function
#checks if value is between 0 and 5 for a valid review
def checkReview(value):
    try:
        value = float(value)
        if value > 5 or value < 0:
            raise Exception
        return True
    except:
        return Exception

#function
#checks is value is an integer for a valid id
def checkId(value):
    try:
        int(value)
        return True
    except:
        return Exception

#functions to send request to the front server
def get():
    movie = getMovie()
    Function = Pyro4.Proxy("PYRONAME:frontServer")
    print(Function.chooseServer("get",None,movie,None))
    
def add():
    userId = getId()
    movie = getMovie()
    review = getReview()
    Function = Pyro4.Proxy("PYRONAME:frontServer")
    print(Function.chooseServer("add",userId,movie,review))
    
def update():
    userId = getId()
    movie = getMovie()
    review = getReview()
    Function = Pyro4.Proxy("PYRONAME:frontServer")
    print(Function.chooseServer("update",userId,movie,review))

run = True
#interface
#asks user for a request and relavent data for request until the program is closed
while run:
    request = input("1 = get reviews, 2 = add review, 3 = update review, quit to close")
    options = { "1" : get,
                "2" : add,
                "3" : update
                }
    try:
        options[request]()
    except KeyError:
        if request.lower() == "quit":
            run = False
        else:
            print("this is not an option")
            
