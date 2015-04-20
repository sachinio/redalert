<?php
  $name = $_GET['name'];
  exec("sudo pkill omxplayer");
  $output = shell_exec("sudo omxplayer $name 2>&1");
  echo $output