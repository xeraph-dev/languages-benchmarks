<?php

function mineAdventCoin($secretKey)
{
    $number = 0;

    while (true) {
        $hash = md5($secretKey . $number);
        if (substr($hash, 0, 6) === "000000") {
            return $number;
        }
        $number++;
    }
}

$secretKey = 'yzbqklnj';
$answer = mineAdventCoin($secretKey);
echo "The lowest number is: " . $answer;
