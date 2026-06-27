from database.DB_connect import DBConnect
from model.Arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct YEAR(s.datetime) as anno
                           from sighting s
                       order by year(s.`datetime` ) """
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getForme():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s2.Name 
from state s2 
 """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Name"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(anno, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select s.*
from sighting s,state s2  
where year(s.`datetime`) =%s and s.state =s2.id and s2.Name =%s """
            cursor.execute(query, (anno, stato))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(anno, stato,idMapA):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """  select s.id a1, s2.id a2
from sighting s ,sighting s2 ,state s3 
where year(s.`datetime`) =%s and s.state =s3.id and s3.Name =%s and  year(s2.`datetime`) =%s and s2.state =s3.id and s3.Name =%s
and s.shape =s2.shape and s.id <s2.id """
            cursor.execute(query, (anno, stato,anno,stato))

            for row in cursor:
                result.append(Arco(idMapA[row["a1"]], idMapA[row["a2"]]))
            cursor.close()
            cnx.close()
        return result
