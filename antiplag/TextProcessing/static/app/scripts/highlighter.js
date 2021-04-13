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
        console.log('tree_and_more')
    }
    else if ( (!(has_found)) && (document.getElementsByClassName('once').firstChild !== undefined) ){
        document.getElementsByClassName('once').firstChild.forEach(element => {has_found = findInElement(element, regex, source, 'two_times')})
        console.log('two_times')
    }
    else if ( !(has_found) ){
        console.log(text)
        root = document.getElementById('first_text_area').firstChild;
        findInElement(root, text, source, 'once')
        console.log('once')
    }
}

function findInElement(root, text, source, burrowed_times){
    var ranges_list = [];
    var content = root.nodeValue;
    var entrance_times = 0;

    if (document.createRange) {
        while (content.indexOf(text, entrance_times*text.length) !== -1){
            var rng = document.createRange();
            rng.setStart(root, content.indexOf(text, entrance_times*text.length));
            rng.setEnd(root, content.indexOf(text, entrance_times*text.length) + text.length);
            ranges_list.push(rng);
            entrance_times++;
        }
        console.log(ranges_list)
        ranges_list.forEach(range => {
            var highlighted = document.createElement('span');
            highlighted.classList.add(`${source}`, 'highlighted_text', `${burrowed_times}`);
            highlighted.addEventListener("click", highlight_sources);
            range.surroundContents(highlighted);
        });
    } else {
        alert( 'Можливо, ви використовуєте IE8, тому виділення запозиченого тексту не працює' );
    }

    if (entrance_times === 0){ return 0; }
    else{ return 1; }
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