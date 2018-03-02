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

        echo  shell_exec("python index.py ".$question);

        ?>

         <footer>
            <span>The Phonetics</span>
            <nav>
                <a href="about.html">About</a>
                <em> | </em>
                <a href="contact.html">Contact</a>
                <em> | </em>
                <a href="documentation.html">Documentation</a>
            </nav>
         </footer>
    </body>
</html>