# Use AFiT

AFiT runs on python 3.9. Make sure it is installed on your machine before following the installation steps.

## Setting Neo4j Database

### Install Neo4j Community Edition

Install Neo4j Community edition by running installNeo4j.sh script.

```bash
$ ./installNeo4j.sh
```

If the installation was not successful, follow the instruction from [Neo4j Website](https://neo4j.com/docs/operations-manual/current/installation/)

### Checking installation

Start Neo4j with the following command.

```bash
$ sudo systemctl start neo4j.service
```

Display Neo4j status.

```bash
$ sudo systemctl status neo4j.service
```

The output should be the following:

```bash
● neo4j.service - Neo4j Graph Database
     Loaded: loaded (/lib/systemd/system/neo4j.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2020-08-07 01:43:00 UTC; 6min ago
   Main PID: 21915 (java)
      Tasks: 45 (limit: 1137)
     Memory: 259.3M
     CGroup: /system.slice/neo4j.service
. . .
```

### Setting Neo4j new password

Run to following command to start neo4j cypher shell

```bash
cypher-shell
```

You will be asked to set a new password. The password define in AFiT's source code is `mitre`. If you choose to use another password, you should modify it in the code otherwise AFiT won't be able to connect to Neo4j Database.

```bash
cypher-shell prompt
username: neo4j
password: neo4j  								# Default password
Password change required
new password: mitre  								# Set new password 
confirm password: mitre  							# Confirm new password 
Connected to Neo4j 4.1.0 at neo4j://localhost:7687 as user neo4j.
Type :help for a list of available commands or :exit to exit the shell.
Note that Cypher queries must end with a semicolon.
```

Exit cypher-shell with the following command.

```bash
neo4j@neo4j> :exit
```


## Run AFiT in a python virtual environment (Optional)

### Create

Create a new python virtual environment to run AFiT.

#### With Venv

```bash
$ python3.9 -m venv /path/to/new/environment/env_name
```

If the following error is displayed,

```bash
Error: Command '['/home/trainees/Desktop/AFiT/AFIT/bin/python3.9', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
```

install venv lib for python 3.9.

```bash
$ sudo apt-get install python3.9-dev python3.9-venv
```

#### With Conda

```bash
$ conda create --name env_name python=3.9
```


### Activate

Activate the virtual environment.

#### With Venv

```bash
$ source /path/to/new/environment/env_name/bin/activate
```


#### With Conda

```bash
$ conda activate env_name
```

### Deactivate

Once you are finished using AFiT, you can deactivate the environment.

#### With Venv

```bash
$ deactivate
```


#### With Conda

```bash
$ conda deactivate
```


## Start AFiT

To start the program, run AFiT.sh script.

```bash
$ ./AFiT.sh
```

This script will install the requirements of the program in the current virtual environment and launch AFiT.

If the requirements are already installed, the following message will be displayed.

```bash
Requirement already satisfied: GitPython==3.1.24 in ./Test1/lib/python3.8/site-packages (from -r requirements.txt (line 1)) (3.1.24)
Requirement already satisfied: neo4j==4.3.4 in ./Test1/lib/python3.8/site-packages (from -r requirements.txt (line 2)) (4.3.4)
Requirement already satisfied: py2neo==2021.2.0 in ./Test1/lib/python3.8/site-packages (from -r requirements.txt (line 3)) (2021.2.0)
Requirement already satisfied: PySide6==6.2.1 in ./Test1/lib/python3.8/site-packages (from -r requirements.txt (line 4)) (6.2.1)
Requirement already satisfied: gitdb<5,>=4.0.1 in ./Test1/lib/python3.8/site-packages (from GitPython==3.1.24->-r requirements.txt (line 1)) (4.0.9)
Requirement already satisfied: typing-extensions>=3.7.4.3 in ./Test1/lib/python3.8/site-packages (from GitPython==3.1.24->-r requirements.txt (line 1)) (4.0.1)
Requirement already satisfied: pytz in ./Test1/lib/python3.8/site-packages (from neo4j==4.3.4->-r requirements.txt (line 2)) (2021.3)
Requirement already satisfied: packaging in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (21.3)
Requirement already satisfied: interchange~=2021.0.3 in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (2021.0.4)
Requirement already satisfied: pygments>=2.0.0 in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (2.11.2)
Requirement already satisfied: monotonic in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (1.6)
Requirement already satisfied: urllib3 in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (1.26.8)
Requirement already satisfied: pansi>=2020.7.3 in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (2020.7.3)
Requirement already satisfied: six>=1.15.0 in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (1.16.0)
Requirement already satisfied: certifi in ./Test1/lib/python3.8/site-packages (from py2neo==2021.2.0->-r requirements.txt (line 3)) (2021.10.8)
Requirement already satisfied: shiboken6==6.2.1 in ./Test1/lib/python3.8/site-packages (from PySide6==6.2.1->-r requirements.txt (line 4)) (6.2.1)
Requirement already satisfied: smmap<6,>=3.0.1 in ./Test1/lib/python3.8/site-packages (from gitdb<5,>=4.0.1->GitPython==3.1.24->-r requirements.txt (line 1)) (5.0.0)
Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in ./Test1/lib/python3.8/site-packages (from packaging->py2neo==2021.2.0->-r requirements.txt (line 3)) (3.0.6)
```

If so, you may want to run AFiT without installing the requirement. To do so, run the following command.

```bash
$ python3.9 AFiT.py
```

### First use

On first use of AFiT, it is highly recommended to load MitreAttack data to have the database up to date.
