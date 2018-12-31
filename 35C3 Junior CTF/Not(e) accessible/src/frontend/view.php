<?php header("Content-Type: text/plain"); ?>
<?php 
    require_once "config.php";
    if(isset($_GET['id']) && isset($_GET['pw'])) {
        $id = $_GET['id'];
        if(file_exists("./pws/" . (int) $id . ".pw")) {
            if(file_get_contents("./pws/" . (int) $id . ".pw") == $_GET['pw']) {
                echo file_get_contents($BACKEND . "get/" . $id);
            } else {
                die("ERROR!");
            }
        } else {
            die("ERROR!");
        }
    }
?>