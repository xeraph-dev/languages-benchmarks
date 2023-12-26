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

$secretKey = 'yzbqklnj';
var_dump(mineAdventCoin($secretKey));
