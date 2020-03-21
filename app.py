#!/usr/bin/env python
# coding: utf-8

# ## Import Dependencies
# 
# Dependencies are libraries that help extend the functionality of core Python.

# In[1]:


from sqlalchemy import create_engine
import pymysql
import pandas as pd
import flask
import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()


# ## Import config variables
# 
# The `is_heroku` variable checks to see if this code has been deployed to Heroku. If not, then read in the credentials from the `config.py` file.

# In[2]:


# Heroku Check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

if is_heroku == True:
    remote_db_host = os.environ.get('remote_db_host')
    remote_db_port = os.environ.get('remote_db_port')
    remote_db_user = os.environ.get('remote_db_user')
    remote_db_pwd = os.environ.get('remote_db_pwd')
    remote_db_name = os.environ.get('remote_db_name')
else:
    from config import remote_db_host, remote_db_port, remote_db_user, remote_db_pwd, remote_db_name


# ## Instantiate Flask
# 
# Flask is the framework that helps serve up your site via the web. 
# 
# There is a bunch of documentation on it, but you can start here: https://flask.palletsprojects.com/en/1.1.x/

# In[3]:


app = Flask(__name__)


# ## Create Database Connection
# 
# This uses the config variables that were created earlier.

# In[4]:


engine = create_engine(f'mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_host}:{remote_db_port}/{remote_db_name}')


# ## Create a Default Route
# 
# The default route is defined at the root level. You will get this endpoint when you pull up your site by default.
# 
# For example, on the localhost, you will get this route if you enter `http://localhost:5000'`
# 
# Port `5000` is the default port for Flask.

# In[5]:


@app.route('/')
def index():
    conn = engine.connect()

    ksa_df = pd.read_sql('SELECT * FROM ksa', conn)

    ksa_json = ksa_df.to_json(orient='records')

    return render_template('index.html')


# ## Create a Route for the KSA data
# 
# This one is named `api/data/ksa`. The idea here is to indicate that data will be served up through an API. Technically, routes can be named whatever you'd like.

# In[6]:


@app.route('/api/data/ksa')
def ksa():
    # establish a connection to your database
    conn = engine.connect()

    # query the `ksa` table and load it into your DataFrame
    ksa_df = pd.read_sql('SELECT * FROM ksa', conn)
    
    # convert your DataFrame into `json`
    ksa_json = ksa_df.to_json(orient='records')

    # return the json to the client
    return(ksa_json)


# ## Run the App
# 
# This one is named `api/data/ksa`. The idea here is to indicate that data will be served up through an API. Technically, routes can be named whatever you'd like.

# In[ ]:


if __name__ == '__main__':
    app.run()

