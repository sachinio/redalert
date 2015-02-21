<?php
$angle = $_GET['angle'];
$sno = $_GET['sno'];
exec("sudo ../cFiles/servo $angle $sno");
?>