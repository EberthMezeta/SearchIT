# ntlk-synonym-api
Python rest API to get word synonyms in english or spanish

# How to run
Open a terminal on the directory containing the repository files and run
* docker build --tag synonym:1 .
* docker run --name synonym-api -p 8091:8091 -d synonym:1 


# Cleaning up
* docker rm -f synonym-api
* docker images rm synonym:1


#Other synonym api

http://sesat.fdi.ucm.es:8080/servicios/rest/sinonimos/json/arbol