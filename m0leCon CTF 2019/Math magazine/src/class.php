<?php

	require_once('config.php');

	class CustomSerializable {
		public function __serialize(){ return md5(serialize($this)); }
		public static function __unserialize($v){ return unserialize(md5($v)); }
	}

	class Article extends CustomSerializable {
		private $author;
		private $is_admin = false;
		private $title = '';
		private $text = '';

		public function getAuthor(){ return $this->author; }
		public function getTitle(){ return base64_decode($this->title); }
		public function getText(){ return base64_decode($this->text); }

		public function setAuthor($v){ $this->author = $v; }
		public function setTitle($v){ $this->title = base64_encode($v); }
		public function setText($v){ $this->text = base64_encode($v); }

		public function isAdmin($v=null){ if($v !== null) $this->is_admin = $v; return $this->is_admin; }

		public function serialize(){ return serialize($this); }
		public static function unserialize($v){ return unserialize($v); }
	}

	class ArticleFactory {
		private $user = null;
		private $articles = [];

		function getUser(){ return $this->user; }
		function getUserDirectory(){ return ARTICLE_DIRECTORY.$this->getUser().'/'; }
		function getUserfile(){ return $this->getUserDirectory().$this->getUser(); }
		function getArticles(){ return $this->articles; }

		function setUser($v){ $this->user = $v; }
		function setArticles($v){ $this->articles = $v; }
		function addArticle($v){ $v->setAuthor($this->getUser()); $this->articles[] = $v; }

		function getLatexByArticleIndex($id){ return $this->getUserDirectory().md5($id); }

		function fetch(){
			$file = fopen($this->getUserfile(), "r");
			if($articles = unserialize(base64_decode(fread($file, filesize($this->getUserfile())))))
				$this->setArticles($articles);
			fclose($file);
		}

		function store(){
			$file = fopen($this->getUserfile(), "w");
			fwrite($file, base64_encode(serialize($this->getArticles())));
			fclose($file);
		}

		function __construct($user){
			$this->setUser($user);

			if(!file_exists(ARTICLE_DIRECTORY))
				mkdir(ARTICLE_DIRECTORY);

			if(!file_exists($this->getUserDirectory()))
				mkdir($this->getUserDirectory());

			if(!file_exists($this->getUserfile()))
				$this->store();

			$this->fetch();
		}
	}

?>