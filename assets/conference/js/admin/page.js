tinymce.init({
      selector: '#id_text, #id_child_intro',
      height: 600,
      paste_data_images: true,
      font_formats:"Andale Mono=andale mono,times; Arial=arial,helvetica,sans-serif; Arial Black=arial black,avant" +
          " garde; Book Antiqua=book antiqua,palatino; Comic Sans MS=comic sans ms,sans-serif; Courier New=courier" +
          " new,courier; Georgia=georgia,palatino; Helvetica=helvetica; Impact=impact,chicago; Symbol=symbol; " +
          "Tahoma=tahoma,arial,helvetica,sans-serif; Terminal=terminal,monaco; Times New Roman=times new roman,times; " +
          "Trebuchet MS=trebuchet ms,geneva; Verdana=verdana,geneva; Webdings=webdings; Wingdings=wingdings,zapf dingbats;" +
          "Open Sans=Open-Sans, sans-serif;",
      plugins: [
          'link image code',
          'insertdatetime media table paste imagetools wordcount'
          ],
      relative_urls: false,
      remove_script_host: false,
    });
