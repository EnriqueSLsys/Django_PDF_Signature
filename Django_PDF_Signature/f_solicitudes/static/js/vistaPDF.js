$(document).ready(function() {
    const pdfPath = "{{ pdf_base64 }}";
    const container = $('#pdfContainer');
    const canvas = document.getElementById('pdfViewer');
    const context = canvas.getContext('2d');

    pdfjsLib.getDocument(pdfPath).promise.then(function(pdf) {
        pdf.getPage(1).then(function(page) {
            const viewport = page.getViewport({ scale: 1 });
            const containerWidth = container.width();
            const scale = containerWidth / viewport.width;
            const scaledViewport = page.getViewport({ scale: scale });

            canvas.height = scaledViewport.height;
            canvas.width = scaledViewport.width;

            const renderContext = {
                canvasContext: context,
                viewport: scaledViewport
            };
            page.render(renderContext);
        });
    });
});


<div class="d-flex justify-content-center">
<div id="pdfContainer" style="width: 50%;">
    <canvas id="pdfViewer" style="border:1px solid black; width: 100%;"></canvas>
</div>
</div>