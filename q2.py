import sqlite3 as DBI
import getData as q1
from datetime import *




class Graph(object):
    def __init__(self, database):
        self.database = database
        try:
            self.db = DBI.connect(self.database)
            self.db.text_factory = str
        except:
            print('The Database cannot be opened')
            raise
        self.cur = self.db.cursor()
    #Calculate the time cost in a given flightID
    def getDuration(self,FlightID):
        self.cur.execute(getFlightTime,(FlightID,))
        ftime = self.cur.fetchall()
        d = datetime.strptime(ftime[0][0],'%H:%M')
        a = datetime.strptime(ftime[0][1],'%H:%M')
        return a - d 
    #Calculate the total duration between flightID1 and flightID 2
    def getTotalDuration(self,FlightID1, FlightID2):
        self.cur.execute(getTotalTime,(FlightID1,FlightID2))
        waitTime = self.cur.fetchall()
        a = datetime.strptime(waitTime[0][0],'%H:%M')
        d = datetime.strptime(waitTime[0][1],'%H:%M')
        layover = timedelta(minutes = 30)
        if d-a <= layover:
            d = d + timedelta(days = 1)
            return d - a
        return d - a 
    #helper function that helper to find all possible path between airport 1 and airport2
    #using DFS Search to find
    def searchPath(self,Airport1, Airport2, res, time, flight, airport):
        if Airport1 == Airport2:
            res.append([flight,time])            
            return        
        
        self.cur.execute(getAirportID,(Airport1,))
        airport.append(self.cur.fetchone()[0])


        self.cur.execute(getAllFlights,(Airport1,))
        options = self.cur.fetchall()
        for f in options:
            if f[0] not in flight:
                airport_id = f[1]
                if airport_id not in airport:
                    self.cur.execute(getAirportName,(airport_id,))
                    airport1 = self.cur.fetchone()[0]
                    flight.append(f[0])
                    total = time + self.getDuration(f[0])
                    self.searchPath(airport1, Airport2, res, total, flight[:], airport[:])
                    flight.remove(f[0])
        return
    #this function that can find all possible paths between 2 different airports            
    def findPath(self, Airport1, Airport2):
        res = []
        flight = []
        airport = []
        time = timedelta(hours = 0)
        self.searchPath(Airport1, Airport2, res, time, flight, airport)
        
        for path in res:
            for i in range(len(path[0])):
                if i+1 <len(path[0]):
                    path[1] += self.getTotalDuration(path[0][i], path[0][i+1])
                
        return res;
    #function that find the shortest path between 2 different airports.
    def findShortestPath(self, Airport1, Airport2):
        res = self.findPath(Airport1, Airport2)
        mini = res[0]
        miniDuration = res[0][1]
        for i in res:
            if i[1] < miniDuration:
                mini = i
                miniDuration = i[1]
        return mini
    #print the shortest path
    def getShortestPath(self,Airport1,Airport2):    
        self.cur.execute(getCity,(Airport1,))
        city1 = self.cur.fetchone()
        self.cur.execute(getCity,(Airport2,))
        city2 = self.cur.fetchone()
        
        info1 = 'From: %s in %s, %s to %s in %s, %s' %(Airport1,city1[0],city1[1],Airport2,city2[0],city2[1])+'\n'
        shortestpath = self.findShortestPath(Airport1, Airport2)
        self.cur.execute(getFlightTime,(shortestpath[0][0],))
        d = self.cur.fetchone()[0]
        self.cur.execute(getFlightTime,(shortestpath[0][len(shortestpath[0])-1],))
        a = self.cur.fetchone()[1]
        #duration = '{} days {} hours '.format(shortestpath[1].days, shortestpath[1].seconds / 3600)
        info2 = "Depart at: %s Arrive at: %s, Total travel time is %s (hour:minute:second)" %(d,a,shortestpath[1])+'\n'
        info3 =''
        for f in shortestpath[0]:
            self.cur.execute(getFlightNumber,(f,))
            flight = self.cur.fetchone()[0]
            
            self.cur.execute(getFromCity,(f,))
            fromCity = self.cur.fetchone()
            departCity = fromCity[0]
            departState = fromCity[1]
            
            
            self.cur.execute(getToCity,(f,))
            ToCity = self.cur.fetchone()
            
            arriveCity = ToCity[0]
            self.cur.execute(getAirport,(arriveCity,))
            air2 = self.cur.fetchone()
            arriveState = ToCity[1]
            self.cur.execute(getFlightTime,(f,))
            time = self.cur.fetchone()
            time1 = time[0]
            time2 = time[1]
            self.cur.execute(getAirport,(departCity,))
            air1 = self.cur.fetchone()
            info3 += "Taking %s from %s, %s (%s)  at %s to %s, %s (%s) at %s" %\
                  (flight,departCity,departState,air1[0],time1,arriveCity,arriveState,air2[0],time2)+'\n'
            
        return info1+info2+info3
    
    def getAirportCodes(self):
        self.cur.execute(getAllAirports)  
        air = self.cur.fetchall()  
        res = []
        for city in air:
            res.append(city[0])
        return res
#Select statements
#this statement can return all fights based on given airport name;
getAllFlights = '''
        SELECT F.FlightID, F.ToID
        FROM Flights as F, Airports as A
        WHERE F.FromID = A.AirportID
        AND A.AirportName = ?
        '''
#return the airport ID on given airport name
getAirportID = '''
        SELECT A.AirportID
        FROM Airports as A
        WHERE A.AirportName = ?
        '''
#return the airport name on given airport ID
getAirportName = '''
        SELECT A.AirportName
        FROM Airports as A
        WHERE A.AirportID = ?
        '''
#return airport name on given city name
getAirport = '''
        SELECT A.AirportName
        FROM Airports as A, Cities as C
        WHERE A.CityID = C.CityID
        AND C.CityName = ?
        '''
#return the departure time and arrival time based on the flight id
getFlightTime = '''
        SELECT F.DepartureTime, F.ArrivalTime
        FROM Flights as F
        Where F.FlightID = ?
        '''
#return the total fly time between 2 different flight number
getTotalTime = '''
        SELECT F1.ArrivalTime, F2. DepartureTime
        FROM Flights as F1, Flights as F2
        WHERE F1.FlightID = ?
        AND F2.FlightID = ?   
        '''
#return city name and city state on given airport name
getCity = '''
        SELECT C.CityName, C.CityState
        FROM Cities as C, Airports as A
        WHERE C.CityID = A.CityID
        AND A.AirportName = ?
        '''
#return the flight number on given flight ID 
getFlightNumber = '''
        SELECT FlightNumber 
        FROM Flights
        Where FlightID = ?
        '''
#return the from city name and city state on given flight id
getFromCity = '''
        SELECT C.CityName, C.CityState
        FROM Cities as C, Flights as F
        WHERE C.CityID = F.FromID
        AND F.FLightID = ?
    '''
#return the to city name and city state on given flight id
getToCity = '''
        SELECT C.CityName, C.CityState
        FROM Cities as C, Flights as F
        WHERE C.CityID = F.ToID
        AND F.FLightID = ?
    '''
getAllAirports = '''
        SELECT AirportName
        FROM Airports
'''
##########################
#######TEST##############

try:
    db = DBI.connect('Graph.db')
    db.text_factory = str
except:
    print('the database cannot be opened!')
    raise
new_db = db.cursor()
new_db.execute(getFlightTime,(1,))
name = new_db.fetchone()
#print(name)


g = Graph('Graph.db')
# # print (g.getTotalDuration(1, 2))
# # print(g.findPath('SEA', 'MIA'))
# # print(g.findShortestPath('SEA', 'MIA'))
#print(g.getShortestPath('SEA', 'MIA'))
# g.getAirport()
#print g.getShortestPath('MIA', 'SEA')
# #g.getShortestPath('SEA', 'SFO')
print(g.getAirportCodes())