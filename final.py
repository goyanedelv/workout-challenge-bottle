from bottle import route, run, template, post, get, request, error
from datetime import datetime

import sqlite3
con = sqlite3.connect('workout_challenge.db')
cur = con.cursor()

# Aux function, adapted from geeksforgeeks
def isSubstring(s1, s2):
    '''
    Returns true if s1 is substring of s2
    '''
    M = len(s1)
    N = len(s2)
 
    # A loop to slide pat[] one by one
    for i in range(N - M + 1):
 
        # For current index i,
        # check for pattern match
        for j in range(M):
            if (s2[i + j] != s1[j]):
                break
             
        if j + 1 == M :
            return True
 
    return False

# Home
@route('/')
def welcome():
    html = "<h2> Welcome to the Workout Challenge App!!! </h2>"

    html += '''
    <p><a href="/search">Search users</a></p>
    <p><a href="/sports">Take a look to all the sports our app supports</a></p>
    '''
    return html

# See all sports
@route('/sports')
def hello():
    html = '''
      <p><a href="/">Go back to Home</a></p>
      <p><a href="/search">Search users</a></p>
    '''
    html += "<h2> All Possible Exercises </h2> <br /> <table>"
    for row in cur.execute('select * from exercise'):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"

    return html

# See specific players
@route('/players/<user_id>')
def show_specific(user_id):
    html = '''
    <p><a href="/">Go back to Home</a></p>
    <p><a href="/search">Search users</a></p>
    '''
    row = cur.execute(f"select user_id, user_handle, email, bio from user where user_id = {str(user_id)}")

    fetched = row.fetchall()[0]
    
    html += f"<h2> Hello @{fetched[1]}!</h2>"
    html += f"<p> Player #{user_id} </p> "
    html += f"<p> Email: {fetched[2]} </p> "
    html += f"<p> Bio: {fetched[3]} </p><br>"

    html += f'<p><a href="/update/{user_id}"> Update this player </a></p>'

    return html

# Search engine frontend
@route('/search')
def add_new():
    return template('search_interface')

# Search backend and results
@route('/search_results', method='POST')
def search():
    collect = [value[1] for value in request.forms.items()]

    print(collect)
    query_ui = collect[0]
    query_un = collect[1]
    limiter = int(collect[2])

    query_ui = query_ui.replace("*", "%")
    query_un = query_un.replace("*", "%")

    if (query_ui == '') & (query_un == ''):
        realm = 0
        query0 = f'select user_id, display_name, user_handle, bio from user limit {limiter}'
    elif query_un == '':
        p = query_ui
        realm = 1
        query1 = f"select user_id, display_name, user_handle, bio from user where user_handle like '{str(p)}' limit {limiter}"
        p = p.replace("%", "*")

    elif query_ui == '':
        q = query_un
        realm = 2
        query2 = f"select user_id, display_name, user_handle, bio from user where display_name like '{str(q)}' limit {limiter}"
        q = q.replace("%", "*")

    else:
        p = query_ui
        q = query_un
        realm = 3
        query3 = f"select user_id, display_name, user_handle, bio from user where display_name like '{str(q)}' AND user_handle like '{str(p)}' limit {limiter}"
        
        p = p.replace("%", "*")
        q = q.replace("%", "*")

    print(realm)

    html = '''
      <div><a href="/">Go back to Home</a></div>
      <div><a href="/search">Search a new term</a></div>
    '''

    html += "<br /><br />"
    
    if realm == 0:
        print("No querys provided --printing all results")
        html += f'<h2> Showing all users...</h2><p><i><a href="/new_user">Add a new user</a></i></p><br/> <table>'
        query = cur.execute(query0)
    elif realm == 1:
        print(f"Search term: {p}")
        html += f'<h2> Results for "{p}"</h2><p><i><a href="/new_user">Add a new user</a></i></p><br/>  <table>'
        query = cur.execute(query1)
    elif realm == 2:
        print(f"Search term: {q}")
        html += f'<h2> Results for "{q}"</h2><p><i><a href="/new_user">Add a new user</a></i></p><br/>  <table>'
        query = cur.execute(query2)
    else:
        print(f"Search term: {p} and {q}")
        html += f'<h2> Results for "{p}" and "{q}"</h2><p><i><a href="/new_user">Add a new user</a></i></p><br/> <table>' 
        query = cur.execute(query3)

    fetched = query.fetchall()

    if len(fetched) == 0:
        if realm == 1:
            html += f'<p> There are no users matching "{p}". <a href="/search">Try with another term</a> or use wildcards with *.'
            return html
        elif realm == 2:
            html += f'<p> There are no users matching "{q}". <a href="/search">Try with another term</a> or use wildcards with *.'
            return html
        elif realm == 3:
            html += f'<p> There are no users matching "{p}" and "{q}". <a href="/search">Try with another set of term</a> or use wildcards with *.'
            return html

    else:

        html += '''<tr> 
        <th> User id</th>
        <th> Display Name</th>
        <th> User handle</th>
        <th> Bio</th>
        <th> View </th>
        <th> Delete </th>
        <th> Show photoworkouts </th>
        <th> Add photoworkotus </th>
        </tr>
        '''
    
        # Had to call this again
        if realm == 0:
            query = cur.execute(query0)
        elif realm == 1:
            query = cur.execute(query1)
        elif realm == 2:
            query = cur.execute(query2)
        else:
            query = cur.execute(query3)

        for row in query:
                html += "<tr>"
                for cell in row:
                    html += "<td>" + str(cell) + "</td>"
                html += f'''
                <td> <a href=/players/{row[0]}>View </a></td> 
                <td> <a href=/delete/{row[0]}>Delete </a></td>
                <td> <a href=/photoworkouts/{row[0]}>Show photoworkouts </a></td>
                <td> <a href=/add/{row[0]}>Add photoworkout </a></td>     
                </tr>
                '''
        html += "</table>"

        return html

# Delete
@route('/delete/<user_id>')
def delete(user_id):
    cur.execute(f"delete from user where user_id = '{user_id}'")
    con.commit()

    return f"User #{user_id} deleted succesfully. Return to <a href=/>Homepage</a> or <a href=/search>Search Engine</a>"

# See related photoworkouts
@route('/photoworkouts/<user_id>')
def see_photoworkouts(user_id):
    query = cur.execute(f'''
    select photoworkout_id, caption, likes_count, photo_locator, photoworkout.creation_date
    FROM photoworkout
    INNER JOIN photoworkouts_user
    USING(photoworkout_id)
    INNER JOIN user
    USING(user_id)
    WHERE user_id = {user_id}
    ''')

    html = f'''
      <p><a href="/">Go back to Home</a></p>
      <p><a href="/search">Search users</a></p><br>

      <h2> Photoworkouts of User #{user_id}</h2><br>
    '''

    html += '''<table><tr> 
    <th> Photoworkout id</th>
    <th> Caption</th>
    <th> Likes count</th>
    <th> Picture</th>
    <th> Creation date</th>

    </tr>
    '''

    for row in query:
        html += "<tr>"
        for cell in row:
            if isSubstring(".jpg" , str(cell)):
                
                picture = f'<img src="https://robohash.org/{str(cell)}.png">'

                html += "<td>" + picture + "</td>"
            else:
                html += "<td>" + str(cell) + "</td>"

    html += "</table>"

    return html

# Add a new photoworkout interface
@route('/add/<user_id>')
def add_interface(user_id):
    html = f'''
    <p><a href="/">Go back to Home</a></p>
    <p><a href="/search">Search users</a></p><br>

    <h2> Add a photoworkout for User #{user_id}</h2><br>
    '''
    html += f'''
    <div>
    <form action="/add_new_pw" method="POST">
        Caption: <input type="text" size="50" maxlength="50" name="caption"><br>
        Picture: <input type="text" size="50" maxlength="50" name="picture"><br>
        
        <input type="hidden" size="50" maxlength="50" name="user_id_new_photoworkout" value={str(user_id)}><br>
        <input type="submit" name="add" value="Add!">

    </form>
    </div>
    '''

    return html

# Add a new photoworkout backend and interface
@route('/add_new_pw', method='POST')
def add_photoworkout():
    collect = [value[1] for value in request.forms.items()]

    caption = collect[0]
    picture = collect[1]
    user_id = collect[2]

    if (caption == '') | (picture == ''):
        return f"Caption or picture location cannot be empty! Please <a href=/add/{user_id}>try again</a> providing correct parameters"
    
    else:
        now = str(datetime.now())[:19]

        row = cur.execute(f"select photoworkout_id from photoworkout order by photoworkout_id DESC")

        next_photoworkout_id = row.fetchall()[0][0] + 1

        query0 = f"INSERT INTO photoworkout VALUES ({next_photoworkout_id}, '{now}', '{now}', '{caption}', 0, '{picture}.jpg')"

        query1 = f"INSERT INTO photoworkouts_user VALUES ('{next_photoworkout_id}', '{user_id}')"

        cur.execute(query0)
        con.commit()

        cur.execute(query1)
        con.commit()

        return f"Photoworkout #{next_photoworkout_id} for User #{user_id} created succesfully. Return to <a href=/>Homepage</a> or <a href=/search>Search Engine</a>"

# Update records of a user --interface
@route('/update/<user_id>')
def update_interface(user_id):

    row = cur.execute(f"select user_id, user_handle, display_name, bio from user where user_id = {str(user_id)}")

    fetched = row.fetchall()[0]
    
    user_handle = fetched[1]
    display_name = fetched[2]
    bio = fetched[3]

    return template('update', user_id=user_id, user_handle=user_handle, display_name=display_name, bio=bio)

# Update user backend and post interface
@route('/update_form', method="POST")
def update():
    collect = [x[1] for x in request.forms.items()]
    print(collect)

    user_handle = collect[0]
    display_name = collect[1]
    bio = collect[2]
    user_id = collect[3]

    if '' in collect:
        return f'Values cannot be left blank. <a href="/update/{user_id}">Try again.</a>'
    else:

        query1 = f"UPDATE user SET user_handle ='{user_handle}', display_name = '{display_name}', bio = '{bio}' WHERE user_id = '{user_id}'"

        cur.execute(query1)
        con.commit()

        return f"User #{user_id} updated succesfully. Return to <a href=/>Homepage</a> or <a href=/search>Search Engine</a>"

# Link to create a new user in top of the search engine
@route('/new_user')
def new_user_interface():
    return template('new_user')

# Create user backend and post interface
@route('/new_user_form', method="POST")
def new_user():
    dict_collect = {k:v for k, v in request.forms.items()}
    print(dict_collect)


    query_unique_email = f"select email from user where email = '{dict_collect['email']}'"
    row = cur.execute(query_unique_email)
    fetched = row.fetchall()

    print(fetched)

    email_unique = True

    if len(fetched) == 1:
        email_unique = False


    if '' in dict_collect.values():
        return f'Values cannot be left blank. <a href="/new_user">Try again.</a>'
    elif not email_unique:
        return f'Provided email is already in use. <a href="/new_user">Try again.</a>'
    else:
        now = str(datetime.now())[:19]

        row = cur.execute(f"select user_id from user order by user_id DESC")

        next_user_id = row.fetchall()[0][0] + 1

        digest = 'imagine_that_there_is_an_encryption_here'

        query0 = f"INSERT INTO user VALUES ({next_user_id}, '{now}', '{now}', '{dict_collect['email']}', '{digest}', {dict_collect['premium']}, '{dict_collect['picture']}', '{dict_collect['bio']}', '{dict_collect['user_handle']}', '{dict_collect['display_name']}')"

        cur.execute(query0)
        con.commit()

        return f"User #{next_user_id} created succesfully. Return to <a href=/>Homepage</a> or <a href=/search>Search Engine</a>"

# Exceptional errors --only in case the user search something inexistent through the address bar. All other errors are handled in their respective overarching functions
@error(404)
def error404(error):
    return 'Error 404. Nothing here, sorry. <a href="/">Go to Home.</a>'

@error(401)
def error401(error):
    return 'Error 401. Nothing here, sorry. <a href="/">Go to Home.</a>'

@error(500)
def error500(error):
    return 'Error 500. Nothing here, sorry. <a href="/">Go to Home.</a>'

run(host = 'localhost', port = 8080, debug = True)
