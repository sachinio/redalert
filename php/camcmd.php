<?php
$angle = $_GET['angle'];
$sno = $_GET['sno'];
$output = shell_exec("sudo ../cFiles/servo $angle $sno");
echo "HELLO $angle $sno $output";
?>