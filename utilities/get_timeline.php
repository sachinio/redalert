<?php
$f = '/var/www/tmp/timeline.csv';
$output = shell_exec("sudo python3 csv_to_json.py $f 2>&1");
echo $output;