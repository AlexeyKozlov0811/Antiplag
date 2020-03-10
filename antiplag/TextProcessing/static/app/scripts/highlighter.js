
url = document.location.href.split('/');
id = url[url.length-2]
$.ajax({
    type: 'GET',
    async: true,
    url: '/highlight_text/' + id + '/',
    data: "",
    success: function(data) {
        if (data !== undefined && data !== null){
            console.log(data);
            burrowed_text = createArrayOfBurrowedContent(data['text']);
            console.log(burrowed_text);

            burrowed_text.forEach(item => domRangeHighlight(item[0], item[1]));


//            new_text = $("#first_text_area").html().trim();

//            for (let key of sources){
////                burrowed_text[key].sort(function(a, b){
////                    return a.length - b.length;
////                });
//                console.log(burrowed_text[key])
//                for (let text_idx = 0; text_idx < burrowed_text[key].length; text_idx++){
//                    burrowed_content = `${burrowed_text[key][text_idx]}`
//                    burrowed_times = 'once'
//
//                    burrowed_content = burrowed_content.replace(symbols, '\\$&');
//                    regex = new RegExp(burrowed_content, 'g');;
//
//                    second_time = 0;
//                    third_time = 0;
//
//
//
//                    $("span.once").map(function(index, element){
//                        console.log(key)
//                        console.log($(element).html())
//                        second_time = $(element).html().indexOf(regex)+1;
//                        console.log(second_time)
//
//
//                    });
////                    if ($("span.once").html()!==undefined){
////                        second_time = $("span.once").html().indexOf(regex)+1;
////                    }
////                    $("span.two_times").map(function(index, element){
//////                        console.log($(element).html())
////                        third_time = $(element).html().indexOf(regex)+1;
////                    });
////                    if ($("span.two_times").html()!==undefined){
////                        third_time = $("span.two_times").html().indexOf(regex)+1;
////                    }
//

//
//                    highlighted_content = '<span class=\'highlighted_text ' + `${key} ` + `${burrowed_times}` +'\''  + ' onclick=\'highlight_sources(\"' + `${key}` + '\")\'' + '>' + `${burrowed_text[key][text_idx]}` + '</span>';
//                    new_text = new_text.replace(regex, highlighted_content);
//
//                    $("#first_text_area").html(new_text);
//
//                }
//            }


        }
    },
    dataType: 'json',
});

function createArrayOfBurrowedContent(dict){
    array = []
    for (var key in dict){
        dict[key].forEach(item => array.push([key,item.trim()]));
    }
    return sortArrayOfBurrowedContent(array);
}

function sortArrayOfBurrowedContent(array){
    array.sort(function(first, second) {
        return second[1].length - first[1].length;
    });
    return array;
}

function domRangeHighlight(source, text){

    has_found = 0;
    if ( document.getElementsByClassName('two_times').firstChild !== undefined ){
        document.getElementsByClassName('two_times').firstChild.forEach(element => {has_found = findInElement(element, regex, source, 'tree_and_more')})
    }
    else if ( (!(has_found)) && (document.getElementsByClassName('once').firstChild !== undefined) ){
        document.getElementsByClassName('once').firstChild.forEach(element => {has_found = findInElement(element, regex, source, 'two_times')})
    }
    else if ( !(has_found) ){
        root = document.getElementById('first_text_area').firstChild;
        findInElement(root, text, source, 'once')
    }


}

function findInElement(root, text, source, burrowed_times){
//    const symbols = /\[|\\|\^|\$|\.|\||\?|\*|\+|\(|\)/g;
//    regex = text.replace(symbols, '\\$&');
//    regex = new RegExp(regex, 'g');
//    regex = "Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на всіх основних платформах. В мові програмування Python підтримується кілька парадигм програмування, зокрема: об'єктно-орієнтована, процедурна, функціональна та аспектно-орієнтована. ЗАСТОСУВАННЯ НЕЙРОМЕРЕЖ ДЛЯ ІНФОРМАЦІЙНОГО ПОШУКУ Застосування нейромереж для задач інформаційного пошуку може значно покращити швидкість та точність пошуку. Сутність методу полягає в властивості нейромережі до навчання, тобто при правильному алгоритмі результат роботи програми буде все точніше й точніше, а завдяки зібраному досвіду шлях вирішення задачі буде також зменшуватись, що прискорить появу результату. Мінусами цього методу є велика вартість в грошових та обчислювальних ресурсах і значні потреби в часі на розробку, тестування, розгортання та навчання нейромережі. Розглянемо застосування методу на прикладі реалізації пошукової системи."
    var content = root.nodeValue;
//TO DO сделать выделение множественного повторения
    if (content.indexOf(text)+1){
        if (document.createRange) {
            var rng = document.createRange();
            rng.setStart(root, content.indexOf(text));
            rng.setEnd(root, content.indexOf(text) + text.length);
            var highlighted = document.createElement('span');
            highlighted.classList.add(`${source}`, 'highlighted_text', `${burrowed_times}`);
            highlighted.addEventListener("click", highlight_sources);
            rng.surroundContents(highlighted);
        } else {
            alert( 'Можливо, ви використовуєте IE8, тому виділення запозиченого тексту не працює' );
        }
        return 1;
    }
    else{ return 0; }
}

function highlight_sources() {
    source = this.className.split(' ')[0]
    console.log(source);

    $('#first_text_area span').css("background", "")
    $('.source_list').css("display", "initial")

    $(`span.${source}`).css("background", "#bae9ff");
    $('.source_list').css("display", "none");
    $(`.source_list.${source}`).css("display", "block");
}
