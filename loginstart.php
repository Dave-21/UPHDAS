<!DOCTYPE html>
<html>
  <body>
    <?php
     #checks if there are any login cookies
     if(isset($_COOKIE["UPHDAS_login"]))
     {
       #require_once 'config.php';
       $conn = new mysqli($hn, $un, $pw, $db);
       $result = $conn->query("Select * from sessions where sessionid = '" . $_COOKIE["UPHDAS_login"] ."'");
       if($result->num_rows == 1)
       {
         header("Location: home.php");
         $conn->close();
         die();
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
