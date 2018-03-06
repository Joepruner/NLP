 <!DOCTYPE html>
 <html>
     <head>
        <title>NL2CQ - Results</title>
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="css/style.css">
     </head>
     <body>
        <header>
            <a href="index.php"><h1>NL2CQ</h1></a>
            <a id="nl2cqHead" href="index.php">NL2CQ</a>
        </header>

        <?php

        $question = $_GET["question"];

        $result = shell_exec("python index.py ". $question);

        echo  $result;

        include "footer.html"
        ?>
    </body>
</html>