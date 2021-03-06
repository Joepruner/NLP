 <!DOCTYPE html>
 <html>
     <head>
         <title>NL2CQ - Home</title>
         <meta charset="utf-8">
         <link rel="stylesheet" type="text/css" href="css/style.css">
     </head>
     <body>
        <header>
             <a id="nl2cqHead" href="index.php">NL2CQ</a>
        </header>
        <img class="mainLogo" src="res/NL2CQ%20Logo.svg" alt="NL2CQ Logo">
        <form action="results.php" method="get">
            <fieldset>
                <label>Ask a question:</label>
                <input id="userInput" type="text" name="question">
                <input type="submit" class="largeButton" name="submit" value="SUBMIT">
            </fieldset>
        </form>
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