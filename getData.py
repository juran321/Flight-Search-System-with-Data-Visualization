import sqlite3 as db
database = db.connect('Graph.db')
d = database.cursor()
#create those four table named Graph.db
d.execute('DROP TABLE IF EXISTS Cities;')
d.execute('DROP TABLE IF EXISTS Flights;')
d.execute('DROP TABLE IF EXISTS Airlines;')
d.execute('DROP TABLE IF EXISTS Airports;')
d.execute('CREATE TABLE Cities(CityID integer not null primary key, \
                              CityName char(30),\
                              CityState char(10));')
d.execute('CREATE TABLE Airlines(AirlineID integer not null primary key,\
                                AirlineOperator char(50));')
d.execute('CREATE TABLE Airports(AirportID integer not null primary key,\
                                AirportName char(40),\
                                CityID integer unsigned,\
                                Longitude float,\
                                Latitude float,\
                                x float,\
                                y float);')
d.execute('CREATE TABLE Flights(FlightID integer not null primary key,\
                                FlightNumber char(30),\
                                FromID integer unsigned,\
                                ToID integer unsigned,\
                                AirlineID integer unsigned,\
                                DepartureTime char(30),\
                                ArrivalTime char(30));')


'''store the airport information to the list'''
try:
    file = open('Airport.txt','r')
except IOError:
    print('Cannot open this file')
#skip the first line
airportList = []
line =file.readline()
for line in file:
    word = line.rstrip().split('\t')
    airportList.append(word)
file.close()
#print(airportList)

'''store the flight information to the list'''
try:
    file = open('Flight.txt','r')
except IOError:
    print('Cannot open this file')
#skip the first line
flightList = []
line =file.readline()
for line in file:
    word = line.rstrip().split('\t')
    flightList.append(word)
file.close()
#print(flightList)

'''Insert data to my database'''

city_id = 1
airport_id = 1
airline_id = 1
flight_id = 1
from_id = 1
to_id = 1
city = []
airport = []
airline = []
flight = []
#add the data into Cities and Airports table
for data in airportList:
    if data[1] not in city:
        d.execute('INSERT INTO Cities(CityID, CityName, CityState)\
                                VALUES(?,?,?)',(city_id,data[1],data[2]))
        city_id += 1
        city.append(data[1])
 
    d.execute('SELECT C.CityID from Cities as C where C.CityName = ?;',(data[1],))
    cityid = d.fetchone()[0]
    d.execute('INSERT INTO Airports(AirportID,AirportName,CityID,Longitude,Latitude,x,y) \
                            VALUES(?,?,?,?,?,?,?)',
                            (airport_id,data[0],cityid,data[3],data[4],data[5],data[6]))
    airport_id += 1
airline_id = 1
#insert data into Airlines
for data in flightList:
    if data[1] not in airline:
        d.execute('INSERT INTO Airlines(AirlineID, AirlineOperator)\
                                VALUES(?,?)',
                                      (airline_id,data[1]))
        airline_id += 1
        airline.append(data[1])
#insert data into Flights
for data in flightList:
    d.execute('SELECT A.AirlineID FROM Airlines as A WHERE A.AirlineOperator = ?;',(data[1],))
    airline_id = d.fetchone()[0]
    d.execute('SELECT P.AirportID FROM Airports as P WHERE P.AirportName = ?;',(data[2],))
    from_id = d.fetchone()[0]
    d.execute('SELECT P.AirportID FROM Airports as P WHERE P.AirportName = ?;',(data[3],))
    to_id = d.fetchone()[0]
    d.execute('INSERT INTO Flights(FlightID, FlightNumber, FromID, ToID, AirlineID,DepartureTime,ArrivalTime)\
                            VALUES(?,?,?,?,?,?,?)',
                                  (flight_id,data[0],from_id,to_id,airline_id,data[4],data[5]))
    flight_id += 1
    
database.commit()
database.close()   