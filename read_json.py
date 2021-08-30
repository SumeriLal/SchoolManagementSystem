import json 
  
# Data to be written 
dictionary ={
    "b'8800135FDE1A'":{
                "name" : "Dev Kumar", 
                "rollno" : 561285,
                },
    
    "b'880012E85123'":{
                "name" : "Amit Kumar", 
                "rollno" : 525682, 
                },
    
    "b'880015ABFCCA'":{
                "name" : "Anuj Chudhary", 
                "rollno" : 589578, 
                },
    } 
  
with open("sample.json", "w") as outfile: 
    json.dump(dictionary, outfile) 


# Opening JSON file 
with open('sample.json', 'r') as openfile: 
  
    # Reading from json file 
    json_object = json.load(openfile)
    for x in json_object:
        if(x=="b'880012E85123'"):
            #print(json_object[x])
            y = json_object[x]
            print(y['name'])
            print(y['rollno'])

y = json_object["b'880012E85123'"]
print(y)
#print(json_object) 
#print(type(json_object)) 
