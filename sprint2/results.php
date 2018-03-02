<!DOCTYPE html>
<html>
    <head>
        <title>Results</title>
        <link rel="stylesheet" type="text/css" href="css/style.css">
    </head>
    <body>
        <header>
            <h1>NL2CQ</h1>
        </header>

        <?php

        $question = $_GET["question"];

        echo  shell_exec("python index.py ".$question);

        ?>

        <footer>
            
        </footer>
    </body>
</html>