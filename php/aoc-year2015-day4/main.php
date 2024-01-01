<?php

$secret = $argv[1];
$zeros = $argv[2];


$half = $zeros / 2;
$bytes_count = ceil($half);
$number = 0;
$target = str_repeat("\x00", $bytes_count - 1);
$target .= $half == $bytes_count ? "\x00" : "\x0F";

$hash = md5($secret . 282749, true);

while (true) {
    $hash = md5($secret . $number, true);
    if (strncmp($hash, $target, $bytes_count) <= 0) {
        break;
    }
    $number++;
}

echo $number;
