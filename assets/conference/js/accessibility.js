function initializeAccessibilitySettings() {
    let accessibility_settings = localStorage.getItem('accessibility_settings');
    if (!accessibility_settings) {
        return;
    }
    accessibility_settings = JSON.parse(accessibility_settings);

    if (accessibility_settings.hasOwnProperty('font_size_multiplier')) {
        $("#id_font_size_multiplier").val(accessibility_settings['font_size_multiplier']);
        if (accessibility_settings['font_size_multiplier'] != 1) {
            let font_size_multiplier = parseFloat(accessibility_settings['font_size_multiplier']);
            let font_size = parseInt($('body').css("font-size"));
            font_size = Math.round(font_size * font_size_multiplier);
            font_size = Math.max(font_size, 10);
            font_size = Math.min(font_size, 32);
            $(':root').css({"font-size": font_size + "px"});
        }
    }

    if (accessibility_settings.hasOwnProperty('high_contrast_mode')) {
        $("#id_high_contrast_mode").prop('checked', accessibility_settings['high_contrast_mode']);
        if (accessibility_settings['high_contrast_mode']) {
            $('body').css({
                "--gray": "black",
                "--dark-gray": "black",
                "--dark-blue": "black",
                "--light-yellow": "white",
                "--red": "black",
            });
            $(".speaker-text-color, .nav-link").css({
                "color": "black",
            });
            $(".child-a-tag").css({
                "background-color": "black",
                "color": "white",
            });
            $(".bg-checkered-yellow, .recipe .tip").css({
                "background-color": "black",
            });
            $("article .category, figure .category").css({
                "color": "black",
            });
            $(".footer .title").css({
                "color": "white",
            });
        }
    }

    if (accessibility_settings.hasOwnProperty('text_to_speech')) {
        $("#id_text_to_speech").prop('checked', accessibility_settings['text_to_speech']);
        if (accessibility_settings['text_to_speech']) {

            function bindNarration (e) {
                let elmt = $(this);

                // Don't narrate the element if it has an ancestor who is supposed to be narrated.
                if (elmt.parent().closest('.atomic-narration').length > 0) {
                    return;
                }

                // Don't narrate the element if it has narratable children.
                let narratable_children = elmt.children(narratable + ":not(svg):not(.fas)");
                let narratable_children_exist = false;
                if (narratable_children.length > 0 && !elmt.hasClass('atomic-narration')) {
                    // Loop through the children and find exemptions.
                    narratable_children.each(function () {
                        let child = $(this);
                        // If the child is a hidden image tag, allow the parent to be narrated.
                        if (child.is(narratable) && child.prop("tagName").toLowerCase() == 'img' && child.css("visibility") == "hidden") {
                            return; // This is the equivalent of continue in a jQuery each loop.
                        }
                        // If the parent is a paragraph tag and the child is an inline element, allow the parent to be narrated.
                        if (child.is(narratable) && (['p', 'li'].indexOf(elmt.prop("tagName").toLowerCase()) != -1) && (['a', 'span', 'i', 'b', 'strong', 'em'].indexOf(child.prop("tagName").toLowerCase()) != -1)) {
                            return; // This is the equivalent of continue in a jQuery each loop.
                        }
                        narratable_children_exist = true;
                        return false; // This is the equivalent of break in a jQuery each loop.
                    });
                    if (narratable_children_exist) {
                        return;
                    }
                }

                let text = "";
                if (!text && elmt.text()) {
                    text = elmt.text().trim();
                }
                if (!text && elmt.attr('title')) {
                    text = elmt.attr('title');
                }
                if (!text && elmt.prop("tagName").toLowerCase() == 'img' && elmt.attr('alt')) {
                    text = elmt.attr('alt');
                }
                if (!text && elmt.attr('aria-label')) {
                    text = elmt.attr('aria-label');
                }
                if (!text && elmt.attr('aria-description')) {
                    text = elmt.attr('aria-description');
                }
                if (!text && elmt.prop("tagName").toLowerCase() == 'input' && elmt.attr('placeholder')) {
                    text = elmt.attr('placeholder');
                }
                if (!text && elmt.prop("tagName").toLowerCase() == 'input' && elmt.attr('type') == 'submit' && elmt.attr('value')) {
                    text = elmt.attr('value');
                }
                if (!text && $("label[for='"+elmt.attr('id')+"']").length) {
                    text = $("label[for='"+elmt.attr('id')+"']").text().trim();
                }
                if (elmt.prop("tagName").toLowerCase() == 'select' && elmt.attr('aria-label')) {
                    text = elmt.attr('aria-label');
                }
                if (!text) {
                    return;
                }

                if (window.speechSynthesis.speaking) {
                    window.speechSynthesis.cancel();
                }

                $(".narrating").removeClass("narrating");
                elmt.addClass("narrating");

                utterance = new SpeechSynthesisUtterance(text);
                window.speechSynthesis.speak(utterance);

                utterance.onend = function () {
                    elmt.removeClass("narrating");
                }

            }

            let utterance = null;
            let narratable = ":not([tabindex='-1']):not([role='none']):not([aria-hidden='true']):not(option):visible";
            $(narratable).off("mouseover focus", bindNarration);
            $(narratable).on("mouseover focus", bindNarration);

            $(window).on("click keydown mouseleave", function () {
                window.speechSynthesis.cancel();
            });

        }
    }

}

$(document).ready(function () {

    $("#accessibility-settings-form").on("submit", function (e) {
        e.preventDefault();
        let accessibility_settings = {};
        $(this).find("input").each(function () {
            let key = $(this).attr('name');
            let type = $(this).attr('type');
            let value = $(this).val();
            if (type == 'checkbox') {
                value = $(this).prop('checked');
            }
            accessibility_settings[key] = value;
        });
        localStorage.setItem("accessibility_settings", JSON.stringify(accessibility_settings));
        window.location.reload();
        return false;
    });

    initializeAccessibilitySettings();

});