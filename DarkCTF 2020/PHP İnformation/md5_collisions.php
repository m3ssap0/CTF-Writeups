<?php

$hex1 = '4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2';
$hex2 = '4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2';

$bin1 = hex2bin($hex1);
$bin2 = hex2bin($hex2);

if ($bin1 == $bin2)
	echo 'The binary data is the same' . PHP_EOL;
else 
	echo 'The binary data is not the same' . PHP_EOL . PHP_EOL;

$md51 = md5($bin1);
$md52 = md5($bin2);

echo 'MD5 hash for binary #1: ' . $md51 . PHP_EOL;
echo 'MD5 hash for binary #2: ' . $md52 . PHP_EOL;

if ($md51 == $md52)
	echo 'The MD5 hashes are the same' . PHP_EOL;
else 
	echo 'The MD5 hashes are not the same' . PHP_EOL;

$urlencoded1 = urlencode($bin1);
$urlencoded2 = urlencode($bin2);
echo PHP_EOL;
echo 'The urlencoded #1 is: '. $urlencoded1 . PHP_EOL;
echo 'The urlencoded #2 is: '. $urlencoded2 . PHP_EOL;