<?php

  #Defines mySQL connection variables
  $hn = 'localhost';
  $db = 'website';
  $un = 'bdavis';
  $pw = 'bdavis';

  #Creates a mySQL connection
  $conn = new mysqli($hn, $un, $pw, $db);

  #Error-checks the connection
  if ($conn->connect_error) die("Fatal Error");

  #Creates a series of SQL commands to create tables if they don't already exist
  $query0 = "SET FOREIGN_KEY_CHECKS=0";
  $queryAuth = "CREATE TABLE IF NOT EXISTS authentication(username varchar(128) not null, password varchar(128) not null, level varchar(32) not null, primary key(username)) ENGINE InnoDB";
  $querySesh = "CREATE TABLE IF NOT EXISTS sessions(sessionID char(10) not null, username varchar(128) not null, exptime char(10) not null, level varchar(32) not null, primary key(sessionID)) ENGINE InnoDB";
  $query1 = "SET FOREIGN_KEY_CHECKS=1";

  #Runs the SQL queries
  $result0 = $conn->query($query0);
  $result1 = $conn->query($queryAuth);
  $result2 = $conn->query($query1);
  $result3 = $conn->query($querySesh);
  if (!$result0 OR !$result1 OR !$result2 OR !$result3) die ("Database access failed");


  #Deletes old/expired sessionID's from the database
  $deleteResult = $conn->query("delete from sessions where ".time()." > exptime");
  if(!$deleteResult) die("Failed to delete old sessions.");



  #Checks if the user has an active sessionID cookie
  if(isset($_COOKIE["UPHDAS_login"]))
  {
    #Checks the database for a sessionID that matches the cookie on the user's computer
    $sessionResult = $conn->query("Select * from sessions where sessionid = '" . $_COOKIE["UPHDAS_login"] ."'");
    if($sessionResult->num_rows != 1)
    {
      $conn->close();
      echo "Access denied.<br>";
      setcookie("UPHDAS_login", $potentialID, time()-3600, "/");
      header("Location: loginstart.php");
    }
    else if(!$sessionResult) die("Failed to fetch sessionIDs");
    else if ($sessionResult->num_rows == 1)
    {
      $data = $sessionResult->fetch_Array(MYSQLI_ASSOC);
      echo "Cookie session IDi is " . $_COOKIE["UPHDAS_login"] . ", database session ID is " . htmlspecialchars($data['sessionID']) . ".<br>";
      if($_COOKIE["UPHDAS_login"] != htmlspecialchars($data['sessionID']) || htmlspecialchars($data['level']) != 'admin')
      {
        $conn->close();
        echo "Access denied.<br>";
        setcookie("UPHDAS_login", $potentialID, time()-3600, "/");
        header("Location: loginstart.php");
      }
    }
  }
  else
  {
    $conn->close();
    echo "Your session has expired. Please log in again.<br>";
    header("Location: loginstart.php");
  }
  #deletes old sessions




?>
