tinymce.init({
      selector: '#id_text, #id_child_intro',
      height: 600,
      plugins: [
          'link image code',
          'insertdatetime media table paste imagetools wordcount'
          ],
      relative_urls: false,
      remove_script_host: false,
    });
