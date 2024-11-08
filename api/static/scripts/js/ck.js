import { ClassicEditor, Essentials, Bold, Italic, Paragraph, Font } from 'ckeditor5';
import { FormatPainter } from 'ckeditor5-premium-features';

import 'ckeditor5/ckeditor5.css';
import 'ckeditor5-premium-features/ckeditor5-premium-features.css';

ClassicEditor.create(document.querySelector('#editor'), {
    plugins: [Essentials, Bold, Italic, Paragraph, Font, FormatPainter],
    toolbar: [
        'undo',
        'redo',
        '|',
        'bold',
        'italic',
        '|',
        'fontSize',
        'fontFamily',
        'fontColor',
        'fontBackgroundColor',
        '|',
        'formatPainter',
    ],
})
    .then(/* ... */)
    .catch(/* ... */);
