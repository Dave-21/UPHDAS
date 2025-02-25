<?php
  $hn = 'localhost';
  $db = 'website';
  $un = 'bdavis';
  $pw = 'bdavis';
  $conn = new mysqli($hn, $un, $pw, $db);
  if ($conn->connect_error) die("Fatal Error");
  $query0 = "SET FOREIGN_KEY_CHECKS=0";
  $queryAuth = "CREATE TABLE IF NOT EXISTS authentication(username varchar(128) not null, password varchar(128) not null, level varchar(32) not null, primary key(username)) ENGINE InnoDB";
  $querySesh = "CREATE TABLE IF NOT EXISTS sessions(sessionID char(10) not null, username varchar(128) not null, exptime char(10) not null, level varchar(32) not null, primary key(sessionID)) ENGINE InnoDB";
  $query1 = "SET FOREIGN_KEY_CHECKS=1";
  $result0 = $conn->query($query0);
  $result1 = $conn->query($queryAuth);
  $result2 = $conn->query($query1);
  $result3 = $conn->query($querySesh);
  $conn->query("delete from sessions where ".time()." > exptime");
  echo "Checking for cookies<br>";
  if(isset($_COOKIE["UPHDAS_login"]))
  {
    echo "Cookie found! Value is ". $_COOKIE["UPHDAS_login"] .".<br>";
    $cookieresult = $conn->query("Select * from sessions where sessionid = '" . $_COOKIE["UPHDAS_login"] ."'");
    if($cookieresult->num_rows != 1)
    {
      header("Location: loginstart.php");
    }
  }
  else
  {
    echo "Cookie not found.<br>";
    header("Location: loginstart.php");
  }
  #deletes old sessions

  $conn->close();
  if (!$result0 OR !$result1 OR !$result2 OR !$result3) die ("Database access failed");


?>
