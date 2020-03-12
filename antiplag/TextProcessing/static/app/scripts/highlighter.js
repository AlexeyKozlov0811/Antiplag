
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
            data_to_highlight = []
            burrowed_text = createArrayOfBurrowedContent(data['text']);
            console.log(burrowed_text);
            burrowed_text.forEach(item => {
                burrowed = domRangeHighlight(item[0], item[1])

                if (burrowed[0])
//                    console.log(burrowed)
                    data_to_highlight.push(burrowed[0])
            });
            highlight_ranges(data_to_highlight)
            console.log(data_to_highlight)
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
    burrowed_data_list = []
    has_found = 0;
    if ( document.getElementsByClassName('two_times').firstChild !== undefined ){
        document.getElementsByClassName('two_times').firstChild.forEach(element => {
            has_found, burrowed_data = findInElement(element, regex, source, 'tree_and_more');
            if (burrowed_data){burrowed_data_list.push(burrowed_data)}});
//        console.log('tree_and_more')
    }
    else if ( (!(has_found)) && (document.getElementsByClassName('once').firstChild !== undefined) ){
        document.getElementsByClassName('once').firstChild.forEach(element => {has_found, burrowed_data = findInElement(element, regex, source, 'two_times');
        if (burrowed_data){burrowed_data_list.push(burrowed_data)}});
//        console.log('two_times')
    }
    else if ( !(has_found) ){
        root = document.getElementById('first_text_area').firstChild;
        has_found, burrowed_data = findInElement(root, text, source, 'once')
        if (burrowed_data)
            burrowed_data_list.push(burrowed_data)
//        console.log('once')
    }

    return burrowed_data_list;
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

        if (ranges_list.length >= 2){ranges_list = delete_ranges_duplicates(ranges_list);}

        burrowed_data = {
            ranges: ranges_list,
            source: `${source}`,
            burrowed_times: `${burrowed_times}`
        };
//        console.log(burrowed_data)
    } else {
        alert( 'Можливо, ви використовуєте IE8, тому виділення запозиченого тексту не працює' );
    }

    if (entrance_times === 0){ return 0, undefined; }
    else{ return 1, burrowed_data; }
}

function delete_ranges_duplicates(ranges){
    var delete_indexes = []
    for (var i = ranges.length-1; i > 0; i--)
        if (ranges[i].startOffset == ranges[i-1].startOffset && ranges[i].endOffset == ranges[i-1].endOffset)
            delete_indexes.push(i)
    delete_indexes.forEach(index => ranges.splice(index))
    return ranges
}

function highlight_ranges(burrowed_data_list) {
    burrowed_data_list.forEach(burrowed_data => {
        burrowed_data.ranges.forEach(range =>{
            var highlighted = document.createElement('span');
            highlighted.classList.add(`${burrowed_data.source}`, 'highlighted_text', `${burrowed_data.burrowed_times}`);
            highlighted.addEventListener("click", highlight_sources);
            range.surroundContents(highlighted);
        });

    });
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
