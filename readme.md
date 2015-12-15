# Swiss Style Tournaments Planner

This tournament planner is a python module which let you keep track of your swiss style tournament 
registering players, the matches and generate pairs for each round according to the number of 
wins per player and those of his opponent.

## Modules

- `tournament.py`: API for interacting with the swiss style tournaments planner.
- `tournament_test.py`: Automated test suite for the tournaments planner API module.
 
## Database Schema

The schema is defined in the file `tournament.sql` which can be used for setting up 
the database tables and views for future usage.
   
## Setup

### Requirements

- `PostgreSQL`: Database management system for storing players and matches.
- `Python runtime 2.7.x`: Runtime environment for python scripts. 
- `Psycopg2`: PostgreSQL driver for python DB-API. 
- `Bleach`: An easy whitelist based markup sanitizing tool.
 
### Setting up database schema
```
$ psql -f tournament.sql
```

### Testing the tournaments planner API
```
$ python tournament_test.py 
```
