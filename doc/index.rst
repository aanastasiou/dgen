.. DGen documentation master file, created by
   sphinx-quickstart on Thu Apr 20 00:43:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DGen's documentation!
================================

DGen is an object oriented approach to GENeration and DeGENeration 
of clinical data in various serialisation formats.

The generation of synthetic data is a topical subject for clinical 
research as it offers ways to stress-test systems, test algorithms in 
the presence of known data and of course for training and educational 
purposes. 

The generation of synthetic data is characterised by two competing 
specifications: Data should be generated according to pre-specified 
rules and Data should be realistic. 

The impact of these two competing specifications is high for 
educational purposes as, it is desirable to train students over 
known, simple test-cases but not so simple as to be obvious and 
"text-book" examples.

A number of tools (and techniques) for the generation of artificial data 
in general and clinical data in particular already exist at various 
levels of complexity in installing, seting up and operating them.

DGen attempts to address the problem of generating artificial 
clinical data, of realistic complexity, by a framework of elementary 
Data Generators and Pertubators. Generators are responsible for 
creating random variables with full control over the characteristics 
of their values and Pertubators are responsible for applying commonly 
encountered errors such as punctuation, abbreviation, data omission 
and others to the generated values. 

DGen uses operator overloading to define a very simple "algebra" of 
combining generators to form complex cases (such as conditionally 
probable ones) and generalisation to create more complex entities such 
as "Patient", "CasePatient", "ControlPatient" and others.

DGen is written in Python and is by no means complete. 

Future work includes improving the way random variables are described 
and formalising the transformation to specific data formats via the use 
of Renderers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   moduleDoc
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
