<div>
    <p><a href="/">Go back to Home</a></p>
    <p><a href="/search">Search users</a></p>
</div>

<div>
    <h2>New user form:</h2>
    <form action="/new_user_form" method="POST">

        Email: <input type="text" size="50" maxlength="50" name="email"><br>
        User handle: <input type="text" size="50" maxlength="50" name="user_handle"><br>
        Password: <input type="password" size="50" maxlength="50" name="password"><br>
        Display name: <input type="text" size="50" maxlength="50" name="display_name"><br>
        Bio: <input type="text" size="50" maxlength="50" name="bio"><br>
        Profile picture: <input type="text" size="50" maxlength="50" name="picture"><br>
        <input type="hidden" name="premium" value="0">
        Premium account: <input type="checkbox" name="premium" value="1"><br>
        <input type="submit" name="add" value="Create!">

    </form>
</div>