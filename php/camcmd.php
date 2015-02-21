<?php
$angle = $_GET['angle'];
$sno = $_GET['sno'];
exec("sudo /home/pi/code/cInterfaces/servo $angle $sno");