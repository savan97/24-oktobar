<?php
/**
 * Plugin Name: 24. oktobar — site tweaks
 * Description: Serbian (Latin) language attribute and translations of the few English strings the theme prints on the front end. No settings; documented in README.md.
 * Version: 1.0.0
 */

defined( 'ABSPATH' ) || exit;

/*
 * The site is written in Serbian Latin script. WordPress has no Serbian Latin
 * locale (sr_RS is Cyrillic), so the admin stays in English and the front end
 * declares its language here.
 */
add_filter(
	'language_attributes',
	static function () {
		return 'lang="sr-Latn"';
	}
);

add_filter(
	'the_seo_framework_og_locale',
	static function () {
		return 'sr_RS';
	}
);

/*
 * Front-end strings printed by Astra / WordPress in English.
 */
add_filter(
	'gettext',
	static function ( $translation, $text, $domain ) {
		if ( is_admin() || ! in_array( $domain, array( 'astra', 'default' ), true ) ) {
			return $translation;
		}
		static $map = array(
			'Skip to content'      => 'Pređi na sadržaj',
			'Main Menu'            => 'Glavni meni',
			'Site Navigation'      => 'Navigacija sajta',
			'Main menu toggle'     => 'Otvori ili zatvori meni',
			'Toggle Menu'          => 'Otvori ili zatvori meni',
			'Close Menu'           => 'Zatvori meni',
			'Menu Toggle'          => 'Otvori ili zatvori meni',
			'Mobile Menu'          => 'Meni',
			'Scroll to Top'        => 'Na vrh stranice',
			'Search for:'          => 'Pretraga:',
			'Search &hellip;'      => 'Pretraga…',
			'Search'               => 'Pretraga',
			'Page Not Found'       => 'Stranica nije pronađena',
			'This page doesn\'t seem to exist.' => 'Ova stranica ne postoji.',
			'It looks like the link pointing here was faulty. Maybe try searching?' => 'Izgleda da je link neispravan. Pokušajte sa pretragom ili se vratite na početnu stranu.',
		);
		return isset( $map[ $text ] ) ? $map[ $text ] : $translation;
	},
	10,
	3
);
