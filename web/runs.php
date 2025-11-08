<?php
if(!$_POST['id']) {
die("You need an ID");
}
$id=$_POST['id'];
$name=$_POST['name'];
$count=0;
$file=fopen("txt/".$id.".txt","r");
if ($file) {
$count=fgets($file);
fclose($file);
}
$file=fopen("txt/".$id.".txt","w+");
flock($file, LOCK_EX);
if (!$file) {
flock($file, LOCK_UN);
die("file_error");
}
$count=$count+1;
fputs($file,$count);
flock($file, LOCK_UN);
$err=fclose($file);
echo "".$count."\n";
?>