<?php
    $angle = $_GET['angle'];
    $sno = $_GET['sno'];
    $del = $_GET['del'];
    $output = shell_exec("sudo ./servo $angle $sno $del 2>&1");
    echo $output;