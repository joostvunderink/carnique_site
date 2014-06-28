function set_language(e, language) {
    console.log("Setting language to " + language);
    $("input#language").val(language);
    $("form#set_language").submit();
};

$(document).ready(function() {
    $("img#lang_nl").click(function(e) {
        set_language(e, 'nl');
    });
    $("img#lang_en").click(function(e) {
        set_language(e, 'en');
    });
    $("img#lang_pl").click(function(e) {
        set_language(e, 'pl');
    });
});
