# User Flow

- Dataset creator downloads this repo - 
- Creates a .yaml file and puts the dataset there
    - Fields/Params:
    - Anotation column Name
    - Possible Values for Annotation. 
    - data file name/path
    - github url for a repo(optional)
    - test
- after dataset creation, he runs the server. 
- Server on startup, does the following :
    - read through datasets folder and for every dataset ensure that 3 tables exist. 
    - if they don't exist, create them. 
    - Inserts dataset into one the tables created. 
    - TODO: Add support for delta inserts

--
 /home
 - Normal user logs onto server
 - logs in with github id
 - gets a series of annotations possible. 

--
/export
- form, puts in threshold values and starts a download. 


