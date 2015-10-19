<?php
    $angle = escapeshellarg($_GET['angle']);
    $sno = escapeshellarg($_GET['sno']);
    $del = escapeshellarg($_GET['del']);
    $output = shell_exec("sudo ./servo $angle $sno $del 2>&1");
    echo $output;
