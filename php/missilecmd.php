<?php
  $cmd = $_GET['cmd'];
  $val = $_GET['val'];
  exec("sudo python ../missile/missile.py $cmd $val");
?>


