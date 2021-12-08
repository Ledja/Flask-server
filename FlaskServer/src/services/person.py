import json
from pathlib import Path


data_folder = Path("src/data/")
data_file_name = data_folder/"people.json" 

class PersonService():

    @staticmethod
    def readJsonFile():
        data = json.loads(open(data_file_name, 'r').read())
        return data

    @staticmethod
    def writeJsonFile(new_data):
        with open(data_file_name, 'w', encoding="utf-8") as file:
            print(new_data)
            json.dump(new_data, file)



    def create_person_api(self,name,age):
        data = self.readJsonFile()      
        
        avaliable_ids = [ int(x['id']) for x in  data['people']]
        new_id = len(avaliable_ids)+1
        record = {
            "id"    : new_id,
            "name"  : name,
            "age"   : age
        }
        data['people'].append(record) 
        self.writeJsonFile(new_data=data) 
        return record
    
    def get_person_by_id_api(self,id):
        data = self.readJsonFile()
        all_persons =data['people']
        for person in all_persons:
            if person['id'] == id:
                res=person        
        return res
        
        
    def get_all_available_ids_api(self):  
        data = self.readJsonFile()
        all_people =data['people']
        res = []
        for person in all_people:
            res.append(person['id'])
        return res




