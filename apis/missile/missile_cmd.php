<?php
  $cmd = $_GET['cmd'];
  $val = $_GET['val'];
  $output = shell_exec("sudo python3 missile.py $cmd $val 2>&1");
  echo $output;


