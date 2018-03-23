 <!DOCTYPE html>
 <html>
     <head>
        <title>NL2CQ - Results</title>
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="css/style.css">
     </head>
     <body>
        <header>
            <a id="nl2cqHead" href="index.php">NL2CQ</a>
        </header>

        <?php

        $question = $_GET["question"];

        $result = shell_exec("python Tokenize.py ". $question);
?>
        <h1 id="resultHeader">The current output is:</h1>
       <h2 id="output"><?=$result?></h2>
        <div style="width: 100%;">
            <a href="index.php" class="largeButton" style="margin-left: 37.5%">Ask another Question</a>
        </div>
        <p>NL2CQ V1.2 will be released soon... </p>
        <?php
        include "footer.html"
        ?>
    </body>
</html>