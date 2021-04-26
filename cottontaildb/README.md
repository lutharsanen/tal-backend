# Cottontail DB

## Setup
Cottontail DB requires Java 11 or newer (Open JDK or Oracle JDK should both work).

### Building and starting Cottontail DB
1. In the .\cottontaildb\bin\bin folder you can find the cottontaildb.bat. Run the batch file and specify where the config file is. I.e. .\cottontaildb\bin\bin\cottontaildb.bat  .\cottontaildb\config.json
CottontailDB is now up and running on localhost port 1865.
2. In order to interact with CottontailDB we use the python client. Run the cottontaildb.py file.
3. The data generated can be found here: .\cottontaildb\bin\bin\cottontaildb-data

#-----------------------------------------------------------------------------------------------------------
### Using Cottontail DB Docker Image

Cottontail DB is available as Docker Image from [DockerHub](https://hub.docker.com/r/vitrivr/cottontaildb).

1. Download Docker Hub for Desktop
2. Pull the docker image via CLI: docker pull vitrivr/cottontaildb
3. Open Windows PS and mount your container with the github repo: docker run -it --name cottontaildb -p 1865:1865 -v "C:\specify\your\path\tal-backend\cottontaildb\cottontaildb-data:/cottontaildb-data" vitrivr/cottontaildb:latest
4. You will see that your container is now running. You can now run the cottontaildb.py file, which serves as a client for the database (perform insertions/queries etc.). All the data will be stored in the folder ".\tal-backend\cottontaildb\cottontaildb-data".