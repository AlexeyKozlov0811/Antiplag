

function highlight_sources(sender) {
    console.log(sender);

    $(`span`).css("background", "")
    $('.source_list').css("display", "initial")

    $(`span.${sender}`).css("background", "#bae9ff");
    $('.source_list').css("display", "none");
    $(`.source_list.${sender}`).css("display", "block");
};