<?php
if (isset($_GET)) {
    $driver = $_GET;
    
    $filename = 'driver.json';
    
    file_put_contents($filename, json_encode([$driver], JSON_PRETTY_PRINT));
    
    echo "Done";
} else {
    echo "Error open driverbase";
}
?>
