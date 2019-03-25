<?php

session_start();
session_unset(); 
session_destroy();
require_once("bd.php");
		$sql = 'DELETE FROM users '
                . 'WHERE ip = ?';
 
        $stmt = $pdo->prepare($sql);

        $stmt->execute([$_SERVER['REMOTE_ADDR']]);
?>
