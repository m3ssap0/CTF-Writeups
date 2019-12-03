<?php

$data = @$_POST['content'] ?? null;

if($data === null || $data == '' || empty($data))
	return 'ERROR: No data to publish.';

if(preg_match("(input|include)", $data))
	return 'ERROR: Commands not allowed.';

if(substr_count('href', $data) == 0)
	return 'ERROR: No source specified.';
if(substr_count('href', $data) > 1)
	return 'ERROR: To many sources specified.';

?>