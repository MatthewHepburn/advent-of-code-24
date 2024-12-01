<?php

namespace AoC\One;

use AoC\Common\InputLoader;
use AoC\Common\Logger;

require_once __DIR__ . '/../../common/php/autoload.php';

$logger = new Logger();

$inputPairs = (new InputLoader(__DIR__))->getAsIntArrays();
$logger->log("InputPairs = " . json_encode($inputPairs));

$listA = [];
$listB = [];
foreach ($inputPairs as [$aItem, $bItem]) {
    $listA[]= $aItem;
    $listB[]= $bItem;
}

$logger->log("List A = " . json_encode($listA));
$logger->log("List B = " . json_encode($listB));


sort($listA);
sort($listB);

if (count($listA) !== count($listB)) {
    throw new \Exception('Mismatch in array lengths');
}

$totalDifference = 0;
for($i = 0; $i < count($listA); $i++) {
    $aItem = $listA[$i];
    $bItem = $listB[$i];
    $diff = abs($aItem - $bItem);
    $logger->log("Difference between $aItem and $bItem = $diff");
    $totalDifference += $diff;
}

echo $totalDifference . "\n";
