<?php
    $on = $_GET['on'];
    if($on === '1'){
        $output = shell_exec("sudo raspimjpeg 2>&1");
    }else{
        $output = shell_exec("sudo pkill raspimjpeg 2>&1");
    }
    echo $output;