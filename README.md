# text-annotator

## Setup

- [Install Gramex 1.x](https://learn.gramener.com/guide/install/)
- Clone this repository
- Copy assets from shared repo, e.g. `demo.gramener.com:/deploy/<user>/<repo>/`
- From the repo folder, run `gramex setup .`
- From the repo folder, run `gramex`


Needs python 3
Needs a datasets.db sqlitedb in the root directory with the following structure 
`CREATE TABLE datasets(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, url TEXT, query TEXT, engine TEXT);`
 


 ## Rough Ideas of how it should work
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

- TODO support LazyNLP as a part of a set of data collection utilities

--
 /home
 - Normal user logs onto server
 - logs in with github id
 - gets a series of annotations possible. 

--
/export
- form, puts in threshold values and starts a download. 




## Contributions

- karmanya.aggarwal <karmanya.aggarwal@gramener.com>
