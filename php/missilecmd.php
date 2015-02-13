<?php
  $cmd = $_GET['cmd'];
  $val = $_GET['val'];
  exec("sudo python /home/pi/code/redalert/missile.py $cmd $val");
?>


