<?php
    $angle = $_GET['angle'];
    $sno = $_GET['sno'];
    $output = shell_exec("sudo ./servo $angle $sno 2>&1");
    echo $output;