(function(jQuery) {
    jQuery.fn.changeElementType = function(newType) {
        var attrs = {};

        jQuery.each(this[0].attributes, function(idx, attr) {
            attrs[attr.nodeName] = attr.nodeValue;
        });

        this.replaceWith(function() {
            return jQuery("<" + newType + "/>", attrs).append(jQuery(this).contents());
        });
    };
})(jQuery);

jQuery(document).ready(function() {

	function formatValueField() {
		var type = jQuery("select#id_type[name='type']").val();
		var value_field = jQuery("#id_value[name='value']");
		var html = value_field.html()
		var value = value_field.val();
		if (!value && html) {
			value = html;
		}
		value_field.next('.related-lookup').remove();
		value_field.next("[type='checkbox']").remove();
		value_field.removeAttr("cols rows style placeholder title");
		jQuery('.CodeMirror').remove();
		switch (type) {
			case 'text':
				value_field.changeElementType('textarea');
				value_field = jQuery("#id_value[name='value']");
				value_field.removeAttr("type value");
				value_field.text(value);
				break;
			case 'boolean':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "hidden"});
				value_field.html("");
				value_field.val(value);
				value_field.after("<input type='checkbox' />");
				if (value_field.val()) {
					value_field.next("[type='checkbox']").attr({"checked": true});
				}
				value_field.next("[type='checkbox']").on('click', function() {
					if (this.checked) {
						value_field.val(1);
					}
					else {
						value_field.val(0);
					}
				});
				break;
			case 'color':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "color"});
				value_field.html("");
				value_field.val(value);
				break
			case 'date':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({
					"type": "date",
					"placeholder": "yyyy-mm-dd",
					"title": "yyyy-mm-dd",
				});
				value_field.html("");
				value_field.val(value);
				break;
			case 'time':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({
					"type": "time",
					"placeholder": "hh:mm:ss",
					"title": "hh:mm:ss",
				});
				value_field.html("");
				value_field.val(value);
				break;
			case 'datetime':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({
					"type": "datetime-local",
					"placeholder": "yyyy-mm-dd hh:mm:ss",
					"title": "yyyy-mm-dd hh:mm:ss",
				});
				value_field.html("");
				value_field.val(value);
				break;
			case 'email':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "email"});
				value_field.html("");
				value_field.val(value);
				break;
			case 'pdf':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({
					"type": "text",
					"class": "vForeignKeyRawIdAdminField",
				});
				value_field.html("");
				value_field.val(value);
				value_field.after("<a href='/admin/media/media/?_to_field=id' class='related-lookup' id='lookup_id_value' title='Lookup'></a>");
				break;
			case 'integer':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({
					"type": "number",
					"step": "1",
				});
				value_field.html("");
				value_field.val(value);
				break;
			case 'number':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "text"});
				value_field.html("");
				value_field.val(value);
				break;
			case 'phone':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "tel"});
				value_field.html("");
				value_field.val(value);
				break;
			case 'url':
				value_field.changeElementType('input');
				value_field = jQuery("#id_value[name='value']");
				value_field.attr({"type": "url"});
				value_field.html("");
				value_field.val(value);
				break;
			case 'html':
				value_field.changeElementType('textarea');
				value_field = jQuery("#id_value[name='value']");
				value_field.removeAttr("type value");
				value_field.text(value);
			    var editor = CodeMirror.fromTextArea(value_field[0], {
			        lineNumbers: true,
			        htmlMode: true,
			        mode: "xml",
			        theme: 'monokai',
			        lineWrapping: true,
			    });
			    editor.setSize(null,"100%");
			    break;
			case 'javascript':
				value_field.changeElementType('textarea');
				value_field = jQuery("#id_value[name='value']");
				value_field.removeAttr("type value");
				value_field.text(value);
			    var editor = CodeMirror.fromTextArea(value_field[0], {
			        lineNumbers: true,
			        htmlMode: true,
			        mode: "javascript",
			        theme: 'monokai',
			        lineWrapping: true,
			    });
			    editor.setSize(null,"100%");
			    break;
			case 'css':
				value_field.changeElementType('textarea');
				value_field = jQuery("#id_value[name='value']");
				value_field.removeAttr("type value");
				value_field.text(value);
			    var editor = CodeMirror.fromTextArea(value_field[0], {
			        lineNumbers: true,
			        htmlMode: true,
			        mode: "css",
			        theme: 'monokai',
			        lineWrapping: true,
			    });
			    editor.setSize(null,"100%");
			    break;
			default:
				value_field.changeElementType('textarea');
				value_field = jQuery("#id_value[name='value']");
				value_field.removeAttr("type value");
				value_field.text(value);
		}

		$('.related-lookup').click(function(e) {
            e.preventDefault();
            var event = $.Event('django:lookup-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showRelatedObjectLookupPopup(this);
            }
        });

	}

	formatValueField();

	jQuery("select[name='type']").on('change', function() {
		formatValueField();
	});

});