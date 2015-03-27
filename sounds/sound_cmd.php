<?php
  $name = $_GET['name'];
  exec("sudo pkill omxplayer");
  exec("sudo omxplayer $name");