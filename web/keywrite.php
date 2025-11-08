<?php
if(!$_POST['password'] or !$_POST['value'])
{
die("error");
}
$val=$_POST["value"];
$pass=$_POST["password"];
if($pass!="item33new")
{
die("Sorry, incorrect password!");
}
file_put_contents("activation_payments.plist",$val);
?>