"""
Defines elementary perturbators

The module gathers together a set of perturbators that abstract various
errors that can be found in datasets. For more information on the implemented
use cases for each of these perturbators please see:
https://www.ncbi.nlm.nih.gov/books/NBK253313/

Athanasios Anastasiou Sept 2016
"""
import random

class dataPerturbator(object):
    """Defines the base class for all data perturbators
    
    This is an abstract class and is not expected to be instantiated directly.
    
    Similarly to data generators, data perturbators represent A MODEL of the
    perturbation. 
    
    Data perturbators are callables too (just like data generators) and 
    apply the perturbation they represent to their (usually single) parameter.
    
    A data perturbator has most commonly at least one probability at which 
    it is triggered, in addition to any other parameters.
    
    So, a perturbator with a probability of 0.7 is expected to apply its
    perturbation 70% of the times it is called.
    
    """
    #TODO: Add operator support to perturbators so that they can be pieced together into more complex ones.
    #TODO: Add a function to the perturbator that actually performs the perturbation and call it from within __call__ to reduce having to write the triger code.
    def __init__(self, prob = 1.0):
        """Standard constructor for all data perturbators"""
        self._prob = prob
        
    @property
    def prob(self):
        return prob
        
    @prob.setter
    def prob(self, aValue):
        """Standard setter for the prob property
        
        Sets the value of prob.
        
        Args:
            aValue: A Real value representing the probability at which this perturbator applies its error to the output
        """
        self._prob = aValue
        
    
class punctuationPerturbator(dataPerturbator):
    """Defines a punctuation perturbator.
    
       A punctuation pertubator either:
            Erases a letter
            Swaps two nearby letters (successive positions)
            Changes a letter with a random one
    """        
    def __init__(self, prob = 0.5):
        super(punctuationPerturbator, self).__init__(prob)
        
    def __call__(self, aString):
        if random.random()>self._prob:
            return aString
                                    
        v = random.random()
        lenS = len(aString)        
        #Generate some random position in the string
        k = random.randrange(1,lenS-1)
        if 0.0<v<=0.5:
            #Erase a letter at random        
            return aString[0:k]+aString[k+1:]
            
        if 0.5<v<=1.0:
            #Swap nearby symbols
            return aString[0:k]+aString[k+1]+aString[k]+aString[k+2:]
            
            
class subsPerturbator(dataPerturbator):
    """Defines a substitution perturbator
    
    A substitution perturbator replaces strings.
    
    Examples:
        P = optionGenerator(["Robert", "William", "Richard"])
        Q = subsPerturbator([("Robert", "Bob"), ("William", "Bill"), ("Richard", "Dick")], prob=0.8)
        I = [Q(P()) for k in xrange(0,100)]
        
        The call to Q(P()) will trigger the generation of one of the three names with a probability of 1/3
        and subsequently apply the substitution to 80% of the evaluations in I.
        
    WARNING!!!
        The substitutions are applied **sequentially, by order of appearance**. This means that 
        if Q = subsPerturbator([("Robert", "Bob"),("Bob", "Hoskins")]) and P() 
        generated "Robert", this WILL NOT be mapped automatically to "Hoskins".
        Rather, Robert will map to Bob and upon a second call to Q, Bob will map to Hoskins.
    """
    
    def __init__(self, subsList, prob = 0.5):
        """Instantitates the perturbator
        
        Instantiates the perturbator to the list of substitutions
        
        Args:
            subsList: A list of tuples describing the substitutions
            prob    : A Real number representing the probability of triggering this perturbator
        Returns:
            Nothing
        """
        super(subsPerturbator, self).__init__(prob)
        self._subsList = subsList
        
    def __call__(self, aString):
        if random.random() > self._prob:            
            return aString
                    
        currentString = aString
        for aSub in self._subsList:
            currentString = currentString.replace(aSub[0],aSub[1])
        return currentString
        
class prefixPerturbator(dataPerturbator):
    """Defines a prefix perturbator
    
    A prefix perturbator adds one of a set of prefixes to a string.
    
    Examples:
        P = optionGenerator(["Burroughs", "Kerouac", "Cohen", "Ginsberg"])
        Q = prefixPerturbator(["Mr", "Dr", "Baron", "Sir"])
    
        This will append random titles to the outputs of P
    """
    def __init__(self, listOfPrefixes, prob=0.5):
        """Instantiates a prefix perturbator
        
        Args:
            listOfPrefixes: A list of prefixes (usually strings)
            prob          : A Real number representing the probability at which this perturbator is supposed to trigger.
            
        Returns:
            Nothing
        """
        super(prefixPertubator, self).__init__(prob)
        self._listOfPrefixes = listOfPrefixes
        self._Nprefixes = len(self._listOfPrefixes)
        
    def __call__(self, aString):
        if random.random()>self._prob:
            return aString
        return self._listOfPrefixes[random.randrange(0,self._Nprefixes)] + aString
        
class suffixPerturbator(dataPerturbator):
    """Defines a suffix to a string with a given probability
    
    Please see documentation of prefixPerturbator which is complementary.
    
    Examples:
        P = optionGenerator(["Burroughs", "Kerouac", "Cohen", "Ginsberg"])
        Q = suffixPerturbator(["ing", "ong", ". Jr"])
    """
    def __init__(self, listOfSuffixes, prob=0.5):
        super(suffixPertubator, self).__init__(prob)
        self._listOfSuffixes = listOfSuffixes
        self._Nsuffixes = len(self._listOfSuffixes)
        
    def __call__(self,aString):
        if random.random()>self._prob:
            return aString
        return aString + self._listOfSuffixes[random.randrange(0,self._Nsuffixes)]
        
class missingDataPerturbator(dataPerturbator):
    """Defines a missing data perturbator
    
    A missing data perturbator returns a symbol indicating the missing data condition (e.g. "-", "N/A", etc)
    
    Examples:
        P = optionGenerator(["Male", "Female"])
        Q = missingDataPerturbator("N/A", prob=0.2)
        I = [Q(P()) for k in xrange(0,100)]
        
        This will return "N/A" to 20% of the evaluations within I
    """
    def __init__(self, missingDataSymbol="", prob=0.5):
        """Instantiates the missing data perturbator
        
        Args:
            missingDataSymbol: A string describing the missing data symbol
            prob             : A Real number describing the probability of triggering this perturbator.
        """
        super(missingDataPerturbator, self).__init__(prob)
        self._missingDataSymbol = missingDataSymbol        
    
    def __call__(self,aString):
        if random.random()>self._prob:
            return aString
        return self._missingDataSymbol
