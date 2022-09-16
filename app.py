import collections
from datetime import datetime
from unicodedata import category
from urllib import response
from flask import Flask, request, json, Response
import pymongo
from pymongo import MongoClient
from bson import json_util
import logging as log
from wtforms import  Form, IntegerField ,BooleanField, StringField, PasswordField, validators, URLField

app = Flask(__name__)

def xstr(s):
    return '' if s is None else str(s)

def xnum(s):
    return 0 if s is None else int(s)

def xlist(s):
    return [] if s is None else s[0]

def parse_json(data):
    return json.loads(json_util.dumps(data))



class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        # self.client = MongoClient("mongodb://localhost:27017/")  # When only Mongo DB is running on Docker.
        self.client = MongoClient("mongodb+srv://admin:qrIyd1Nmx6f2Lf3O@cluster0.gwm0k3a.mongodb.net/?retryWrites=true&w=majority")     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose
        self.filter = filter
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def findOne(self):
        filter = self.data['filter']
        datax = self.collection.find_one(filter)
        return datax

    def find(self):
        filter = self.data['filter']
        datax = self.collection.find(filter)
        dataA = []
        for x in datax:
            dataA.append(x);
        return dataA

    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find(self.filter)
        print("This is Object: ", documents);
        print("This is Object: ", documents);
        for x in documents:
            print(x);

        output = documents
        # output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output
    
    def readWithFilter(self):
        output = self.mycol.find(self.filter);
        print("This is Output: ",output)
        for x in output:
            print(x)
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data['document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self,data):
        log.info('Updating Data')
        filt = data['filter']
        updated_data = {"$set": data['dataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Deleting Data')
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output


# myclient = MongoClient("mongodb+srv://admin:qrIyd1Nmx6f2Lf3O@cluster0.gwm0k3a.mongodb.net/?retryWrites=true&w=majority")     # When both Mongo and This application is running on

# def MongoFindOne(app, filter):
#     mydb = myclient[app['database']]
#     mycol = mydb[app['collection']]

#     mydoc = mycol.find_one(filter)

#     return mydoc

    

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route('/person' , methods=['GET'])
def readPeron():
    query = xlist(request.args.getlist("query"))
    person_name = xstr(request.args.get("personName"))
    print(query)
    if len(query) == 0:
        return Response(response=json.dumps({"Error": "Please provide correct query"}),
                        status=400,
                        mimetype='application/json');

    if person_name == '':
        return Response(response=json.dumps({"Error": "Please provide Person Name"}),
                        status=400,
                        mimetype='application/json');

    
    person_issued = None
    person_current = None
    person_return = None

    if "issued" in query:
        
        dataParam = {
            "database": "scoutoTranscationDB",
            "collection": "issued",
            "filter": { "person.name": person_name }
        }
        print(dataParam)
        datax = MongoAPI(dataParam).find()
        count = 0
        main = []
        for x in datax:
            main.append({
                'bookName': x['book']['name'],
                'issuedAt': x['issuedAt']
            })
            count = count + 1

        person_issued = {
            "total_count": count,
            "data": main
        }

    if "returned" in query:
    
        dataParam = {
            "database": "scoutoTranscationDB",
            "collection": "issued",
            "filter": { "person.name": person_name, "isReturned": True }
        }
        datax = MongoAPI(dataParam).find()
        count = 0
        main = []
        for x in datax:
            main.append({
                'bookName': x['book']['name'],
                'returnedAt': x['returnedAt']
            })
            count = count + 1

        person_return = {
            "total_count": count,
            "data": main
        }
    

    if "current" in query:
    
        dataParam = {
            "database": "scoutoTranscationDB",
            "collection": "issued",
            "filter": { "person.name": person_name, "isIssued": True }
        }
        datax = MongoAPI(dataParam).find()
        count = 0
        main = []
        for x in datax:
            main.append({
                'bookName': x['book']['name'],
                'issuedAt': x['issuedAt']
            })
            count = count + 1

        person_current = {
            "total_count": count,
            "data": main
        }
    
    answer = {
        "person_current_books": person_current,
        "person_returned_books": person_return,
        "person_issued_books": person_issued
    }
    return Response(response= json.dumps(answer),
                status=200,
                content_type='application/json',
                mimetype='application/json')

@app.route('/book' , methods=['GET'])
def readBook():
    query = xlist(request.args.getlist("query"))
    book_name = xstr(request.args.get("bookName"))
    print(query)
    if len(query) == 0:
        return Response(response=json.dumps({"Error": "Please provide correct query"}),
                        status=400,
                        mimetype='application/json');
    if book_name == '':
        return Response(response=json.dumps({"Error": "Please provide Person Name"}),
                        status=400,
                        mimetype='application/json');
    response = {}
    pep_issued = None
    pep_current = None

    if "pepissued" in query:
        
        dataParam = {
            "database": "scoutoTranscationDB",
            "collection": "issued",
            "filter": { "book.name": book_name }
        }
        print(dataParam)
        datax = MongoAPI(dataParam).find()
        count = 0
        main = []
        for x in datax:
            main.append({
                x['person']['name']: x['book']['name'],
                'issuedAt': x['issuedAt']
            })
            count = count + 1

        pep_issued = {
            "total_count": count,
            "data": main
        }
    

    if "pepcurrent" in query:
    
        dataParam = {
            "database": "scoutoTranscationDB",
            "collection": "issued",
            "filter": { "book.name": book_name, "isIssued": True }
        }
        print(dataParam)
        datax = MongoAPI(dataParam).find()
        count = 0
        main = []
        for x in datax:
            main.append({
                x['person']['name']: x['book']['name'],
                'issuedAt': x['issuedAt']
            })
            count = count + 1

        pep_current = {
            "total_count": count,
            "data": main
        }
    
    answer = {
        "pep_issued": pep_issued,
        "pep_current": pep_current
    }
    return Response(response= json.dumps(answer),
                status=200,
                content_type='application/json',
                mimetype='application/json')

# @app.route('/rent' , methods=['GET'])
# def rent():


@app.route('/books', methods=['GET'])
def readManyBook():
    query_name = xstr(request.args.get("name"))
    query_category = xstr(request.args.get("category"))
    query_rentPerDay = xnum(request.args.get("rent"))
    query_minRentPerDay = xnum(request.args.get("rentMin"))
    query_maxRentPerDay = xnum(request.args.get("rentMax"))

    if(query_rentPerDay ==0 and query_maxRentPerDay==0 and query_minRentPerDay==0):
        query_minRentPerDay = -6143
        query_maxRentPerDay = 6144

    if(query_rentPerDay>0 and query_minRentPerDay == 0):
        query_minRentPerDay = query_rentPerDay

    if(query_maxRentPerDay == 0 and query_minRentPerDay == 0):
        query_minRentPerDay = query_rentPerDay-1
        query_maxRentPerDay = query_rentPerDay+1

    if(query_minRentPerDay == 0  and query_maxRentPerDay > 0):
        query_maxRentPerDay = query_maxRentPerDay + 1
        query_minRentPerDay = -6143

    if(query_minRentPerDay > 0  and query_maxRentPerDay == 0):
        query_maxRentPerDay = 6144
        query_minRentPerDay = query_minRentPerDay - 1

    


    print(query_name,query_category)
    query = {
        "name": { "$regex": query_name },
        "category": { "$regex": query_category},
        "rentPerDay": { "$gt": query_minRentPerDay, "$lt": query_maxRentPerDay},
        }
    print(query)
    dataParam = {
        "database": "scoutoBookDB",
        "collection": "books",
        "filter": query
    }
    dataX = MongoAPI(dataParam).find();
    dataZ = parse_json(dataX)
    print("Data: ", parse_json(dataX));
    return Response(response= json.dumps(dataZ),
                    status=200,
                    content_type='application/json',
                    mimetype='application/json')



@app.route('/book/issue', methods=['POST'])
def issueBook():
    person_name = xstr(request.args.get("personName"))
    book_name = xstr(request.args.get("bookName"))
    book_id = xstr(request.args.get("bookId"))

    if(book_name == ''):
            return Response(response= {"message":"Enter Name of the Book!"},
                    status=400,
                    content_type='application/json',
                    mimetype='application/json')
    
    if(person_name == ''):
            return Response(response= {"message":"Enter Person Name to Issue the Book!"},
                    status=400,
                    content_type='application/json',
                    mimetype='application/json')

    book = {}
  
    dataParam = {
        "database": "scoutoTranscationDB",
        "collection": "issued",
        "filter": { "book.name": book_name, "person.name": person_name}
    }
    issuedBook = MongoAPI(dataParam).findOne();
    print("ISSE ", issuedBook)

    if issuedBook is not None and issuedBook['isIssued'] == True:
        return Response(response= json.dumps({"message":"Book Already Issued!"}),
                status=400,
                content_type='application/json',
                mimetype='application/json')

    dataParam = {
        "database": "scoutoBookDB",
        "collection": "books",
        "filter": { "name": book_name}
    }
    book = MongoAPI(dataParam).findOne()

    if book is None:
        return Response(response= json.dumps({"message":"Incorrect Book!! Search /books [GET] to list all the books."}),
                    status=400,
                    content_type='application/json',
                    mimetype='application/json')

    dataParam = {
        "database": "scoutoTranscationDB",
        "collection": "issued"
    }
    documetData = {
        "document":{
            "isIssued": True,
            "isReturned": False,
            "book": book,
            "person": { "name": person_name},
            "issuedAt": datetime.utcnow(),
            "returnedAt": None,
            "returedTotal": None
        }  
    }
    
    dataX = MongoAPI(dataParam).write(documetData);
    dataZ = parse_json(dataX)
    print("Data: ", parse_json(dataX));
    return Response(response= json.dumps(dataZ),
                    status=200,
                    content_type='application/json',
                    mimetype='application/json')

@app.route('/book/return', methods=['POST'])
def returnBook():
    person_name = xstr(request.args.get("personName"))
    book_name = xstr(request.args.get("bookName"))
    book_id = xstr(request.args.get("bookId"))

    if(book_name == ''):
            return Response(response= json.dumps({"message":"Enter Name of the Book!"}),
                    status=400,
                    content_type='application/json',
                    mimetype='application/json')
    
    if(person_name == ''):
            return Response(response= json.dumps({"message":"Enter Person Name to Return the Book!"}),
                    status=400,
                    content_type='application/json',
                    mimetype='application/json')

    dataParam = {
        "database": "scoutoTranscationDB",
        "collection": "issued",
        "filter": { "isIssued":True, "isReturned": False, "book.name": book_name, "person.name": person_name}}
    
    issuedBook = MongoAPI(dataParam).findOne()
    print(issuedBook)
    if issuedBook is None:
        return Response(response= json.dumps({"message":"No Issued Book Found!!"}),
                    status=404,
                    content_type='application/json',
                    mimetype='application/json')
    
    if issuedBook['isReturned'] == True:
        return Response(response= json.dumps({"message":"Book already Returned!"}),
                    status=404,
                    content_type='application/json',
                    mimetype='application/json')

    dataParam = {
        "database": "scoutoTranscationDB",
        "collection": "issued"
    }

    endtime = datetime.utcnow()
    documetData = {
        "filter":{
            "_id": issuedBook['_id']
        },
        "dataToBeUpdated":{
            "isIssued": False,
            "isReturned": True,
            "returnedAt": endtime,
            "returedTotal": None
        }  
    }
    
    dataX = MongoAPI(dataParam).update(documetData);
    dataZ = parse_json(dataX)
    print("Data: ", parse_json(dataX));

    dataZen = MongoAPI({
        "database": "scoutoTranscationDB",
        "collection": "issued",
        "filter": { "_id": issuedBook['_id'] }
    }).findOne();



    return Response(response= json.dumps(dataZen),
                    status=200,
                    content_type='application/json',
                    mimetype='application/json')





if __name__ == '__main__':
    app.run(debug=True, threaded=True)
