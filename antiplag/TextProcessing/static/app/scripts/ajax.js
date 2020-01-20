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
                    $(".first_text").css({"display": "inline-block",
                                          "width": "48%"
                                         });
                    $(".second_text").css("display", "inline-block");
                    $("#second_text_area").text(data['text']);
                    if (data['burrowed_content'] !== undefined){
                        console.log(data['burrowed_content'][0]);

                        //let text = data['burrowed_content'][0];
                        //let text = "енциклопедії. Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван Россумом. ";
                        let text = document.getElementById("second_text_area").innerHTML
                        console.log(text)
                        console.log(text.indexOf(data['burrowed_content'][0]));
                        for (let text_idx = 0;text_idx<data['burrowed_content'].length; text_idx++){
                            document.getElementById("second_text_area").innerHTML = document.getElementById("second_text_area").innerHTML.replace(`${data['burrowed_content'][text_idx]}`, `<span class='orange'>${data['burrowed_content'][text_idx]}</span>`);
                        }
                    }
                },
                dataType: 'json',
            });
        });
    });