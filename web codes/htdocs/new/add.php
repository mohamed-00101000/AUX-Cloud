<?php
if (isset($_GET)) {
    $data = $_GET;
    
    $filename = 'data.json';
    
    file_put_contents($filename, json_encode([$data], JSON_PRETTY_PRINT));
    
    echo "Done";
} else {
    echo "Error open database";
}
file_put_contents("log.txt", json_encode($_GET) . "\n", FILE_APPEND);

?>
