# text-annotator

## Setup

- [Install Gramex 1.x](https://learn.gramener.com/guide/install/)
- Clone this repository
- Copy assets from shared repo, e.g. `demo.gramener.com:/deploy/<user>/<repo>/`
- From the repo folder, run `gramex setup .`
- From the repo folder, run `gramex`


## Userflow.md has a rough direction of where this project should go. 
Needs python 3
Needs a datasets.db sqlitedb in the root directory with the following structure 
`CREATE TABLE datasets(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, url TEXT, query TEXT, engine TEXT);`
 

## Contributions

- karmanya.aggarwal <karmanya.aggarwal@gramener.com>
