<div>
    <p><a href="/">Go back to Home</a></p>
</div>

<h2>Workout Challenge Search Engine:</h2>

<div>
    <p><i><a href="/new_user">Add a new user</a></i></p>
</div>

<div>
    <p> <i> Use * as wildcard </i> </p>
    <form action="/search_results" method="POST">
        Search by user handle: <input type="text" size="50" maxlength="50" name="user_handle"><br>
        Search by display name: <input type="text" size="50" maxlength="50" name="user_name"><br>

        <label for="limit_query">Limit search results by:</label>
        <select name="limiter" id="limit_query">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="5" selected>5</option>
        <option value="20" selected>20</option>
        <option value="9999999">All</option>

        </select><br>

        <input type="submit" name="add" value="Search!">

    </form>
</div>