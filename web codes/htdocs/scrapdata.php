<?php
$url = "https://projectegypt.online/scrap.php";

echo "Fetching the URL every 5 seconds. Press Ctrl+C to stop.\n";

while (true) {
    try {
        // Fetch the URL content using file_get_contents
        $response = file_get_contents($url);

        // Check if the response is valid
        if ($response === false) {
            echo "Failed to fetch the URL: $url\n";
        } else {
            // Print success message
            echo "Fetched URL: $url | Content Length: " . strlen($response) . "\n";
        }

        // Wait for 5 seconds
        sleep(5);
    } catch (Exception $e) {
        // Handle exceptions
        echo "Error: " . $e->getMessage() . "\n";
    }
}
