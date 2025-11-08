<?php
$what=$_POST['what'];
if($what=="")
{
die("you need to enter a new text in order to update the reason");
}
file_put_contents("sdown.txt", $what);
echo "Success";
?>