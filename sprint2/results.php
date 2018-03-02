<!DOCTYPE html>
<html>
    <head>
        <title>Results</title>
        <link rel="stylesheet" type="text/css" href="css/style.css">
    </head>
    <body>
        <header>
            <a href="index.php"><h1>NL2CQ</h1></a>
        </header>

        <?php

        $question = $_GET["question"];

        $result = shell_exec("python index.py ". $question);

        echo  $result
        ?>

        <footer>
            
        </footer>
    </body>
</html>