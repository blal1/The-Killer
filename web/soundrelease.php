<?php
if(!$_POST['version'])
{
die("you need to specify the version ");
}
$version=$_POST['version'];
file_put_contents("soundsver.txt", $version);
echo "successfully updated the sounds";
?>