tinymce.init({
      selector: '#id_description',
      height: 400,
      plugins: [
          'link image code',
          'image imagetools',
          'nonbreaking',
          'insertdatetime media table paste imagetools wordcount'
          ],
      toolbar: 'nonbreaking',

      relative_urls: false,
      remove_script_host: false,
    });
