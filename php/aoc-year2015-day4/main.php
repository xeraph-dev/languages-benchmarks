<?php

function mineAdventCoin($secretKey)
{
    $number = 0;
    $target = "\x00\x00\x00";

    while (true) {
        $hash = md5($secretKey . $number, true);
        if (strncmp($hash, $target, 3) === 0) {
            return ['number' => $number, 'hash' => bin2hex($hash)];
        }
        $number++;
    }
}

$secretKey = 'your_secret_key';
var_dump(mineAdventCoin($secretKey));
