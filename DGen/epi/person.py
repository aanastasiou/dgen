# -*- coding: utf-8 -*-
"""Defines a very simple skeleton of an object oriented hierarchy for 
generating case-control clinical data

Athanasios Anastasiou April 2017
"""

from ..datagenerator import *
from utils import *

class PersonData(randomDataGenerator):
    """Defines an abstract class for a person's data.
    
    Person data can be primary care or secondary care or define a further
    hierarchy of 'data catalogues' to contain various different types"""
    def __init__(self):
        self._data = []
        
    def __call__(self):
        return self._data
    
class Person(randomDataGenerator):
    """Defines an abstract class for a Person.
    
       This class abstracts an individual in a population and 
       initialises it with a number of attributes that are commonly encountered in Epidemiology"""
    
    def __init__(self, ageMin=18, ageMax=65, *args, **kwargs):
        super(Person, self).__init__()
        
        self._ageMin = ageMin
        self._ageMax = ageMax
                    
        #Demographic data
        self._Identifier = uidGenerator().setVarName("PATID")
        self._Surname = optionGenerator(Surnames).setVarName("Surname")
        self._Name = condProbOptionGenerator({'male':optionGenerator(maleNames), 'female':optionGenerator(femaleNames)}).setVarName("Name")        
        self._DOB = dateGenerator(datetime.datetime(year = datetime.datetime.now().year-self._ageMax, month = 01, day = 01),datetime.datetime(year = datetime.datetime.now().year - self._ageMin, month = 12, day = 31)).setVarName("DOB")
        self._Gender = optionGenerator(['male','female']).setVarName("Gender")
        self._Address = (revRegexGenerator("([1-9]|([1-9][0-9]?[0-9]?)) ") * optionGenerator(StreetNames)).setVarName("Address")
        self._Postcode = revRegexGenerator("[A-Z][A-Z][1-9][1-9][A-Z][A-Z]").setVarName("Postcode")
        self._GPID = revRegexGenerator("[A-Z][0-9][0-9][0-9][0-9][0-9]").setVarName("GPID")
        self._Data = PersonData().setVarName("Data")
        
    def __call__(self):
        """Generates and returns an instance of a Person"""
        gnd = self._Gender()
        nme = self._Name(gnd)
        idf = self._Identifier()
        dob = self._DOB()
        srn = self._Surname()
        adr = self._Address()
        pcd = self._Postcode()
        gpd = self._GPID()
        dta = self._Data()
        return Bunch({self._Identifier.name:idf,                 
                self._Name.name:nme, 
                self._Surname.name:srn,
                self._Gender.name:gnd, 
                self._DOB.name:dob,
                self._Address.name:adr,
                self._Postcode.name:pcd,
                self._GPID.name:gpd,
                self._Data.name:dta})                
               
class DiseasePersonData(PersonData):
    """Defines the way a disease manifests in a patient data"""
    def __call__(self):
        return []
    
class DiseasePerson(Person):
    """Defines the characteristics of a person under disease.
    
    A person under disease might require additional characteristics to 
    those already defined in Person."""    
    def __init__(self, ageMin, ageMax):
        super(DiseasedPerson,self).__init__(ageMin, ageMax)
        
    def __call__(self):
        somePerson = super(DiseasedPerson,self).__call__()
        somePerson['Data'] = DiseasePersonData()()
        return somePerson
        
class ControlPersonData(PersonData):
    """Defines the way 'normality' would manifest itself in patient data"""
    def __call__(self):
        return []
    
class ControlPerson(Person):
    """Defines the characteristics of a control person."""    
    def __init__(self, ageMin, ageMax):
        super(ControlPerson,self).__init__(ageMin, ageMax)
        
    def __call__(self):
        somePerson = super(ControlPerson,self).__call__()
        somePerson['Data'] = ControlPersonData()()
        return somePerson        
