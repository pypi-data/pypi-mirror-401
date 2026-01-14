let alias = jQuery.noConflict();

var site_theme = (localStorage.getItem('theme') != null)
    ? localStorage.getItem('theme')
    : 'light';

var site_font = (localStorage.getItem('font') != null)
    ? localStorage.getItem('font')
    : 'normal';

function toggle_theme(_theme) {

    console.log(_theme)

    if (_theme === "dark") {
        console.log("dark mode")
        alias('html').attr("data-theme", "dark")
        alias('#source-code-css').attr("href", "../css/source_code/github-dark.css")
        alias(`select option#${_theme}`).attr("selected", true)
    } else if (_theme === "dyslexia") {
        alias('html').attr("data-theme", "dyslexia")
        alias(`select option#${_theme}`).attr("selected", true)
    } else {
        alias('html').attr("data-theme", "light")
        alias('#source-code-css').attr("href", "../css/source_code/github.css")
        alias(`select option#${_theme}`).attr("selected", true)
    }
    localStorage.setItem('theme', _theme);
}

function toggle_font(_font) {
    if (_font === "comic-sans") {
        alias('#btn-font').attr("onclick", "toggle_font('normal')")
        alias('#chosen-font').attr("href", "https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap")
        alias('body').addClass('comic-sans')
        alias('body').removeClass('ubuntu')
        console.log("comic-sans")
    } else {
        alias('#btn-font').attr("onclick", "toggle_font('comic-sans')")
        alias('#chosen-font').attr("href", "https://fonts.googleapis.com/css2?family=Ubuntu+Sans:ital,wght@0,100..800;1,100..800&display=swap")
        alias('body').addClass('ubuntu')
        alias('body').removeClass('comic-sans')
        console.log("normal")
    }
    alias(`select option#${_font}`).attr("selected", true)
    localStorage.setItem('font', _font);
}

alias(document).ready(function () {
    toggle_theme(site_theme)
    toggle_font(site_font)
})