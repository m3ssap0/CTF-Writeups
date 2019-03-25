<?php
session_start();
require_once('./db.php');
if(!isset($_SESSION['username'])) {
    header('location: login.php');
    die();
}

if (isset($_POST['post']) && isset($_POST['title'])) {
    if(!empty($_POST['post']) && !empty($_POST['title'])) {
        $success = true;
        $post = mysqli_real_escape_string($conn, $_POST['post']);
        $title = mysqli_real_escape_string($conn, $_POST['title']);
        $sql = "INSERT INTO posts (title, content, date, author) VALUES ('". $title ."', '". $post ."', CURDATE(), '". $_SESSION['username'] ."')";
        try {
            $conn->query($sql);
        } catch(Exception $err) {
            echo 'err: '.$err;
            $success = false;
        }
    } else {
        $success = false;
    }

    if($success) {
        $_SESSION['message'] = "<div class=\"alert alert-success\">
            <strong>Success!</strong> Your post has been saved!
        </div>";
    }
}
if (isset($_POST['post_author'])) {
    $sql = "SELECT * FROM posts WHERE author = '". mysqli_real_escape_string($conn, $_POST['post_author']) ."'";
    try {
        $posts = $conn->query($sql);
    } catch(Exception $err) {
        echo 'err: '.$err;
    }
} else {
    $sql = "SELECT * FROM posts WHERE author = '". $_SESSION['username'] ."'";
    try {
        $posts = $conn->query($sql);
    } catch(Exception $err) {
        echo 'err: '.$err;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Sign up</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="./css/index.css" />
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
<a class="navbar-brand" href="#">Welcome <strong><?php echo $_SESSION['username']; ?></strong></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
      <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="flags.php">Flags</a>
      </li>
    </ul>
    <!-- <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form> -->
    <a href="logout.php">
        Logout
    </a>
  </div>
</nav>

<div class="content">
<?php
if(isset($_SESSION['message']) && $_SESSION['message']) {
    echo $_SESSION['message'];
    $_SESSION['message'] = null;
}
?>
<div>
    <form class="post-form" action="" method="post">
        <input class="form-control" placeholder="Title" name="title" style="margin-bottom: 10px;" />
        <textarea class="form-control" placeholder="Express yourself ..." name="post"></textarea>
        <input type="submit" class="btn btn-primary post-btn" value="Post">
    </form>
</div>
<h5 style="color: gray;">Find Posts</h5>
<form class="post-search" action="" method="post">
    <input class="form-control" placeholder="username" style="width: 250px;" name="post_author" value="<?php echo $_POST['post_author'] ?>"/> 
    <button class="btn btn-outline-success" type="submit"> Find </button>
</form>
<?php
echo "<h5 class=\"results-count\">Results: $posts->num_rows</h5>";
if($posts->num_rows > 0) {
    while($post = $posts->fetch_assoc()) {
?>
    <div style="padding-bottom: 20px">
        <div>
            <h5 style="display: inline"> <?php echo $post['title'] ?></h5>
            <h6 class="float-right"> <?php echo $post['date'] ?></h6>
        </div>
        <h6> <?php echo $post['content'] ?></h6>
        <div class="float-right"> By: <?php echo $post['author'] ?> </div>
    </div>
    <hr/>
<?php
    }
}
?>
</div>
</body>
</html>