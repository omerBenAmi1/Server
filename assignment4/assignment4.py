import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

import mysql.connector

assignment4 = Blueprint('assignment4', __name__,
                        static_folder='static',
                        template_folder='templates', url_prefix='/assignment4')


@assignment4.route('/users')
def getting_users():
    users = get_users()
    return jsonify(users)


@assignment4.route('/restapi_users')
def get_default_user():
    users = get_users()
    return jsonify(users[0])


@assignment4.route('/restapi_users/')
def empty_default_user():
    return redirect(url_for("assignment4.get_default_user"))


@assignment4.route('/restapi_users/<USER_ID>')
def get_user(USER_ID):
    if not USER_ID.isnumeric():
        return jsonify({
            "error": "No such user exists"
        })
    users = get_users()
    for user in users:
        if user.id == int(USER_ID):
            return jsonify(user)

    return jsonify({"error": "No such user exists"})


def get_users():
    query = 'select * from users'
    return interact_db(query, query_type='fetch')


@assignment4.route('/')
def open_assignment4():
    error = None
    if "error" in request.args:
        error = request.args["error"]

    users_list = get_users()
    return render_template('assignment4.html', users=users_list, error=error)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb', auth_plugin='mysql_native_password')
    cursor = connection.cursor(named_tuple=True)

    # try:
    cursor.execute(query)
    # except Exception as e:
    #     print(e)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['insert_name']
    email = request.form['insert_email']

    users = get_users()
    for user in users:
        if user.email == email:
            return redirect(url_for("assignment4.open_assignment4", error="A user with that email already exists"))

    query = "INSERT INTO users(name, email) VALUES ('%s', '%s')" % (name, email)
    interact_db(query=query, query_type='commit')
    return redirect(url_for("assignment4.open_assignment4", error="This user has been successfully added"))


@assignment4.route('/update_user', methods=['POST'])
def update_user():
    i_email = request.form['insert_email']
    u_name = request.form['update_name']

    users = get_users()
    for user in users:
        if user.email == i_email:
            query = "UPDATE users SET name='%s' WHERE email='%s'" % (u_name, i_email)
            interact_db(query=query, query_type='commit')
            return redirect(url_for("assignment4.open_assignment4", error="This user update"))

    return redirect(url_for("assignment4.open_assignment4", error="A user with that email is not exists"))


@assignment4.route('/delete_user', methods=['POST'])
def delete_user():
    email = request.form['delete_email']

    users = get_users()
    exists = False
    for user in users:
        if user.email == email:
            exists = True

    if not exists:
        return redirect(url_for("assignment4.open_assignment4", error="No user with that email exists"))

    query = "DELETE FROM users WHERE email='%s';" % email
    interact_db(query, query_type='commit')
    return redirect(url_for("assignment4.open_assignment4", error="This user has been successfully deleted"))


@assignment4.route('/outer_source')
def return_html():
    return render_template('outer_source.html')


# @assignment4.route('/source')
# def source():
#
#         user_num = request.args['id']
#         response = requests.get(f"https://reqres.in/api/users/{user_num}")
#         print(response)
#         img = response.json()['data']['avatar']
#         first_name = response.json()['data']['first_name']
#         return render_template('outer_source.html', url=img, name=first_name)

@assignment4.route('/source', methods=['GET', 'POST'])
def source():
    if request.method == 'GET':
        id = request.args['id']
        response = requests.get(f"https://reqres.in/api/users/{id}")
        print(response)
        img = response.json()['data']['avatar']
        first_name = response.json()['data']['first_name']
        last_name = response.json()['data']['last_name']
        return render_template('outer_source.html', url=img, name=first_name, last_name=last_name)
    return render_template('outer_source.html')
