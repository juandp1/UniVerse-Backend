# UniVerse Backend

## Getting started

Dependencies:

1. Python 3.10 or higher
2. MySQL 8.0 or higher

### Clone the repository

```bash
git clone https://github.com/El-Clan-Del-Bug/UniVerse-Backend.git && cd UniVerse-Backend
```

### Create virtual enviroment

```bash
pip install virtualenv
python3 -m venv .venv
```

### Activate virtual env

#### Linux - MacOs

```bash
source .venv/bin/activate
```

#### Windows Powershell

Before to execute the command [enable execution of scripts in powershell](https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts)

```bash
.\venv\Scripts\Activate.ps1
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Configure Enviroment Variables

```bash
# Server
HOST=127.0.0.1
PORT=8080
ENV=development
SECRET_KEY=
# MySQL
MYSQL_USER=root
MYSQL_PASSWORD=1201
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB_NAME=generic-database
# JWT
JWT_SECRET_KEY=
```

### Run the project

```bash
python3 server.py
```
