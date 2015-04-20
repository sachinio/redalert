<?php
  $msg = $_GET['msg'];
  exec("sudo python mona.py $msg");