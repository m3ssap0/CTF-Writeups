<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
    <title>Not(e) accessible</title>
<!-- My source is at /src.tgz -->
    <style>
html {
  position: relative;
  min-height: 100%;
}

body {
  padding-top: 5rem;
  margin-bottom: 60px; /* Margin bottom by footer height */
}
.starter-template {
  padding: 3rem 1.5rem;
  text-align: center;
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px; /* Set the fixed height of the footer here */
  line-height: 60px; /* Vertically center the text there */
  background-color: #f5f5f5;
}
    </style>
</head>
    <body>

    <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
      <a class="navbar-brand" href="/">Not(e) accessible</a>
    </nav>

    <main role="main" class="container">

      <div class="starter-template">
        <h1>Not(e) accessible :-(</h1>
        <p class="lead">This is good service. It is not(e) accessible!</p>
      </div>
      <div class="container">
        <form method="post">
              <div class="form-group">
                <label for="note">Enter your text</label>
                <textarea class="form-control" name="note" id="note" placeholder="Your note here!" rows="3"></textarea>
              </div>
              <button type="submit" class="btn btn-primary" name="submit" value="submit">Submit note!</button>
        </form>
      </div>

<?php
    require_once "config.php";

    if(isset($_POST['submit']) && isset($_POST['note']) && $_POST['note']!="") {
        $note = $_POST['note'];

        if(strlen($note) > 1000) {
            die("ERROR! - Text too long");
        }

        if(!preg_match("/^[a-zA-Z]+$/", $note)) {
            die("ERROR! - Text does not match /^[a-zA-Z]+$/");
        }

        $id = random_int(PHP_INT_MIN, PHP_INT_MAX);
        $pw = md5($note);
        
        # Save password so that we can check it later
        file_put_contents("./pws/$id.pw", $pw); 

        file_get_contents($BACKEND . "store/" . $id . "/" . $note);

        echo '<div class="shadow-sm p-3 mb-5 bg-white rounded">';
            echo "<p>Your note ID is $id<br>";
            echo "Your note PW is $pw</p>";

            echo "<a href='/view.php?id=$id&pw=$pw'>Click here to view your note!</a>";
        echo '</div>';
    }
?>
    </main>

<footer class="footer">
      <div class="container">
        <span class="text-muted">With love from <a href="https://twitter.com/gehaxelt">@gehaxelt</a> for the 35C3 Junior CTF and ESPR :-)</span>
      </div>
</footer>


        <script src="/assets/js/jquery-3.3.1.slim.min.js"></script>
        <script src="/assets/js/popper.min.js"></script>
        <script src="/assets/js/bootstrap.min.js"></script>
    </body>
</html>
