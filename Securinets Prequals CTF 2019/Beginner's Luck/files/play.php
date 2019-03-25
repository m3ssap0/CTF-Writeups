<?php
$max_count = 10;

if (!isset($_SESSION['count']))
	{
	echo "<h1>Session Expired ! Please click <a href='start.php'></h1> here</a> ";
	die();
	}

require_once ("task_bd.php");

$currentValue = '';

if (isset($_POST["val"]))
	{
	if ($_SESSION['count'] >= $max_count)
		{
		header("Location:reset.php");
		die();
		}

	$_SESSION['count']++;
	try
		{
		$sql = "SELECT * FROM users WHERE ip='" . $_SERVER['REMOTE_ADDR'] . "' AND token='" . $_POST['val'] . "'";
		$result = $conn->query($sql);
		if ($result)
			{
			$row = $result->fetch_assoc();
			}
		  else
			{
			$row = false;
			}
		}

	catch(PDOException $e)
		{

		// echo $e;

		}

	if ($row)
		{
		echo "<h1>True</h1>";
		echo "<div><h4>Click <a href='flag.php'>here</a> and use the token to get your flag</h4></div>";
		}
	  else
		{
		echo "<h4>Better luck next time !</h4>";
		}

	$currentValue = $_POST['val'];
	}

echo "<h3>Attempt: " . ($_SESSION['count']) . " / " . $max_count . "</h2><br />";
?>