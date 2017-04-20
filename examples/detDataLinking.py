# -*- coding: utf-8 -*-
"""Generates four datasets which can be used in assignments related to data linking
Athanasios Anastasiou April 2017
"""

from DGen.datagenerator import *
from DGen.dataperturbator import *
from DGen.epi.person import Person
from DGen.epi.utils import StreetNames
import bunch
import sys

class Participant(Person):
    """Abstracts a participant. Participants can be of any age between parameters
       ageMin, ageMax and have a probability of being dead of probDeath. If the 
       person has died, their date of death will be within 3 months of today's date"""
    def __init__(self, *args, **kwargs):
        """In addition to ageMin, ageMax it also adds probOfDeath"""
        super(Participant, self).__init__(self, *args, **kwargs)
        #Add DeathRecord if dead       
        self._probOfDeath = probOfDeath
        self._deathCertificate = []
         
    def __call__(self):
        '''Returns a possible patient'''
        participantData = super(Participant,self).__call__()
        #If the person has died, add a death certificate
        if random.random()<=self._probOfDeath:
            self._deathCertificate = DeathReg((revRegexGenerator("([1-9]|([1-9][0-9]?[0-9]?)) ") * optionGenerator(StreetNames)).setVarName("Address"), optionGenerator(["Natural causes", "Accidental"]), dateGenerator((datetime.datetime.now()-datetime.timedelta(weeks=96)).replace(microsecond=0), datetime.datetime.now()))
            participantData.update({'DC':self._deathCertificate()})      
        else:
            participantData.update({"DC":[]})
        return participantData

class DeathReg(randomDataGenerator):
    '''Generates a random set of death records'''
    def __init__(self, possibleStreetAddress, possibleCauseOfDeath, possibleDateofDeath):
        '''Initialises a generator with a possible place and cause of death'''
        self._possibleStreetAddress = possibleStreetAddress
        self._possibleCauseOfDeath = possibleCauseOfDeath      
        self._possibleDateOfDeath = possibleDateofDeath
        
    def __call__(self):
        '''Returns a possible cause of death at a possible date'''
        return bunch.Bunch({'ADDRESS':self._possibleStreetAddress(), 'CAUSE':self._possibleCauseOfDeath(), 'DATE':self._possibleDateOfDeath()})
        
class HospitalData(randomDataGenerator):
    '''Generates clinical events associated with secondary care'''
    def __init__(self, possibleHospitals, dateRange, lifeEvents):
        '''Initialises a "timeseries" of life events that is completely parametrisable'''
        self._possibleHospitals = possibleHospitals
        self._dateRange = dateRange
        self._lifeEvents = lifeEvents
                
    def __call__(self):
        return bunch.Bunch({'HOSPID':self._possibleHospitals(), 'EVENT_DATE':self._dateRange(), 'EVENT_CODE':self._lifeEvents()})

class ClinicalData(randomDataGenerator):
    '''Generates clinical events associated with primary care'''
    def __init__(self, lifetimeGPSurgeries, dateRange, lifeEvents, lifeEventData):
        '''Initialises a "timeseries" of life events that is completely parametrisable'''
        self._possibleGPIDs = lifetimeGPSurgeries
        self._lifeEvents = lifeEvents
        self._lifeEventData = lifeEventData
        self._dateRange = dateRange
    
    def __call__(self):
        '''Generates life events based on the parameters passed to this generator at initialisation time'''
        return bunch.Bunch({'GPID':self._possibleGPIDs(), 'EVENT_DATE':self._dateRange(), 'EVENT_CODE':self._lifeEvents(), 'EVENT_DATA':self._lifeEventData()})

class ControlParticipant(Participant):
    '''A data generator that produces sequences of primary and secondary care events for the case of a control participant'''
    def __init__(self, *args, **kwargs):
        '''probOfDeath, NPrimaryCareEvents, NSecondaryCareEvents)'''
        super(ControlParticipant, self).__init__(*args, **kwargs)
        try:
            self._NprimaryCareData = kwargs['NPrimaryCareEvents']
        except KeyError:
            self._NprimaryCareData = 20
            
        try:
            self._NsecondaryCareData = kwargs['NSecondaryCareEvents']
        except KeyError:
            self._NsecondaryCareData = 20
        
    def __call__(self):
        '''Generates the actual data'''
        participantData = super(ControlParticipant, self).__call__()
        #If the person is dead, then their life events should stop 4 weeks before death        
        #TODO: This can be further customised and primary and secondary care event sequences can have different terminaldates so that 
        #persons can be dying at the hospital after complications (for instance)
        if not participantData.DC:
            #If the patient does not have a death certificate, the last date of a health event can well be today
            terminalDate = datetime.datetime.now()
        else:
            #If the patient is dead, then the last date of a health event should be 4 weeks before death.
            terminalDate = (datetime.datetime.strptime(participantData.DC.DATE,"%Y-%m-%d %H:%M:%S") - datetime.timedelta(weeks=4)).replace(microsecond=0)
        self._primaryCareData = ClinicalData(optionGenerator([participantData.GPID, self._GPID(), self._GPID(), self._GPID(), self._GPID()]), dateGenerator(datetime.datetime.strptime(participantData.DOB,"%Y-%m-%d %H:%M:%S"),terminalDate), optionGenerator(["ITX10","QB65", "ABC456"]), optionGenerator(["10","22","55","3.22"]))
        self._secondaryCareData = HospitalData(optionGenerator(["SGH2498753","MST9530622"]),dateGenerator((datetime.datetime.strptime(participantData.DOB,"%Y-%m-%d %H:%M:%S")+datetime.timedelta(weeks=336)).replace(microsecond=0),terminalDate), optionGenerator(["V00.131S", "J11.82", "J44.9", "V15.82", "F41.9"]))
        participantData.update({'PCD':[self._primaryCareData() for k in xrange(0,self._NprimaryCareData)], 'SCD':[self._secondaryCareData() for k in xrange(0,self._NsecondaryCareData)]})
        return participantData
        
class CaseParticipant(ControlParticipant):
    '''Abstracts a custom random data generator that produces sequences of primary and secondary care events for a person with specific observations and findings conforming to a disease'''
    def __init__(self, *args, **kwargs):
        '''Initialises the random data generator'''
        super(CaseParticipant, self).__init__(*args, **kwargs)        
        
    def __call__(self):
        '''Generates the actual data'''
        participantData = super(CaseParticipant, self).__call__()
        #If the person is dead, then their life events should stop 4 weeks before death        
        #TODO: This can be further customised and primary and secondary care event sequences can have different terminaldates so that 
        #persons can be dying at the hospital after complications (for instance)
        if not participantData.DC:
            #If the patient does not have a death certificate, the last date of a health event can well be today
            terminalDate = datetime.datetime.now()
        else:
            #If the patient is dead, then the last date of a health event should be 4 weeks before death.
            terminalDate = (datetime.datetime.strptime(participantData.DC.DATE,"%Y-%m-%d %H:%M:%S") - datetime.timedelta(weeks=4)).replace(microsecond=0)
        self._primaryCareData = ClinicalData(optionGenerator([participantData.GPID, self._GPID(), self._GPID(), self._GPID(), self._GPID()]), dateGenerator(datetime.datetime.strptime(participantData.DOB,"%Y-%m-%d %H:%M:%S"),terminalDate), optionGenerator(["ITX10","QB65", "ABC456"]), optionGenerator(["10","22","55","3.22"]))
        self._secondaryCareData = HospitalData(optionGenerator(["SGH2498753","MST9530622"]),dateGenerator((datetime.datetime.strptime(participantData.DOB,"%Y-%m-%d %H:%M:%S")+datetime.timedelta(weeks=336)).replace(microsecond=0),terminalDate), optionGenerator(["W00.9","W06.XXXA", "W11.XXXA", "W14.XXXA", "W17.2XXA", "W19.XXXA", "F32.9", "G40.909", "C34.00", "C46.51", "D12.8", "I15.9", "I27.0", "F41.9"]))
        participantData.update({'PCD':[self._primaryCareData() for k in xrange(0,self._NprimaryCareData)], 'SCD':[self._secondaryCareData() for k in xrange(0,self._NsecondaryCareData)]})
        return participantData
        
if __name__ == "__main__":
    NPersons = 100 #A population of 100 persons
    NCase = 50 #50 of them should be case persons
    NPCD = 10 #Each with 10 events in primary care
    NSCD = 10 #and 10 events in secondary care
    NControlDead = 20 #5 out of the 50 should be dead
    NCaseDead = 30 #12 out of the 50 should be dead 


    #Generate a dataset
    sys.stdout.write("Generating dataset. . .");    
    #Generate the controls
    ZControl = [ControlParticipant(probOfDeath = NControlDead/float((NPersons-NCase)),NPrimaryCareEvents = NPCD, NSecondaryCareEvents = NSCD)() for k in xrange(0,NPersons-NCase)]
    #Generate the cases
    ZCase = [CaseParticipant(NCaseDead/float(NCase), NPCD, NSCD)() for k in xrange(0,NCase)]
    #Put them together in the same list and randomise their index so that they are mixed
    Z = random.sample(ZControl + ZCase, NPersons)    
    sys.stdout.write("Done\n")
    
    #Split into different tables
    sys.stdout.write("Denormalising. . .")    
    GP_DEM = []
    GP_CLIN = []
    HOSPDAT = []
    DEATHREG = []
    for aPerson in Z:
        GP_DEM.append({'PATID':aPerson.PATID, 'NAME':aPerson.Name, 'SURNAME':aPerson.Surname, 'DOB':aPerson.DOB, 'GENDER':aPerson.Gender, 'ADDRESS':aPerson.Address, 'POSTCODE':aPerson.Postcode, 'GPID':aPerson.GPID})
        for aClinDat in aPerson.PCD:
            GP_CLIN.append({'PATID':aPerson.PATID, 'GPID':aClinDat.GPID, 'EVENT_DATE':aClinDat.EVENT_DATE, 'EVENT_CODE':aClinDat.EVENT_CODE, 'EVENT_DATA':aClinDat.EVENT_DATA})        
        for aHospDat in aPerson.SCD:
            HOSPDAT.append({'PATID':aPerson.PATID, 'HOSPID':aHospDat.HOSPID, 'EVENT_DATE':aHospDat.EVENT_DATE, 'EVENT_CODE':aHospDat.EVENT_CODE})            
        if aPerson.DC:
            DEATHREG.append({'PATID':aPerson.PATID, 'NAME':aPerson.Name, 'SURNAME':aPerson.Surname, 'DOB':aPerson.DOB, 'GENDER':aPerson.Gender, 'ADDRESS':aPerson.Address, 'POSTCODE':aPerson.Postcode, 'DOD':aPerson.DC.DATE, 'CAUSE':aPerson.DC.CAUSE})
    #Data pertubation
    sys.stdout.write("Done\n")               
    sys.stdout.write("Perturbing data fields. . .")
    #Perturbing just the death registry here
    for aDeadPerson in DEATHREG:
        aDeadPerson['CAUSE'] = missingDataPerturbator(prob=0.1)(aDeadPerson['CAUSE'])        
        aDeadPerson['PATID'] = punctuationPerturbator(prob=0.8)(aDeadPerson['PATID'])        
        aDeadPerson['ADDRESS'] = subsPerturbator([('Street','St.'),('Avenue', 'Avn'), ('Drive','Drv'), ('Road','Rd')],0.6)(aDeadPerson['ADDRESS'])        
    sys.stdout.write("Done\n")               
    #Save everything to the disk
    sys.stdout.write("Saving to disk. . .")
    pandas.DataFrame.from_dict(GP_DEM).to_csv("GP_DEM.csv", index = False)
    pandas.DataFrame.from_dict(GP_CLIN).to_csv("GP_CLIN.csv", index = False)
    pandas.DataFrame.from_dict(HOSPDAT).to_csv("HOSPDAT.csv", index = False)
    pandas.DataFrame.from_dict(DEATHREG).to_csv("DEATHREG.csv", index = False)
    sys.stdout.write("Done\n")
