# UniVerse Backend

## Getting Started

### Pre-requisites

Before to start, you need to install the following tools:

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. [Docker Compose](https://docs.docker.com/compose/install/)

---

#### Clone the repository

First, clone the repository:

```bash
git clone https://github.com/El-Clan-Del-Bug/UniVerse-Backend.git && cd UniVerse-Backend
```

If you can get the last version of the repository, you can use the following command:

```bash
git pull origin develop
```

---

#### Create the .env file

Then, create the `.env` file, and add the following variables:

```text
# Server
HOST=api
PORT=3333
ENV=development
SECRET_KEY=

# MySQL
MYSQL_USER=<custom-user>
MYSQL_PASSWORD=<custom-password>
MYSQL_HOST=database
MYSQL_PORT=3306
MYSQL_DB_NAME=<custom-db-name>

# JWT
JWT_SECRET_KEY=
```

**IMPORTANT:** Replace the `<custom-user>`, `<custom-password>` and `<custom-db-name>` values with your own values.

To create the `SECRET_KEY` and `JWT_SECRET_KEY` variables, you can use the following command:

```bash
# With Node.js
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"

# With Python
python -c 'import secrets; print(secrets.token_urlsafe(256))'
```

And copy the output to the `.env` file.

**NOTE:** Use different values for the `SECRET_KEY` and `JWT_SECRET_KEY` variables.

---

#### Create Database User

Create a file in the project root file named `init.sql`, in this file create the database user, the script should look like this:

```sql
CREATE USER '<custom-user>'@'%' IDENTIFIED BY '<custom-password>';
GRANT ALL PRIVILEGES ON <custom-db-name>.* TO '<custom-user>'@'%';
FLUSH PRIVILEGES;
```

**IMPORTANT:** Replace the `<custom-user>`, `<custom-password>` and `<custom-db-name>` values with your own values.

---

#### Run Docker Compose

Then, run the following command:

```bash
docker-compose up
```

You can see the status of your containers from `Docker Desktop`, if something fails, just restart the containers. To restart the containers, run the following command:

```bash
docker-compose restart
```

Look at the `api` container logs, when you see something like:

```text
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://api:3333
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 357-031-883
 * Serving Flask app 'config.server_conf'
 * Debug mode: on
```

the project will be running at `127.0.0.1:3333`

---

#### Stop Docker Compose

To stop the containers, run the following command:

```bash
docker-compose down
```
