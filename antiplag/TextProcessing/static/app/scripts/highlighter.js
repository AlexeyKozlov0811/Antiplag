
url = document.location.href.split('/');
id = url[url.length-2]
$.ajax({
    type: 'GET',
    async: true,
    url: '/highlight_text/' + id + '/',
    data: "",
    success: function(data) {
        console.log(data);
        burrowed_text = data['text'];
        sources = data['sources'];
        if (data !== undefined){

            new_text = $("#first_text_area").html().trim();
            for (let key of sources){
                burrowed_text[key].sort(function(a, b){
                    return a.length - b.length;
                });
                for (let text_idx = 0; text_idx < burrowed_text[key].length; text_idx++){
                    burrowed_content = `${burrowed_text[key][text_idx]}`
                    burrowed_times = 'once'
                    if (key.split("_").length >= 3){
                        burrowed_times = 'tree_and_more';
                    }
                    else if (key.split("_").length == 2){
                        urrowed_times = 'two_times';
                    }
                    highlighted_content = '<span class=\'highlighted_text ' + `${key} ` + `${burrowed_times}` +'\''  + ' onclick=\'highlight_sources(\"' + `${key}` + '\")\'' + '>' + `${burrowed_content}` + '</span>';

                    const symbols = /\[|\\|\^|\$|\.|\||\?|\*|\+|\(|\)/g;
                    burrowed_content = burrowed_content.replace(symbols, '\\$&');
                    const regex = new RegExp(burrowed_content, 'g');
                    new_text = new_text.replace(regex, highlighted_content);


                }
            }
            $("#first_text_area").html(new_text);
        }
    },
    dataType: 'json',
});
