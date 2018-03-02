import sys

sysin = sys.argv[1:]

str = " ".join(sysin)

print str


<?php

$question = $_GET["question"];

$result = shell_exec("python index.py ". $question);

echo  $result
?>