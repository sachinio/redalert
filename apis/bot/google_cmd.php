<?php
  $msg = $_GET['msg'];
  exec("sudo python3 google.py $msg");