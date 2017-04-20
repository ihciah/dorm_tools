<?php
$BASE_URI = "http://your_ip:11111/opendoor?";
echo(file_get_contents($BASE_URI . $_SERVER['QUERY_STRING']));
?>
