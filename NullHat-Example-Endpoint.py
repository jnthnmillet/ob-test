#!/usr/bin/env python
# coding: utf-8

# ## Import Dependencies
#
# Dependencies are libraries that help extend the functionality of core Python.

# In[10]:


from sqlalchemy import create_engine
import pymysql
import pandas as pd
import flask

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()


# ## Import config variables

# In[11]:

# Heroku Check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

if is_heroku == False:
    from config import remote_db_host, remote_db_port, remote_db_user, remote_db_pwd, remote_db_name
else:
    remote_db_host = os.environ.get('remote_db_host')
    remote_db_port = os.environ.get('remote_db_port')
    remote_db_user = os.environ.get('remote_db_user')
    remote_db_pwd = os.environ.get('remote_db_pwd')
    remote_db_name = os.environ.get('remote_db_name')

app = Flask(__name__)


# In[12]:


engine = create_engine(f'mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_host}:{remote_db_port}/{remote_db_name}')


# In[ ]:


@app.route('/api/data/ksa')
def ksa():
    conn = engine.connect()

    ksa_df = pd.read_sql('SELECT * FROM ksa', conn)

    ksa_json = ksa_df.to_json(orient='records')

    return(ksa_json)


# In[ ]:


if __name__ == '__main__':
    app.run(debug=True)
