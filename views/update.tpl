<div>
    <p><a href="/">Go back to Home</a></p>
    <p><a href="/players">See all players</a></p>
    <p><a href="/search">Search users</a></p>
</div>

<div>
    <h2>Edit User #{{user_id}}:</h2>
    <form action="/update_form" method="POST">

        User handle: <input type="text" size="50" maxlength="50" name="user_handle" value="{{user_handle}}"><br>
        Display name: <input type="text" size="50" maxlength="50" name="display_name" value="{{display_name}}"><br>
        Bio: <input type="text" size="50" maxlength="50" name="bio" value="{{bio}}"><br>
        <input type="hidden" size="50" maxlength="50" name="user_id" value="{{user_id}}"><br>

        <input type="submit" name="add" value="Update!">

    </form>
</div>