<?php
session_start();
if(isset($_SESSION['username'])) {
    header('location: index.php');
    die();
}
require_once('./db.php');

if (isset($_POST['username']) && !empty($_POST['username']) && isset($_POST['password']) && !empty($_POST['password'])) {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
    $sql = "SELECT * FROM users WHERE login='". $username ."' and password='". $password ."'";
    $res = $conn->query($sql);
    if($res->num_rows > 0) {
        $user = $res->fetch_assoc();
        $_SESSION['username'] = $user['login'];
        $_SESSION['role'] = $user['role'];
        header('location: index.php');
        die();
    } else {
        $success = false;
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
    <link rel="stylesheet" type="text/css" media="screen" href="./css/register.css" />
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

</head>
<body>
    <div class="auth-form">
        <form action="" method="post">
            <h5 style="color: gray;">Login</h5>
            <?php
                if(isset($success) && !$success) {
            ?>
                <div class="alert alert-danger">
                    <strong>Error!</strong> Bad Credentials;
                </div>
            <?php
                }
            ?>
            <input type="text" class="form-control" placeholder="Username" name="username">
            <input type="password" class="form-control" placeholder="Password" name="password">
            
            <div class="register">
                <a href="register.php">Create Account !</a>
                <input type="submit" class="btn btn-primary" value="Login">
            </div>
        </form>
    </div>
</body>
</html>