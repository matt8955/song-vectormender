# song-vectormender

Final project for my data science program at Flatiron School, New York City.
The project's goal was to create an artist recommendation engine using just playlist information to discover song similarity



# Data Collection

* Scraped Twitter for publicly tweeted spotify playlists
* Collected song ids for all playlists with Spotify's Api
* Collected artist and song information from Spotify's Api


# Data Cleaning

* removed all playlists that had the same Artist over 75% of the time
* removed all artists that did not appear over 100 times total 

# Model

* Used Word2Vec to create word embeddings to create vector space of all artists on the playlists
* Made reccomendations based on nearest neighbor of artist or average vector of multiple artist selections of the user

# Usage

run the following from the dash_app directory and direct your browser to the given web address in your command line

`python app.py`

or try the deployed version on heroku

https://song-vectomender.herokuapp.com/
