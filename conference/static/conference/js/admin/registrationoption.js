tinymce.init({
      selector: '#id_text, #id_description',
      height: 400,
      plugins: [
          'link image code',
          'insertdatetime media table paste imagetools wordcount'
          ]
      relative_urls: false,
      remove_script_host: false,
    });
