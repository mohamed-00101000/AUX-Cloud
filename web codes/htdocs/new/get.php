<?php
if (isset($_GET)) {
    $data = $_GET;
    
    $filename = 'get.json';
    
    file_put_contents($filename, json_encode([$data], JSON_PRETTY_PRINT));
    
    echo "Done";
} 
else {
    echo "Error open database";
}
?>
