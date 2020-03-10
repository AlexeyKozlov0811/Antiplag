
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
            const symbols = /\[|\\|\^|\$|\.|\||\?|\*|\+|\(|\)/g;
            new_text = $("#first_text_area").html().trim();

            for (let key of sources){
                burrowed_text[key].sort(function(a, b){
                    return a.length - b.length;
                });
                console.log(burrowed_text[key])
                for (let text_idx = 0; text_idx < burrowed_text[key].length; text_idx++){
                    burrowed_content = `${burrowed_text[key][text_idx]}`
                    burrowed_times = 'once'

                    burrowed_content = burrowed_content.replace(symbols, '\\$&');
                    regex = new RegExp(burrowed_content, 'g');;

                    second_time = 0;
                    third_time = 0;



                    $("span.once").map(function(index, element){
                        console.log(key)
                        console.log($(element).html())
                        second_time = $(element).html().indexOf(regex)+1;
                        console.log(second_time)


                    });
//                    if ($("span.once").html()!==undefined){
//                        second_time = $("span.once").html().indexOf(regex)+1;
//                    }
//                    $("span.two_times").map(function(index, element){
////                        console.log($(element).html())
//                        third_time = $(element).html().indexOf(regex)+1;
//                    });
//                    if ($("span.two_times").html()!==undefined){
//                        third_time = $("span.two_times").html().indexOf(regex)+1;
//                    }

                    if (second_time || (key.split("_").length >= 2)){
                        burrowed_times = 'two_times';
                    }
                    else if (third_time || (key.split("_").length >= 3)){
                        burrowed_times = 'tree_and_more';
                    }









                    highlighted_content = '<span class=\'highlighted_text ' + `${key} ` + `${burrowed_times}` +'\''  + ' onclick=\'highlight_sources(\"' + `${key}` + '\")\'' + '>' + `${burrowed_text[key][text_idx]}` + '</span>';
                    new_text = new_text.replace(regex, highlighted_content);

                    $("#first_text_area").html(new_text);

                }
            }


        }
    },
    dataType: 'json',
});
