<?php
/**
 * One-shot, re-runnable site setup for 24. oktobar.
 *
 *   python build/pages.py
 *   wp eval-file build/import.php
 *   wp elementor flush-css
 *
 * Creates or updates the pages (matched by slug) and configures the theme. It never deletes content:
 * the default "Hello world!" post and "Sample Page" are moved to the trash, where they can be restored.
 */

defined( 'ABSPATH' ) || exit( 'Run with: wp eval-file build/import.php' );

require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$dir      = __DIR__;
$root     = dirname( $dir );
$manifest = json_decode( file_get_contents( "$dir/out/manifest.json" ), true );

function t24_log( $msg ) {
	echo $msg, "\n";
}

/* ------------------------------------------------------------------ media */
function t24_media( $file, $title, $alt ) {
	$name     = basename( $file );
	$existing = get_posts(
		array(
			'post_type'   => 'attachment',
			'meta_key'    => '_t24_source',
			'meta_value'  => $name,
			'numberposts' => 1,
		)
	);
	if ( $existing ) {
		return $existing[0]->ID;
	}
	$tmp = wp_tempnam( $name );
	copy( $file, $tmp );
	$id = media_handle_sideload( array( 'name' => $name, 'tmp_name' => $tmp ), 0, $title );
	if ( is_wp_error( $id ) ) {
		t24_log( 'Media error: ' . $id->get_error_message() );
		return 0;
	}
	update_post_meta( $id, '_wp_attachment_image_alt', $alt );
	update_post_meta( $id, '_t24_source', $name );
	return $id;
}

$logo_id  = t24_media( "$dir/assets/24-oktobar-logo.png", '24. Oktobar — logo', '24. Oktobar' );
$logo_w   = t24_media( "$dir/assets/24-oktobar-logo-beli.png", '24. Oktobar — logo, beli', '24. Oktobar' );
$icon_id  = t24_media( "$dir/assets/24-oktobar-ikonica.png", '24. Oktobar — ikonica sajta', '' );
t24_log( "media: logo $logo_id, logo white $logo_w, icon $icon_id" );

/* ------------------------------------------------------------------ general options */
update_option( 'blogname', '24. Oktobar d.o.o.' );
update_option( 'blogdescription', 'Gasovodi, mreže i grubi građevinski radovi — Novi Sad' );
update_option( 'timezone_string', 'Europe/Belgrade' );
update_option( 'date_format', 'd.m.Y.' );
update_option( 'time_format', 'H:i' );
update_option( 'start_of_week', 1 );
update_option( 'default_comment_status', 'closed' );
update_option( 'default_ping_status', 'closed' );
update_option( 'site_icon', $icon_id );

foreach ( array( 'hello-world' => 'post', 'sample-page' => 'page' ) as $slug => $type ) {
	$p = get_page_by_path( $slug, OBJECT, $type );
	if ( $p && 'trash' !== $p->post_status ) {
		wp_trash_post( $p->ID );
		t24_log( "trashed default $type '$slug'" );
	}
}

/* ------------------------------------------------------------------ Elementor */
update_option( 'elementor_disable_color_schemes', 'yes' );
update_option( 'elementor_disable_typography_schemes', 'yes' );
update_option( 'elementor_local_google_fonts', '1' );
update_option( 'elementor_cpt_support', array( 'page' ) );
update_option( 'elementor_font_display', 'swap' );

$kit_id = (int) get_option( 'elementor_active_kit' );
$kit    = (array) get_post_meta( $kit_id, '_elementor_page_settings', true );
$typo   = function ( $family, $weight, $size = null, $lh = null, $size_m = null ) {
	$t = array(
		'typography_typography'  => 'custom',
		'typography_font_family' => $family,
		'typography_font_weight' => $weight,
	);
	if ( $size ) {
		$t['typography_font_size'] = array( 'unit' => 'px', 'size' => $size, 'sizes' => array() );
	}
	if ( $size_m ) {
		$t['typography_font_size_mobile'] = array( 'unit' => 'px', 'size' => $size_m, 'sizes' => array() );
	}
	if ( $lh ) {
		$t['typography_line_height'] = array( 'unit' => 'em', 'size' => $lh, 'sizes' => array() );
	}
	return $t;
};
$prefixed = function ( $prefix, $arr ) {
	$out = array();
	foreach ( $arr as $k => $v ) {
		$out[ $prefix . $k ] = $v;
	}
	return $out;
};
$kit = array_merge(
	$kit,
	array(
		'system_colors'       => array(
			array( '_id' => 'primary', 'title' => 'Primarna (grafit)', 'color' => '#1C1D1B' ),
			array( '_id' => 'secondary', 'title' => 'Crvena za tekst i dugmad', 'color' => '#A92D3D' ),
			array( '_id' => 'text', 'title' => 'Tekst', 'color' => '#1C1D1B' ),
			array( '_id' => 'accent', 'title' => 'Crvena iz logotipa', 'color' => '#D34053' ),
		),
		'custom_colors'       => array(
			array( '_id' => 't24sand', 'title' => 'Pesak (osnovna pozadina)', 'color' => '#F2EEE6' ),
			array( '_id' => 't24paper', 'title' => 'Papir (druga pozadina)', 'color' => '#FAF8F4' ),
			array( '_id' => 't24line', 'title' => 'Linije', 'color' => '#D8D0C2' ),
			array( '_id' => 't24ink2', 'title' => 'Sekundarni tekst', 'color' => '#4A4741' ),
		),
		'system_typography'   => array(
			array_merge( array( '_id' => 'primary', 'title' => 'Naslovi' ), $typo( 'Archivo Narrow', '700' ) ),
			array_merge( array( '_id' => 'secondary', 'title' => 'Podnaslovi' ), $typo( 'Archivo Narrow', '600' ) ),
			array_merge( array( '_id' => 'text', 'title' => 'Tekst' ), $typo( 'Archivo', '400' ) ),
			array_merge( array( '_id' => 'accent', 'title' => 'Akcenat' ), $typo( 'Archivo', '500' ) ),
		),
		'custom_typography'   => array(
			array_merge( array( '_id' => 't24mono', 'title' => 'Oznake (mono)' ), $typo( 'IBM Plex Mono', '500', 13 ) ),
		),
		'body_background_background' => 'classic',
		'body_background_color'      => '#F2EEE6',
		'body_color'                 => '#1C1D1B',
		'link_normal_color'          => '#A92D3D',
		'link_hover_color'           => '#1C1D1B',
		'container_width'            => array( 'unit' => 'px', 'size' => 1240, 'sizes' => array() ),
		'container_padding'          => array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '0', 'left' => '0', 'isLinked' => true ),
		'space_between_widgets'      => array( 'unit' => 'px', 'size' => 16, 'column' => '16', 'row' => '16', 'isLinked' => true ),
		'site_name'                  => '24. Oktobar d.o.o.',
		'site_description'           => get_option( 'blogdescription' ),
	),
	$prefixed( 'body_', $typo( 'Archivo', '400', 17, 1.6, 16 ) ),
	$prefixed( 'h1_', $typo( 'Archivo Narrow', '700', 64, 1.02, 40 ) ),
	$prefixed( 'h2_', $typo( 'Archivo Narrow', '700', 44, 1.08, 32 ) ),
	$prefixed( 'h3_', $typo( 'Archivo Narrow', '600', 26, 1.2, 22 ) ),
	$prefixed( 'h4_', $typo( 'Archivo Narrow', '600', 20, 1.25 ) )
);
update_post_meta( $kit_id, '_elementor_page_settings', $kit );
t24_log( "elementor kit $kit_id updated" );

/* ------------------------------------------------------------------ pages */
$ids = array();
foreach ( $manifest as $i => $m ) {
	$data = file_get_contents( "$dir/out/{$m['slug']}.json" );
	$page = get_page_by_path( $m['slug'] );
	$args = array(
		'post_type'    => 'page',
		'post_status'  => 'publish',
		'post_title'   => $m['title'],
		'post_name'    => $m['slug'],
		'menu_order'   => $i,
		'post_content' => '',
	);
	if ( $page ) {
		$args['ID'] = $page->ID;
		$id         = wp_update_post( $args );
	} else {
		$id = wp_insert_post( $args );
	}
	update_post_meta( $id, '_wp_page_template', 'elementor_header_footer' );
	// Astra: full-width stretched layout, no title/sidebar (what Astra sets when a page is opened in Elementor)
	update_post_meta( $id, 'ast-site-content-layout', 'full-width-container' );
	update_post_meta( $id, 'site-content-style', 'unboxed' );
	update_post_meta( $id, 'site-sidebar-layout', 'no-sidebar' );
	update_post_meta( $id, 'site-post-title', 'disabled' );
	update_post_meta( $id, 'ast-title-bar-display', 'disabled' );
	update_post_meta( $id, 'ast-featured-img', 'disabled' );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_elementor_template_type', 'wp-page' );
	update_post_meta( $id, '_elementor_version', ELEMENTOR_VERSION );
	update_post_meta( $id, '_elementor_data', wp_slash( $data ) );
	delete_post_meta( $id, '_elementor_css' );
	delete_post_meta( $id, '_elementor_element_cache' );
	// The SEO Framework
	update_post_meta( $id, '_genesis_title', $m['seo_title'] );
	update_post_meta( $id, '_genesis_description', $m['seo_desc'] );
	update_post_meta( $id, '_tsf_title_no_blogname', 1 );
	$ids[ $m['slug'] ] = $id;
	t24_log( "page {$m['slug']} => $id" );
}

/* Elementor renders from _elementor_data; post_content gets a plain-text copy so search and feeds are not empty. */
foreach ( $ids as $slug => $id ) {
	$doc = \Elementor\Plugin::$instance->documents->get( $id, false );
	if ( $doc ) {
		$plain = $doc->get_content();
		$plain = wp_strip_all_tags( preg_replace( '#<(svg|style|script)\b.*?</\1>#s', '', $plain ) );
		wp_update_post( array( 'ID' => $id, 'post_content' => trim( preg_replace( '/\s+/', ' ', $plain ) ) ) );
	}
}

update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $ids['pocetna'] );
update_option( 'page_for_posts', 0 );

/* ------------------------------------------------------------------ menu */
$menu_name = 'Glavni meni';
$menu      = wp_get_nav_menu_object( $menu_name );
$menu_id   = $menu ? $menu->term_id : wp_create_nav_menu( $menu_name );
foreach ( (array) wp_get_nav_menu_items( $menu_id ) as $item ) {
	wp_delete_post( $item->ID, true ); // rebuild the menu items (menu itself is kept)
}
foreach ( array( 'delatnosti', 'reference', 'mehanizacija', 'o-nama', 'kontakt' ) as $pos => $slug ) {
	wp_update_nav_menu_item(
		$menu_id,
		0,
		array(
			'menu-item-object-id' => $ids[ $slug ],
			'menu-item-object'    => 'page',
			'menu-item-type'      => 'post_type',
			'menu-item-status'    => 'publish',
			'menu-item-position'  => $pos + 1,
		)
	);
}
$locations                 = (array) get_theme_mod( 'nav_menu_locations', array() );
$locations['primary']      = $menu_id;
$locations['mobile_menu']  = $menu_id;
set_theme_mod( 'nav_menu_locations', $locations );
set_theme_mod( 'custom_logo', $logo_id );
t24_log( "menu $menu_id assigned" );

/* ------------------------------------------------------------------ Astra */
$astra = (array) get_option( 'astra-settings', array() );
$empty_row5 = function ( $prefix ) {
	$r = array();
	foreach ( array( '_left', '_left_center', '_center', '_right_center', '_right' ) as $s ) {
		$r[ $prefix . $s ] = array();
	}
	return $r;
};
$hd                   = array(
	'popup'   => array( 'popup_content' => array( 'mobile-menu' ) ),
	'above'   => $empty_row5( 'above' ),
	'primary' => $empty_row5( 'primary' ),
	'below'   => $empty_row5( 'below' ),
);
$hd['primary']['primary_left']  = array( 'logo' );
$hd['primary']['primary_right'] = array( 'menu-1', 'button-1' );
$hm = array(
	'popup'   => array( 'popup_content' => array( 'mobile-menu', 'button-1' ) ),
	'above'   => array( 'above_left' => array(), 'above_center' => array(), 'above_right' => array() ),
	'primary' => array( 'primary_left' => array( 'logo' ), 'primary_center' => array(), 'primary_right' => array( 'html-1', 'mobile-trigger' ) ),
	'below'   => array( 'below_left' => array(), 'below_center' => array(), 'below_right' => array() ),
);
$fd = array(
	'above'   => array( 'above_1' => array(), 'above_2' => array(), 'above_3' => array(), 'above_4' => array(), 'above_5' => array() ),
	'primary' => array( 'primary_1' => array( 'widget-1' ), 'primary_2' => array( 'widget-2' ), 'primary_3' => array( 'widget-3' ), 'primary_4' => array(), 'primary_5' => array() ),
	'below'   => array( 'below_1' => array( 'copyright' ), 'below_2' => array(), 'below_3' => array(), 'below_4' => array(), 'below_5' => array() ),
);
$astra = array_merge(
	$astra,
	array(
		'header-desktop-items'              => $hd,
		'header-mobile-items'               => $hm,
		'mobile-header-type'                => 'dropdown',
		'ast-header-responsive-logo-width'  => array( 'desktop' => 200, 'tablet' => 170, 'mobile' => 140 ),
		'display-site-title-responsive'     => array( 'desktop' => 0, 'tablet' => 0, 'mobile' => 0 ),
		'display-site-tagline-responsive'   => array( 'desktop' => 0, 'tablet' => 0, 'mobile' => 0 ),
		'hb-header-height'                  => array( 'desktop' => 92, 'tablet' => 76, 'mobile' => 68 ),
		'header-button1-text'               => '+381 21 47 41 048',
		'header-button1-link-option'        => array( 'url' => 'tel:+381214741048', 'new_tab' => false, 'link_rel' => '' ),
		'header-html-1'                     => '<a class="t-mobile-call" href="tel:+381214741048">Pozovite</a>',
		'footer-desktop-items'              => $fd,
		'hb-footer-column'                  => '3',
		'hb-footer-layout'                  => array( 'desktop' => '3-equal', 'tablet' => '3-equal', 'mobile' => 'full' ),
		'hb-footer-main-sep'                => 0,
		'hbb-footer-separator'              => 0,
		'footer-copyright-editor'           => '© [current_year] Građevinsko preduzeće „24. Oktobar“ d.o.o., Novi Sad',
		'footer-copyright-alignment'        => array( 'desktop' => 'left', 'tablet' => 'left', 'mobile' => 'left' ),
		'scroll-to-top-enable'              => false,
		'site-content-width'                => 1240,
		'ast-site-content-layout'           => 'full-width-container',
		'site-content-style'                => 'unboxed',
		'single-page-sidebar-layout'        => 'no-sidebar',
		'site-sidebar-layout'               => 'no-sidebar',
	)
);
update_option( 'astra-settings', $astra );

$palettes = get_option( 'astra-color-palettes' );
if ( ! is_array( $palettes ) && class_exists( 'Astra_Global_Palette' ) ) {
	$palettes = Astra_Global_Palette::get_default_color_palette();
}
$palettes['currentPalette']          = 'palette_1';
$palettes['palettes']['palette_1'] = array( '#A92D3D', '#1C1D1B', '#1C1D1B', '#1C1D1B', '#F2EEE6', '#FAF8F4', '#1C1D1B', '#D8D0C2', '#141513' );
update_option( 'astra-color-palettes', $palettes );
t24_log( 'astra configured' );

/* ------------------------------------------------------------------ footer widgets */
$blocks   = (array) get_option( 'widget_block', array() );
$sidebars = (array) get_option( 'sidebars_widgets', array() );
$footer   = array(
	'footer-widget-1' => '<p class="t-foot-name">Građevinsko preduzeće<br>„24. Oktobar“ d.o.o.</p><p>Gasovodi, mreže i grubi građevinski radovi. Novi Sad, od 1997.</p>',
	'footer-widget-2' => '<p class="t-foot-label">Adresa i telefoni</p><p>Temerinska 50<br>21000 Novi Sad, Srbija</p><p><a href="tel:+381214741048">+381 21 47 41 048</a><br><a href="tel:+38121551044">+381 21 551 044</a><br><a href="tel:+38163503333">+381 63 503 333</a></p>',
	'footer-widget-3' => '<p class="t-foot-label">E-pošta i radno vreme</p><p><a href="mailto:24oktobar.ns@gmail.com">24oktobar.ns@gmail.com</a></p><p>Ponedeljak–petak, 08:00–15:00</p><p>PIB 101 699 336 · MB 0866 4102</p>',
);
$next = max( array_filter( array_keys( $blocks ), 'is_int' ) ?: array( 1 ) ) + 1;
foreach ( $footer as $area => $content ) {
	// replace our previous widget in this area if the script was run before
	foreach ( (array) ( $sidebars[ $area ] ?? array() ) as $wid ) {
		$n = (int) str_replace( 'block-', '', $wid );
		unset( $blocks[ $n ] );
	}
	$blocks[ $next ]    = array( 'content' => "<!-- wp:html -->\n$content\n<!-- /wp:html -->" );
	$sidebars[ $area ] = array( "block-$next" );
	$next++;
}
$blocks['_multiwidget'] = 1;
update_option( 'widget_block', $blocks );
update_option( 'sidebars_widgets', $sidebars );
t24_log( 'footer widgets set' );

/* ------------------------------------------------------------------ CSS */
$css = file_get_contents( "$root/wp-custom/site.css" );
$r   = wp_update_custom_css_post( $css, array( 'stylesheet' => get_stylesheet() ) );
t24_log( is_wp_error( $r ) ? 'css error: ' . $r->get_error_message() : 'additional css saved (' . strlen( $css ) . ' bytes)' );

/* ------------------------------------------------------------------ The SEO Framework: homepage */
$tsf = (array) get_option( 'autodescription-site-settings', array() );
$home = $manifest[0];
$tsf['homepage_title']         = $home['seo_title'];
$tsf['homepage_description']   = $home['seo_desc'];
$tsf['homepage_title_tagline'] = '';
$tsf['homepage_tagline']       = 0;
$tsf['title_separator']        = 'pipe';
$tsf['knowledge_name']         = 'Građevinsko preduzeće „24. Oktobar“ d.o.o.';
update_option( 'autodescription-site-settings', $tsf );
t24_log( 'seo settings saved' );

echo "done\n";
