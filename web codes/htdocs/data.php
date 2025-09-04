<?php
$jsonData = file_get_contents('data.json');
$data = json_decode($jsonData, true);

$speedJsonData = file_get_contents('speed.json');
$speedData = json_decode($speedJsonData, true);

$lastRowValue = $speedData['last_row_value'] ?? 'NA'; // إذا لم يكن موجودًا، يتم إرجاع 'NA'

$response = [
    'TotalVoltage' => $data['data']['TotalVoltage'] ?? 'NA',
    'TotalCurrent' => $data['data']['TotalCurrent'] ?? 'NA',
    'PowerConsumed' => $data['data']['PowerConsumed'] ?? 'NA',
    'Energy' => $data['data']['Energy'] ?? 'NA',
    'AmbientTemp' => $data['data']['AmbientTemp'] ?? 'NA',
    'MaximumInverterTemperature' => $data['data']['MaximumInverterTemperature'] ?? 'NA',
    'RightInverterTemperature' => $data['data']['RightInverterTemperature'] ?? 'NA',
    'LeftInverterTemperature' => $data['data']['LeftInverterTemperature'] ?? 'NA',
    'YawRate' => $data['data']['YawRate'] ?? 'NA',
    'SOC' => $data['data']['SOC'] ?? 'NA',
    'CarSpeedGauge' => $data['data']['CarSpeedGauge'] ?? 'NA',
    'NumberOfLabs' => $data['data']['NumberOfLabs'] ?? 'NA',
    'LastRowValue' => $lastRowValue,  
];

echo json_encode($response);
?>
