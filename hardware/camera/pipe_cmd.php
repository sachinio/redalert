<?php
    $pipe = fopen("../../../../rpicam/FIFO","w");
    fwrite($pipe, $_GET["cmd"]);
    fclose($pipe);
