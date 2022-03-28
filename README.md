# Databases - Final Project instructions
This was the final project for the course "Databases"

## Create the database
While the database is already included in the folder as `workout_challenge.db`, this can be recreated by running:

```sql
.read create_db.sql
.read populate_db.sql
.read triggers.sql
.save workout_challenge.db
```

## Run the application

The web application can be ran as usual:

```console
python final.py
```
Then, proceed to http://localhost:8080/ in your web explorer.

Only additional library is `datetime` (apart from `bottle` and `sqlite3`).

## Navigating the web app

The homepage will take the user to a menu in which it will be possible to choose the search engine (item 0) or a list of supported sports (not included in the rubric).

The search engine has the specificied functionaly of supporting searches by two attributes: user handle and display name. When using *, the engine reads it as a wildcard. Moreover, there is an additional field to specify the number of results the user wants to see (default is 20). If nothing is specified, the search engine will provide all results of the database limited by the "limit search results by" field.

Recommended search querys:
- user handle: lawrence\*, \*lawrence\*, \*john\*, john14
- display name: john\*, john james, \*cooper
- mix: user handle: lawrence\*; display name: \*john\*

The result entry will provide distinguishable information for every record (item 1), a link to view the record in detail (item 2), a link to delete the user (item 3), a link to see all photoworkouts related to that user (item 4), and a link to add new photoworkouts (item 5).

When viewing the user in detail, it will be possible to update the user through a link at the end of the page (item 2).

When clicking on the 'add photoworkout' the user will see a form to add a new photoworkout (item 5).

Finally, on top of the search engine page, it will be possible to add new users (item 6). Clicking on the 'add a new user' link will lead the user to a new form.

Please note that error handling is embeded in every function in `final.py`. Try, for example, to add a user with an existing email (emails must be unique) --it won't be possible.

Additionally, cascade deletion is handled via triggers. If a user is deleted, all its photoworkouts will be deleted as well.

Only 'weird' errors are handled via 401, 404, 500. A user manipulating the address bar with a non-existent address will activates this sort of errors.

