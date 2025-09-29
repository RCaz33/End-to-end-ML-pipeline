
1. Follow the Readme

.. code-block:: bash

  git clone https://github.com/<user>/<repo>.git

2. Install PostgreSQL

.. code-block:: bash

  brew install postgresql

3. Verify that PostgreSQL is installed and running

.. code-block:: bash

  postgres -V

4. Open PSQL command line

.. code-block:: bash

  psql postgres

5. Create a DB User "db_user" with Password "123" (in psql command line)

.. code-block:: bash

  CREATE ROLE db_user WITH LOGIN PASSWORD '123';

6. Verify the new DB User (in psql command line)

.. code-block:: bash

  \du

7. Create Database (in psql command line)

.. code-block:: bash

  CREATE DATABASE mlflow_db;


Create dedicated schema for dbuser

.. code-block:: bash

CREATE SCHEMA mlflow_schema AUTHORIZATION db_user_mlflow;

Grant usage on new database

.. code-block:: bash

GRANT USAGE ON SCHEMA mlflow_schema TO db_user_mlflow;
GRANT CREATE ON SCHEMA mlflow_schema TO db_user_mlflow;

SPECIFY SCHEMA FOR USER MLFLOW

.. code-block:: bash

ALTER ROLE db_user_mlflow SET search_path = mlflow_schema;


8. Verify the New Database was created (in psql command line)

.. code-block:: bash

  \list

9. Grant the User access to the Database (in psql command line)

.. code-block:: bash

    GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO db_user;

10. check access

.. code-block:: bash

  \dg

11. set up environment variables

* tracking metadata locally
os.environ['MLFLOW_TRACKING_URI'] = 'postgresql+psycopg2://db_user:123@localhost/mlflow_db'
* MUST Set MLflow to use the new schema
os.environ['MLFLOW_TRACKING_URI'] = "postgresql+psycopg2://db_user_mlflow:123@localhost/mlflow_db?options=-csearch_path=mlflow_schema"


* serving artifact on AWS S3
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://192.168.86.64:9001'
