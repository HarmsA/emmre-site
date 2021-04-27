$(document).ready(function (){
    let editor = CodeMirror.fromTextArea(document.getElementById('id_css'), {
        lineNumbers: true,
        htmlMode: true,
        mode: "css",
        theme: 'monokai',
        lineWrapping: true,
    });
    editor.setSize(null,"100%");
});