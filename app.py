# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:00:59 2022

@author: Jit
"""


from abc import ABC, abstractmethod
import json 
from flask import request, jsonify, Flask



app = Flask(__name__)
app.config["DEBUG"] = True


Customer = [
    {'customer_id': 0,
     'name': 'Pj',
     'pet_name': 'Seal hunter',
     'pet_type': 'Otter',
     'last_visit_was_for': 'Castration'},
    {'customer_id': 1,
     'name': 'Ahmed',
     'pet_name': 'Mac',
     'pet_type': 'Tortoise',
     'last_visit_was_for': 'Being slow even for a tortoise'},
    {'customer_id': 2,
     'name': 'Gareth',
     'pet_name': 'Captain Jazzy Pants',
     'pet_type': 'Cat',
     'last_visit_was_for': 'Dog bite'}
]





#Vet - staff members - (attributes) name, age, job role : (methods) get name, get age, get job role
#Treat animal (going to take in an animal, and staff member) - examine, treat wounds, surgery, x-ray 


class Animal(ABC):

    #Attributes
    

    #Constructors
    def __init__(self):
        self.value = "Animal"


    #Methods
    

    @abstractmethod
    def eat(self):
        pass


    
    def sleep(self):
        print("I am sleeping")

    def type(self):
        print(self.value)



        
class Tortoise(Animal):
    
    def __init__(self, animal_id, pet_name, owner):
        self.animal_id = animal_id
        self.value = "Tortoise"
        self.pet_name = pet_name
        self.owner = owner
        
    #Methods
    def type(self):
        return(self.value)

    def pet_name(self):
        return(self.pet_name)

    def eat(self):
        print("I eat leaves")


class Hedgehog(Animal):
    
    def __init__(self, animal_id, pet_name, owner):
        self.animal_id = animal_id
        self.value = "Hedgehog"
        self.pet_name = pet_name
        self.owner = owner
        
    #Methods
    def type(self):
        return(self.value)

    def pet_name(self):
        return(self.pet_name)

    def eat(self):
        print("I eat leaves")



class Cat(Animal):
    #Attributes
    #Constructors
    def __init__(self, animal_id, pet_name, owner):
        self.animal_id = animal_id
        self.value = "Cat"
        self.pet_name = pet_name
        self.owner = owner

    #Methods
    def type(self):
        return(self.value)

    def pet_name(self):
        return(self.pet_name)


    def eat(self):
        print("I eat mice")        


class Customer(ABC):
    
    
    def __init__(self, customer_id, name, age):
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.pets = []
        

    def display_name(self):
        print("The name of the customer is: ", self.name)
        
    def display_age(self):
        print("This is the age of the customer: ", self.age)

    def add_pet(self, animal):
        Animal_type = (animal.type())
        Animal_name = (animal.pet_name)
        Animal_details = (Animal_type + "," + Animal_name)
        self.pets.append(Animal_details)

        
    def display_pet_names(self,animal):
        for animals in self.pets:
            print(animals + "\n")
            

        



my_cat = Cat(1, "Gooner", "Pj")
other_cat = Cat(2, "Arteta", "Gareth")
tortoise1 = Tortoise(3, "Flash", "Jay")
hedgehog1 = Hedgehog(4, "Spikey", "Gareth")



Pj = Customer(1, "Pj", 22)
Gareth = Customer(2, "Gareth", 30)
Jay = Customer(3, "Jay", 35)


Pj.add_pet(my_cat)
Gareth.add_pet(other_cat)
Jay.add_pet(tortoise1)
Gareth.add_pet(hedgehog1)


customerdict1 = Pj.__dict__
customerdict2 = Gareth.__dict__
customerdict3 = Jay.__dict__


animaldict1 = my_cat.__dict__
animaldict2 = other_cat.__dict__
animaldict3 = tortoise1.__dict__
animaldict4 = hedgehog1.__dict__




#customer and animal is in dictionary form - these lists contain all of the customer and animal/pet objects
#I do this by appending the customer dictionaries into the relevant lists
customer = []
customer.append(customerdict1)
customer.append(customerdict2)
customer.append(customerdict3)

animal = []
animal.append(animaldict1)
animal.append(animaldict2)
animal.append(animaldict3)
animal.append(animaldict4)


@app.route('/', methods=['GET'])    #tell which HTTP method we are using (GET) and what route (extra bit of the URL) this method will be activated on.  In this case nothing and so home
def home():
    
    title= "<h1>Welcome To My Vet App</h1><p>Created by Prabhjit Sehra</p>" #what the api returns
    return title

# A route to return all of the available entries in our collection of pet owners.
@app.route('/api/somearea/animal/all', methods=['GET'])
def api_all():
    try:
        #json.dumps method converts a python object (in our case the dictionary) into a JSON object
        #all_data will now be equal to the json format of all animals that have been created or used in the vet
        all_data = json.dumps(animal)
        #as it is already in json form, I do not need to jsonify it, hence the reason I have just returned it as all_data
        return (all_data)
    except:
        return("Inputted incorrect URL")

# A route to return all of the available entries in our collection of pets associated to the vet.
@app.route('/api/somearea/vetcustomers/all', methods=['GET'])
def api_all_pet():

    #this does the same as api_all, where instead of going through all of the animals in the vet
    #we go through all of the customers associated with the vet
    all_data = json.dumps(customer)
    return (all_data)


@app.route('/api/somearea/petowner', methods=['GET'])
def get_pets_owned_by_owner():
    
    try:
        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        
        #we check to see if the requested argument is in fact an owner type - this function is looking to retrieve the pets owned by a particular
        #owner, hence why we need to request the owner string from the url
        if 'owner' in request.args:
            #if the user has attempted to obtain an owner from their name, then we the owners name is saved as a string and associated with 
            #the variable owner
            owner = str(request.args['owner'])
        else:
            print("")
#            return "Error: You are an idiot."
    
        # Create an empty list for our results
        results = []
    
        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results    
        
        #we will now for loop through every single animal in the vet, and pet will be equal to this
        for pets in animal:        
            
            #converts the individual pets (in dictionary form) into JSON object
            dictionary = json.dumps(pets)  
        
            #this will then convert the individual pet back into dictionary form from JSON form
            response = json.loads(dictionary)

            #I then look for the owners name of each pet and assign it to owner_name in string format                    
            owner_name = str(pets['owner'])
            
            
            #I think check to see if the pets owner in the full list of pets in the vet is equal to the 
            #owners name the user inputted in the url
            if str(owner_name) == owner:
                
                #return("WORKING")       

                #if this is true, then we know that the pets owner is in fact the one the user is wishing
                #to see all pets for, and we therefore append this pet in dictionary form to the results array
                results.append(pets)
        
            # Use the jsonify function from Flask to convert our list of
            # Python dictionaries to the JSON format.

        #once we have for looped through every single pet, we will now return a jsonify'd version of results
        #which will include all of the pets         
        return jsonify(results)
    except:
        return("You have inputted in incorrect url format. It should be in the form of the local host, followed with /api/somearea/petowner?owner=yourownername")


@app.route('/api/somearea/vetcustomers', methods=['GET'])
def get_owner_by_id():
    
    try:
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
 
        if 'customer_id' in request.args:
            id = str(request.args['customer_id'])
        else:
            print("")
    #        return "Error: You are an idiot."
    
        # Create an empty list for our results
        results = []
    
        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results    
        
        for PetOwner in customer:        
            
            #dictionary = json.dumps(PetOwner)  
                    
            #response = json.loads(dictionary)
            
            customerid = str(PetOwner['customer_id'])
            
            
            if str(customerid) == id:
                
                #return("WORKING")       
                results.append(PetOwner)
        
            # Use the jsonify function from Flask to convert our list of
            # Python dictionaries to the JSON format.
        
        return jsonify(results)
    except:
        return("You have inputted in incorrect url format. It should be in the form of the local host, followed with /api/somearea/vetcustomers?customer_id=yourcustomerid")


    

@app.route('/api/somearea/animal', methods=['GET'])
def get_animal_by_id():
    try:
        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
     
        if 'animal_id' in request.args:
            id = str(request.args['animal_id'])
        else:
            print("")
#            return "Error: You are an idiot."
    
        # Create an empty list for our results
        results = []
    
        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results    
        
        for Pet in animal:        
            
            #dictionary = json.dumps(Pet)  
                    
            #response = json.loads(dictionary)
            
            animalid = str(Pet['animal_id'])
            
            
            if str(animalid) == id:
                
                #return("WORKING")       
                results.append(Pet)
        
            # Use the jsonify function from Flask to convert our list of
            # Python dictionaries to the JSON format.
        
        return jsonify(results)
    except:
        return("You have inputted in incorrect url format. It should be in the form of the local host, followed with /api/somearea/animal?animal_id=youranimalid")
   
    

if __name__ == '__main__':
    app.run()

