<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'xiaofeng_wp323');

/** MySQL database username */
define('DB_USER', 'xiaofeng_wp323');

/** MySQL database password */
define('DB_PASSWORD', '57P5Swj7jh');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'l39v8gwuihi1pxovsdumad7ytmpa25qg6piesew9kch36hjauicrajdqtkjidmbn');
define('SECURE_AUTH_KEY',  'gftnmm1fu0nyi2lwj2r7e2mtvq2osp857xbaqmygq7qn3vgihua7knluj7l8ttnl');
define('LOGGED_IN_KEY',    '5slwxb4cbnmldzf9lfnjmlixfhgeea0r6y2phdpohu90rlkfagef5kefjfpqn57f');
define('NONCE_KEY',        'iz7evofersetjhwbg4muborfrgn5jeg8psy5gdwzsad4hvwbklz6qvhuznozykcb');
define('AUTH_SALT',        'tt1jxkyikwox25r2tjzxwgkbvumwulfj7u3babzpl1dx4zgap6up9xuj02gukrzh');
define('SECURE_AUTH_SALT', '90pkewmsxdnqmpbj7u3nzojd3bnpycvb8g5xye756odigon4ykxywxwpxe7iko13');
define('LOGGED_IN_SALT',   '0wtwrosowxoe09btxeekvsujhreea885notvql6q8du5cjqodg5kjdwd1y1klvhq');
define('NONCE_SALT',       'yphde9y26ebfvsrlro3tmyj80ujdja2lekrhfxdrf8rbqwnzbdxfo7rwesun7pr3');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress.  A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de_DE.mo to wp-content/languages and set WPLANG to 'de_DE' to enable German
 * language support.
 */
define ('WPLANG', 'zh_CN');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
