# Container Architecture
THis application has been made to run in multiple environments. One of these is within containers. So tha the aplication can basically run on any environment running a container engine.

The container application takes advantage of the tiangolo/uwsgi-ngin.python3.6 image that's publically available and ready to run Flask based application using NGINX as the web server. This repo already contains a Dockerfile that uses this image and algo contains the following setup in order for the aplication work:

1. SQL Server driver preparation for stabilishing SQL Server connections from Linux.
2. NGINGX reverse proxy and web server configurations and optimizations.


# Containers Build and Run Process
In order for the required container to run, the following steps are required:

1. Login to the server that runs the container engine.
2. Clone this repo into a local folder and cd root of the folder
3. Create the required environmental variables (see the environmental variables section for more details).
4. Fix the path insert routes as required in the python files. Usually, the application routes need to point to the /var/www/app/ folder.
5. Build the main image using the command: docker build -t manning .
6. Run the container application using the command: 
- docker run -d -p 8080:8080 --network=host -it --add-host '' -t manning

Please consider in the commands above:

- The build command is tagging the manning image, which should be eventually used to run the app.
- The run command is making a mapping of multiple hosts to the container. This is required for the container to be able to understand and use these on-prem hosts in the resulting Python code.

After running these commands, the application should be available in the port 8080 in the target network ip address/hostname (for instance the ip address which corresponds to the host where thecontainer engine runs).

Note: If it's required to re-deploy updated code due to new business logic or tweaks to the Docker file, you need to run a docker stop <container-id> && docker rm <container-id> first to stop the existing container, and then run the steps 4-5 described above.


# Enviromental variables
In order for the application to run as a container, it's required to create a specific enviromental variables as folllows.


1. Create a file of name .env in root of folder where the repo was cloned.
2. Fill the values of the enviromental variable as required: 

DATABASE_CONN_STRING="Driver={ODBC Driver 17 for SQL Server};Server='';Database='';UID='';PWD=''"

# Summary commands:
0. Docker ps
1. docker stop <container-id> && docker rm <container-id>
2. clone repo
3. rm -rf mannningUpdated
4. mv Manning manningUpdated
5. change enviromental variables
6. create .env file: DATABASE_CONN_STRING="Driver={ODBC Driver 17 for SQL Server};Server='';Database='';UID=SQLU_Manning;PWD=''"
7. docker build -t manning .
8. docker run -d -p 8080:8080 --network=host -it --add-host '' -t manning


