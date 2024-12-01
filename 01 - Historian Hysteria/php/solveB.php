<?php

namespace AoC\One;

use AoC\Common\InputLoader;
use AoC\Common\Logger;

require_once __DIR__ . '/../../common/php/autoload.php';

$logger = new Logger();

$inputPairs = (new InputLoader(__DIR__))->getAsIntArrays();

$listA = [];
$listB = [];
foreach ($inputPairs as [$aItem, $bItem]) {
    $listA[]= $aItem;
    $listB[]= $bItem;
}

$bFreq = [];
foreach ($listB as $bItem) {
    if (!isset($bFreq[$bItem])) {
        $bFreq[$bItem] = 0;
    }
    $bFreq[$bItem]++;
}

$similarityTotal = 0;
foreach ($listA as $aItem) {
    $simScore = ($bFreq[$aItem] ?? 0) * $aItem;
    $logger->log("Score for $aItem is $simScore");
    $similarityTotal += $simScore;
}

echo $similarityTotal . "\n";
