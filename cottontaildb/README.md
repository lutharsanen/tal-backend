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

Cottontail DB is available as Docker Image from [DockerHub](https://hub.docker.com/r/vitrivr/cottontaildb). Please have a look at the repository instructions and/or the [Wiki](https://github.com/vitrivr/cottontaildb/wiki/Setup) for more information.

### Connecting to Cottontail DB

Communication with Cottontail DB is facilitated by [gRPC](https://grpc.io/). By default, the gRPC endpoint runs on **port 1865**. To connect to Cottontail DB, you must first generate the model classes and stubs using the gRPC library of your
preference based on the programming environment you use. You can find the latest gRPC definitions [here](https://github.com/vitrivr/cottontaildb-proto).