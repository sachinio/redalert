<?php
  $cmd = $_GET['cmd'];
  $val = $_GET['val'];
  exec("sudo python ../missile.py $cmd $val");
?>


