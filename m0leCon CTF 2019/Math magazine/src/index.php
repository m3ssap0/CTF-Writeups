<?php

	require_once('config.php');
	require_once('class.php');

	$pages = [
		'home',
		'articles',
		'source',
		'ajax'
	];

	$page = @$_GET['p'] ?? $pages[0];
	if(!in_array($page, $pages))
		$page = '404';

	ob_start();
	require_once(PAGES_DIRECTORY.$page);
	$output = ob_get_clean();
?>
<!DOCTYPE html>
<html>
	<head>
		<title>WEB Medium - Math magazine - @andreossido</title>
		<?php
		if(substr($_SERVER['REMOTE_ADDR'],0,4) !== "172."){
		?>

		<!-- Bootstrap -->
		<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

		<!-- Bootstrap theme -->
		<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootswatch/4.2.1/slate/bootstrap.min.css">

		<!-- Font awesome -->
		<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.2/css/all.css">
		<?php
		}
		?>

		<!-- Custom -->
		<!-- <link rel="stylesheet" type="text/css" href="style.css"> -->
		<!-- <script type="text/javascript" src="latex.js"></script> -->
	</head>
	<body>
		<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
			<div class="container">
				<a class="navbar-brand" href="./?p=home">
					We <i class="fas fa-heart text-danger"></i> Math
				</a>
				<ul class="navbar-nav mr-auto">
					<li class="nav-item">
						<a class="nav-link" href="./?p=home">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="./?p=articles&u_id=<?=USER?>">Articles</a>
					</li>
					<!--
						<li class="nav-item">
							(Not used anymore, but I left it here for historical reasons)
							<a class="nav-link" href="./src.zip">Source</a>
						</li>
					-->
				</ul>
			</div>
		</nav>
		<div class="container">
			<br>
			<?=$output?>
		</div>
	</body>
</html>