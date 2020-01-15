$(document).ready(function () {
        $(".get_source").click(function() {
            id = $(this).attr("value");
            $.ajax({
                type: 'GET',
                async: true,
                url: '/text_source/' + id + '/',
                data: "",
                success: function(data) {
                    $(".first_text").css({"display": "inline-block",
                                          "width": "48%"
                                         });
                    $(".second_text").css("display", "inline-block");
                    $("#second_text_area").text(data['text']);
                },
                dataType: 'json',
            });
        });
    });