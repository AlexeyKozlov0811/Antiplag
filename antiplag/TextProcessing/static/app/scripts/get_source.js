$(document).ready(function () {
    $(".get_source").click(function() {
        url = document.location.href.split('/');
        first_text_id = url[url.length-2]
        second_text_id = $(this).attr("value");
        $.ajax({
            type: 'GET',
            async: true,
            url: '/text_source/' + first_text_id + '/' + second_text_id + '/',
            data: "",
            success: function(data) {
                console.log(data);
                second_text_text = data['text'].replace(/\s+/g, ' ');
                burrowed_content = data['burrowed_content'];
//                $(".source_list").css({"display": "none"});
                $(".first_text").css({"display": "inline-block", "width": "48%"});
                $("#second_text_area").css("display", "inline-block");
                $("#second_text_area").text(second_text_text);
                area_style = 'background:' + '#ffff00;';
                if (burrowed_content !== undefined) {
                    let text = document.getElementById("second_text_area").innerHTML;
                    new_text = $("#second_text_area").html()
                    for (let text_idx = 0; text_idx < burrowed_content.length; text_idx++) {
                        part = `${burrowed_content[text_idx]}`.trim()
                        highlighted_content = '<span style=' + `${area_style}>` + `${part}` + '</span>';
                        new_text = new_text.replace(part, highlighted_content);
                    }
                    $("#second_text_area").html(new_text)
                }
            },
            dataType: 'json',
        });
    });
});