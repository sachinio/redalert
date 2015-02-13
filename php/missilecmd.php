<?php
  $cmd = $_GET['cmd'];
  $val = $_GET['val'];
  exec("sudo python ../redalert/missile.py $cmd $val");
?>


