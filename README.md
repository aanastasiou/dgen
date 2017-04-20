# DGen

DGen is a Python module for the generation (and degeneration) of synthetic 
clinical data.

It achieves this by establishing a very basic algebra of random data generators
(and degenerators) and enabling the user to create more complex re-usable and "replugable"
data generators via inheritance.

To an extent, the syntax and overall design of DGen was influenced by [PyParsing](http://pyparsing.wikispaces.com/),
the Python module that enables its users to build parsers.

Just as a PyParsing parser is a model for the strings it can recognise, 
so is DGen, a model of *patient data*. 

In fact, DGen ships with a very basic `Person` model, that represents basic 
data most commonly encountered in epidemiology. DGen users can extend this 
`Person` to create more complex participants with data representing their 
[*Book Of Life*](https://books.google.co.uk/books?id=1iI5rHtCT-4C&lpg=PA180&ots=2kMSde3-kq&dq=%22book%20of%20life%22%20epidemiology&pg=PA180#v=onepage&q=%22book%20of%20life%22%20epidemiology&f=false) events.

## Quickstart
This quickstart covers the two basic packages of DGen:

1. Data Generators
2. Data Perturbators

###Data Generation
To create a fictional postcode variable that conforms loosely to the UK
standard of postcodes:

    from DGen.datagenerator import *
    
    postCode = revRegexGenerator("[A-Z][A-Z][1-9][1-9][A-Z][A-Z]").setVarName("Postcode")
    postCode()
    
Note at this point, `postCode` is **NOT** the instance of a postcode but rather, 
a **model** for postcodes that are composed of 2 letters 2 numbers 2 letters.

To obtain **an instance** of the model, the model is simply *called* (`postCode()`).

#### Other Generators

At the moment, the following generators have been defined:

* `optionGenerator`
    * `P = optionGenerator(["Male", "Female"]) # Generates strings Male, Female with equal probabilities`
    * `P = optionGenerator([(0.1,"Male"),(0.9,"Female")]) # Attaches a discrete probability to each event`

* `condProbOptionGenerator`
    * `P = condProbOptionGenerator({"Male":"Victor", "Female":"Victoria"}) #Given the gender, generate a name`
        * *Note*, the specific mechanics of this generator will become apparent further below
        
* `archivedOptionGenerator`
    * Exactly like an `optionGenerator` but reads options from an archive.
    
* `revRegexGenerator`
    * `P = revRegexGenerator("[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]") # Generates a random 6-digit number in hex`
    * *Note:* Reverse Regular Expressions provided by the excellent Python module [`rstr`](https://pypi.python.org/pypi/rstr/2.1.3).

* `uidGenerator`
    * `P = uidGenerator() # Generates universal identifiers`
    * *Note:* Essentially a repackaging of the excellent [uuid](https://docs.python.org/2/library/uuid.html) module.
    
* `seqGenerator`
    * `P = seqGenerator("ABCD*EFG", maxNum=8) # Generates a sequence or length 8 given an iterable of options`

* `dateGenerator`
    * `P = dateGenerator(datetime.datetime.now()-datetime.timeinterval(weeks=4), datetime.datetime.now()) # Generates a date within the last four weeks`
    
#### Combining generators
All of the above generators can also be combined with each other, either 
as parameters to other generators or through the use of operator overloading. 

For example:

`P = optionGenerator([optionGenerator(["A","B"]), revRegexGenerator("[0-9][0-9]")])`

`P` is now a model which will generate **either** (**A** or **B**) or a number between 0-99.

To generate the cartesian product between sets `U = {"Male", "Female"}` and `V = {"Prostate", "Pregnant"}` with 
specific probabilities, we might define something like:

    P = optionGenerator(["Male","Female"]).setVarName("Gender")
    Q = optionGenerator(["Prostate", "Pregnant"]).setVarName("Condition")
    K = (P * Q).setVarName("GenderCondition")
    
`K` is now a model, a composite data generator, that was created through the multiplication 
operator. It will generate all possible combinations with equal chances, so:
`("MaleProstate", "MalePregnant", "FemaleProstate", "FemalePregnant")`. There are 4 events
and therefore 0.25 probability assigned to each. The probabilities can be altered by using 
the tuple syntax of `optionGenerator`'s constructor.

Obviously, persons of a male gender at birth are more likely to suffer from 
a prostate related condition and similarly, persons of a female gender at birth
are more likely to become pregnant.

To represent this properly, we need a conditional generator, like this:

    P = optionGenerator(["Male","Female"]).setVarName("Gender")
    Q = condProbOptionGenerator({"Male":optionGenerator("Prostate", "Hairloss"), "Female":optionGenerator("Pregnant", "Menustration")})
    K = (Q | P).setVarName("GenderCondition")
    
`K` is now a model that represents the conditional probability of **Q given P**.

In this case, the final generator creates the eventualities:
`("MaleProstate", "MaleHairloss", "FemalePregnancy", "FemaleMenstruation")`

The difference between the cartesian product and conditional probability generator options
is that between a [Klique](https://en.wikipedia.org/wiki/Klique) and a [Tree](https://en.wikipedia.org/wiki/Tree_(graph_theory)).

Finally, data generators can be *XORed" together:

    P = optionGenerator(["Alpha", "Beta"])
    Q = optionGenerator(["Gamma", "Delta"])
    K = (P^Q).setVarName("Combined")
    
`K` is now a model that creates the eventualities of `P XOR Q` or more 
generally, `P1 XOR P2 XOR P3 . . . Pn`.


### Data Degeneration
Similarly to the above examples, let's create a fictional postcode variable 
that suffers from punctuation errors:

    from DGen.datagenerator import *
    from DGen.dataperturbator import *
    
    postCode = revRegexGenerator("[A-Z][A-Z][1-9][1-9][A-Z][A-Z]").setVarName("Postcode")
    postCodeDemon = punctuationPerturbator(prob = 0.8)
    
    P = postCode()
    Q = postCodeDemon(P)
    
In the above example, `P` is a pristine **instance** of a postcode but `Q` is a 
perturbed version of `P` suffering a punctuation error.

The common element of all perturbators is a *probability of occurence* parameter 
which determines how often is the error supposed to appear. In this example, `prob = 0.8` 
which means that in 100 generated instances of `postCode`, 80% of them would appear 
to suffer a punctuation error.

For more information on the specific data perturbation scenarios modeled by DGen, 
please see [Linking Data for Health Services Research: A Framework and Instructional Guide](https://www.ncbi.nlm.nih.gov/books/NBK253312/).

#### Other Degenerators

At the moment, the following degenerators have been defined:

* `subsPerturbator`
    * `P = subsPerturbator([("Avenue", "Avn"),("Robert", "Bob"),("William", "Bill")]) #When triggered, substitutes (from,to)`

* `prefixPerturbator`
    * `P = prefixPerturbator(["Mr", "Sir", "Dr", "Baron"]) #When triggered, adds one of the prefixes to its output`
    
* `suffixPerturbator`
    * Self explanatory, given the operation of `prefixPerturbator`

* `missingDataPerturbator`
    * `P = missingDataPerturbator("-") #When triggered, outputs a predefined missing data symbol to its output.`

## Creating more complex data generators
To create more complex data geneartors, one generally derives from `randomDataGenerator`, the abstract class 
that defines all behaviour expected by a data generator. However, it is up to the user of DGen to further refine 
the algebra of derived `randomDataGenerator`s.

A very simple example of this is the `Person` class, available from `epi` and a more extensive 
example of how DGen can be used to piece together more complex generators is available in the `examples/` folder.


## Where to go from here
The module is extensively documented in `doc/`, including a draft TODO list.
