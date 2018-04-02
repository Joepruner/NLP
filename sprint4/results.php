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
        <img class="mainLogo" src="res/NL2CQ%20Logo.svg" alt="NL2CQ Logo">
        <main>
            <?php

            $question = $_GET["question"];

            $result = shell_exec("python Tokenize.py ". $question);
            ?>
            <h1 id="resultHeader">The Cypher Query:</h1>
            <h2 id="output"><?=$result?></h2>
        
            <a href="index.php" class="largeButton">Ask another Question</a>
        </main>
        <footer>
            <span>The Phonetics</span>
            <nav>
                <a href="about.html">About</a>
                <em> | </em>
                <a href="documentation.html">Documentation</a>
            </nav>
        </footer>
    </body>
</html>