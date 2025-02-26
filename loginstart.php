<!DOCTYPE html>
<html>
  <body>
    <?php
     #checks if there are any login cookies
     if(isset($_COOKIE["UPHDAS_login"]))
     {
       #Defines mySQL connection variables
       $hostname = 'localhost';
       $dbname = 'website';
       $username = 'bdavis';
       $password = 'bdavis';

       #Creates a mySQL connection
       $conn = new mysqli($hostname, $username, $password, $dbname);

       #Cleans up expired cookies
       $deleteResult = $conn->query("delete from sessions where ".time()." > exptime");

       #CHecks if the user's cookie points to an active session
       $result = $conn->query("Select * from sessions where sessionid = '" . $_COOKIE["UPHDAS_login"] ."'");

       #Checks if the result of the query only had 1 row
       if($result->num_rows == 1)
       {
         #Moves user to homepage (skips login)
         header("Location: home.php");
         $conn->close();
         die();
       }
       else
       {
         $conn->close();
       }
     }
    ?>
    <p>Please enter your username and password below.</p><br>
    <form action="loginending.php" method="GET">
      Username: <input type="text" name="user" maxlength="128"><br>
      Password: <input type="password" name="pass" maxlength="128"><br>
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
