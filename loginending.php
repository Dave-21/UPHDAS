<?php
  require_once 'config.php';
  $conn = new mysqli($hn, $un, $pw, $db);
  $identified = FALSE;
  echo "login ending<br>";
  if ($conn->connect_error) die("Fatal Error");
  $query = "SELECT * FROM authentication";
  $result = $conn->query($query);
  if (!$result) die("Fatal Error");
  $rows = $result->num_rows;
  for($j = 0 ; $j < $rows ; ++$j)
  {
    $row = $result->fetch_array(MYSQLI_ASSOC);
    if($_GET["user"] == htmlspecialchars($row['username']) AND
    $_GET["pass"] == htmlspecialchars($row['password']) AND
    $identified == FALSE )
    {
        #expand on this later
        echo "Welcome " . htmlspecialchars($row['username']) . "<br>";
        echo "Permissions level ". htmlspecialchars($row['level']) . "<br>";

        #Tries to find an available session ID
        $rowchecker = 1;
        while($rowchecker > 0)
        {
          #selects a random session id
          $potentialID = rand(1000000000, 9999999999);
          #checks if there are any other sessions with the same session ID
          $checkerquery = $conn->query("Select * from sessions where sessionID = ".$potentialID);
          echo "Potential ID is ". $potentialID.", num rows is ". $checkerquery->num_rows . "<br>";
          #num_rows should be 0 if this is a unique session id
          $rowchecker = $checkerquery->num_rows;
        }
        #inserts the current session into the sessions table
        $sessionQuery = $conn->query("Insert into sessions values('".$potentialID."', '" . htmlspecialchars($row['username']) . "', '" . time()+3600 . "', '" . htmlspecialchars($row['level'])."')");
        if(!$sessionQuery) die("Could not add session to database");
        $identified = TRUE;

        setcookie("UPHDAS_login", $potentialID, time()+3600, "/");
        header("Location: home.php");
    }
  }
  if($identified == FALSE)
  {
        echo "Incorrect username or password.<br>";
        echo "<a href='loginstart.php'>Back</a>";
  }
  $result->close();
  $conn->close();
 ?>
