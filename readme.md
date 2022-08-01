## 1 CLONE THE PROJECT

-> ```https://github.com/fabriciogl/hexagoon.space.git```

## 2 POETRY

--> Having python 3.10 installed, use ``` pip install poetry ```

## 3 INSTALL PACKAGES

--> Inside the root app folder run ``` poetry install ```

## 4 SECRETS

--> create a ```.secrets.toml``` file with the following content inside the root folder, replacing the password for each enviroment:

--> replace the values with your own settings  
--> ``` [default] ``` is mandatory, even if you don't use as an environment.    
--> ``` [production] [development] [testing] ``` are used when necessary  

<code>
[default]<br/>
root_pass = "cookies" <br/>
db_pass = "secret" <br/>
dns = "oracleService" <br/>
jwt_hash = "longHash" <br/>
jwt_algo = "HS256" <br/>
root_user = "" <br/>
root_email = "" <br/>
root_role = "root" <br/>
db_driver = "" <br/>
db_user = "" <br/>
db_address = "" <br/>
[production] <br/> 
root_pass = "cookies" <br/>
db_pass = "secret" <br/>
dns = "oracleService"  <br/>
jwt_hash = "longHash" <br/>
jwt_algo = "HS256" <br/>
root_user = "" <br/>
root_email = "" <br/>
root_role = "root" <br/>
db_driver = "" <br/>
db_user = "" <br/>
db_address = "" <br/>
[development] <br/>
root_pass = "cookies" <br/>
db_pass = "secret" <br/>
dns = "oracleService"  <br/>
jwt_hash = "longHash" <br/>
jwt_algo = "HS256" <br/>
root_user = "" <br/>
root_email = "" <br/>
root_role = "root" <br/>
db_driver = "" <br/>
db_user = "" <br/>
db_address = "" <br/>
[testing] <br/>
root_pass = "cookies" <br/>
db_pass = "secret" <br/>
dns = "oracleService"  <br/>
jwt_hash = "longHash" <br/>
jwt_algo = "HS256" <br/>
root_user = "" <br/>
root_email = "" <br/>
root_role = "root" <br/>
db_driver = "" <br/>
db_user = "" <br/>
db_address = "" <br/>
</code>

## 5 ORACLE DB CONTAINER

--> build a image from oracle database following the instruction from 
https://github.com/oracle/docker-images/blob/main/OracleDatabase/SingleInstance/README.md  
--> Basically  (Linux instructions)  
- a) ``` git clone https://github.com/oracle/docker-images.git```  
- b) download the binaries from your desired version of Oracle DB direct from their site. Always choose Linux version, even if you are running docker on Windows or Mac. Remember, the container has his own Operational System, in general Linux.  
- c) Save the binaries inside ``` OracleDatabase/SingleInstance/dockerfiles/versionChosen``` (I used 19.3.0)  
- d) execute ```./buildContainerImage.sh -h``` inside dockerfiles folder. If everything goes right at end you will have an Oracle Database Image.  
- e) run the image with docker ``` docker run ``` and all the variables needed, as instructed in the README link above.  
- f) download the instant client from Oracle site (this one need to be according to yours OS LINUX/MAC/WINDOWS).  
- g) unzip it inside this project at root folder and pass the environment variable ```LD_LIBRARY_PATH``` pointing to the directory.  
***Ex. If you placed the zip files at folder ```hexagoon\oracle_client``` you will need to pass as environment variable ```LD_LIBRARY_PATH=oracle_client```***  
***If you are having issues importing the files from oracle pass a helper environment variable ```DPI_DEBUG_LEVEL=64``` to see what is happening during the file imports.***

- h) (Very Important): complete the ```db_user```, ```db_pass``` and ```db_address``` at the ```.secret.toml``` created at step 4.  
--> ```db_adress``` will be like ```system/<your password>@//localhost:1521/<your SID>```  
***If you don´t have a connections using ```localhost```, use the IP from ```Docker0``` instead. Check the IP from ```Docker0``` using ```ifconfig``` at the terminal.***

## 7 PASS THE ENVIRONMENT 

--> If using Pycharm, create a server run/debug configuration and add following variables to env through "Edit Configurations" 

    - ENV_FOR_DYNACONF=development;

--> same if running the code from terminal or VS (add the ENV_FOR_DYNACONF variable to environment).

## 8 RUN THE APPLICATION

--> run aplication on Pycharm at the upper right options, correct the working directory to the root (hexagoon)  
--> highly recommend to use an IDE (Pycharm/VS) to code and debug, but you can run it from terminal with:  
```DPI_DEBUG_LEVEL=64 LD_LIBRARY_PATH=oracle_client ENV_FOR_DYNACONF=development python3.10 main.py```  


## 9 STOPPING AND RESTARTING

--> stop  
``` docker stop <name oracle container> ``` and stop pycharm run/debug server  
--> restart  
``` docker start <name oracle container> ``` and start pycharm run/debug server

