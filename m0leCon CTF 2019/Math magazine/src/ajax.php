<?php

require_once('config.php');
require_once('class.php');

$_POST = json_decode(file_get_contents('php://input'), true);
$title = $_POST['title'] ?? null;
$data = $_POST['content'] ?? null;

# echo '<pre>'.var_dump($_SERVER).'</pre>';


if($title === null || $title == '' || empty($title))
	die( 'ERROR: No title.');

if($data === null || $data == '' || empty($data))
	die( 'ERROR: No data to publish.');

$f = new ArticleFactory(USER);

$latexFilename = $f->getLatexByArticleIndex(count($f->getArticles()));
$latexFile = fopen($latexFilename.'.tex', "w");
fwrite($latexFile, $data);
fclose($latexFile);
$output = shell_exec('cd "'.$f->getUserDirectory().'" && latex --shell-escape '.$latexFilename.'.tex');

@unlink('texput.log');
@unlink($latexFilename.'.aux');
@unlink($latexFilename.'.log');
@unlink($latexFilename.'.pdf');

if(preg_match("(error)", strtolower($output))){
	@unlink($latexFilename.'.tex');
	die('ERROR: Error executing program.<hr><pre>'.$output.'</pre>');
}

if(preg_match("(input|include|location|\[|\])", $data))
	die( 'ERROR: Commands not allowed.');


$article = new Article();
$article->setAuthor(USER);
$article->setTitle($title);
$article->setText($data);

$f->addArticle($article);

$f->store();

$output = shell_exec('./bot.py "'.URL_ROOT.'/?p=articles&a=view&u_id='.USER.'&id='.(count($f->getArticles())-1).'" 2>&1');

if(empty($output) || preg_match("(error)", strtolower($output)))
	die('WARN: Published, but admin cannot view you article :(<br>'.str_replace("\n", '<br>', $output));

die('OK: published!<br><br>Admin says:<br>'.str_replace("\n", '<br>', $output));

?>