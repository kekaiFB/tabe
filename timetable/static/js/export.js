$('.export').on('click', function () {
    var myTableArray = [];
    $("table tr").each(function() {
        var rowDataArray = [];
        var actualData = $(this).find('td');

        if (actualData.length > 0) {
            actualData.each(function() {
                rowDataArray.push($(this).html());
            });
            myTableArray.push(rowDataArray.slice(0, -2));
        }
    });
    const doc = new Document();

    var paragraph = new Paragraph("РАСПИСАНИЕ (с _____ по _______)");
    doc.addParagraph(paragraph);
  
    
    paragraph = new Paragraph();
    text = new TextRun($("table tr").text()).bold();
    paragraph.addRun(text);
    doc.addParagraph(paragraph);

    const packer = new Packer();
  
    packer.toBlob(doc).then(blob => saveAs(blob, "example.docx"));
 });
