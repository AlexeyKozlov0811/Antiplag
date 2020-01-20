let patterns = [
    {text: " 1!_!_!1 ", classes: ['orange']},
    {text: " 2!_!_!2 ", classes: ['orange']},
];

url = document.location.href.split('/');
id = url[url.length-2]
$.ajax({
    type: 'GET',
    async: true,
    url: '/highlight_text/' + id + '/',
    data: "",
    success: function(data) {
        if (data['text'] !== undefined){
            for (let text_idx = 0;text_idx<data['text'].length; text_idx++){
                    document.getElementById("first_text_area").innerHTML = document.getElementById("first_text_area").innerHTML.replace(`${data['text'][text_idx]}`, `<span class='orange'>${data['text'][text_idx]}</span>`);
                }
        }
    },
    dataType: 'json',
});

