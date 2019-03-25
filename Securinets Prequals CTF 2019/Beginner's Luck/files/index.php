<?php
session_start();
require_once ("bd.php");

function generateRandomToken($length)
	{
		//generate random token
	}

if (!isset($_SESSION['count']))
	{
	$_SESSION['count'] = 0;
	$pass = generateRandomToken(100);
	$ip = $_SERVER['REMOTE_ADDR'];
	$sql = "INSERT INTO users (ip, token) VALUES (?,?)";
	$stmt = $pdo->prepare($sql);
	$stmt->execute([$ip, $pass]);
	}

header("Location:play.php");