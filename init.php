<?php
  require_once 'login.php';
  $conn = new mysqli($hn, $un, $pw, $db);
  if ($conn->connect_error) die("Fatal Error");
  $query0 = "SET FOREIGN_KEY_CHECKS=0";
  $queryAuth = "CREATE TABLE IF NOT EXISTS authentication(username varchar(128) not null, password varchar(128) not null, level varchar(32) not null, primary key(username)) ENGINE InnoDB";
  $query1 = "SET FOREIGN_KEY_CHECKS=1";
  $result0 = $conn->query($query0);
  $result1 = $conn->query($queryAuth);
  $result2 = $conn->query($query1);
  if (!$result0 OR !$result1 OR !$result2) die ("Database access failed");
  else die("Table authentication created successfully");
 ?>
