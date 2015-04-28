<?php
    $addr = $_GET['addr'];
    $cmd = $_GET['cmd'];
    $del = $_GET['del'];
    $bri = $_GET['bri'];
    $rgb = $_GET['rgb'];
    $tout = $_GET['tout'];
    $output = shell_exec("sudo python3 lights.py $addr $cmd $del $bri $rgb $tout 2>&1");
    echo $output;