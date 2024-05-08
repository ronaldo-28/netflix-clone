# Netflix Clone App
This is a Flask web application that serves as a clone of Netflix, allowing users to sign in, register, and access movies. 


### Working

https://github.com/pavankumarmuppuri/Netflix-Clone/assets/155610590/5746a173-1385-43d3-8678-507ee38dbc74

## Setup

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`.

2. **Database Configuration and URI**: Set up a PostgreSQL database for the application.<br> You can use tools like pgAdmin or the command line to create a new database and user.<br> Obtain the URI for connecting to your PostgreSQL database. <br>It should look like `postgresql://username:password@localhost/database_name`, where:
    - `username`: Your PostgreSQL username
    - `password`: Your PostgreSQL password
    - `localhost`: The host where your database is running (typically `localhost` for local development)
    - `database_name`: The name of your database

    **Replace Database URI**: Replace the default database URI in `app.py` with your own database connection details. Modify the following line:

    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
    ```

    Replace `username`, `password`, and `database_name` with your actual database credentials.


3. **Install Dependencies**: Install the required Python dependencies using `pip install -r requirements.txt`.

4. **Initialize Database**: Run the following command to initialize the database schema:

    ```bash
    python app.py db upgrade
    ```

5. **Run the Application**: Start the Flask application by running `python app.py`.

6. **Access the Application**: Access the application in your web browser at `http://localhost:5000`.


## Features

1. **User Authentication**: Users can sign in, register, and log out securely.
2. **Superuser Privileges**: Superusers have additional privileges such as managing users.
3. **Database Integration**: Uses PostgreSQL database for storing user data.
4. **Restricted Access to Movies**: Movie access is limited to logged-in users only. Only authenticated users can access and watch movies, ensuring a secure and personalized viewing experience.

## Steps to run the project in your PC
### Database Setup

1. **Create a PostgreSQL Database**: Create a PostgreSQL database named `ott` (or a name of your choice).

2. **Update Database URI**: Update the database URI in the Flask app configuration (`app.config['SQLALCHEMY_DATABASE_URI']`) to point to your local database.<br> Modify the following line in `app.py`:

   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'

   
### Running the Application

<b>To run the Flask application, execute the following command:</b>

python app.py
The application should now be running locally. You can access it by navigating to http://localhost:5000 in your web browser.

### Usage

1. Sign in with existing credentials or register as a new user to access the movie page.
2. Superusers have additional features to manage other users. Use the appropriate routes to access these functionalities.

### Deployment

<b>For deployment in a production environment, ensure the following:</b>

1. Set `debug` to `False` in the Flask app configuration.
2. Secure your database and application environment with appropriate access controls and credentials.
3. Consider deploying your Flask app on a platform like Heroku or PythonAnywhere for easier access from anywhere with an internet connection.
