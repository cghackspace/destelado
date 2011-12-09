$(function() {
    // used on /deputados
    $("table").tablesorter({ 
        textExtraction: function(node) {
            switch(node.className) {
                case "name":
                    return node.childNodes[0].textContent;
                case "frequency":
                    textContent = node.textContent;
                    frequency = node.textContent.substring(textContent.indexOf('(')+1, textContent.length-1).split(" / ");
                    return parseInt(frequency[0]) / parseInt(frequency[1]);
                default:
                    return node.innerHTML;
            }
        } 
    });

    // used on /deputados to filter deputies
    $('table').tableFilter({
        filters: {
            party: $('#party'),
            state: $('#state')
        }
    }); 
});