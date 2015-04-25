<?php
  $msg = $_GET['msg'];
  exec("sudo python google.py $msg");