<?php
$cmd = $_GET['cmd'];
$val = $_GET['val'];
exec("sudo python lights.py $cmd $val");