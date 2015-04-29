<?php
  $msg = $_GET['msg'];
  exec("sudo python3 text_to_speech.py $msg");