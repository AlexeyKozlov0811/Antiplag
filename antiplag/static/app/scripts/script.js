$(document).ready(function () {
        $(".get_source").click(function() {
            id = this.innerHTML.split("/")[2];
            $.ajax({
                type: 'GET',
                async: true,
                url: '/text_source/' + id + '/',
                data: "",
                success: function(data) {
                    $("#more-text-here1").text(data['first-text']);
                },
                dataType: 'json',
            });
        });
    });