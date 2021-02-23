tinymce.init({
      selector: '#id_cancel_refund, #id_basic_conference, #id_all_access_conference',
      height: 600,
      plugins: [
          'link image code',
          'insertdatetime media table paste imagetools wordcount'
          ],
      toolbar: 'nonbreaking',

      relative_urls: false,
      remove_script_host: false,
    });
