<?php
if(!$_POST['password'])
{
die("No password provided!");
}
$pass=$_POST["password"];
if($pass!="moneyisgoodforyouTK7727007")
{
die("Sorry, incorrect password!");
}
echo file_get_contents("activation_payments.plist");
?>