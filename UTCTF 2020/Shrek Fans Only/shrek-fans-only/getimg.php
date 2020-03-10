<?php
header("Content-Type: image/jpg");
readfile(base64_decode($_GET['img']));
?>
