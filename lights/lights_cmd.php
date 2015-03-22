<?php
$addr = $_GET['addr'];
$cmd = $_GET['cmd'];
$del = $_GET['del'];
$bri = $_GET['bri'];
$rgb = $_GET['rgb'];
$tout = $_GET['tout'];
exec("sudo python lights.py $addr $cmd $del $bri $rgb $tout");