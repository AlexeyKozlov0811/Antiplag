{% block scripts %}
{% load staticfiles %}
    <script src="{% static 'app/scripts/ajax.js' %}">
    </script>

    <script>
        let patterns = [
            {text: "123", classes: ['orange']},
            //{text: "Python (��������� ������� ���������� � ���?����, ���������� �����[5] � ������������ ��� ���� ������) � �������������� ��'�����-��������� ���� ������������� �������� ���� � ������� ��������� ���������.[6] ���������� � 1990 ���� ���� ��� ��������. ��������� ����� �������� ���� ����� �� ��������� ���������� �� ��������� ��'��������� ������� �� ����������� ��� ������ �������� �������, � ����� �� ���� ���������� ������� ����������. Python ������� ����� �� ������ ������, �� ������ ���������� �� ���������� ������������ ����. ������������� Python �� ��������� �������� ������� �� � ������������, ��� � � ������� ���� �� ��� �������� ����������. � ��� ������������� Python ����������� ", classes: ['orange']},
        ];






        const marker = ( text, patterns ) => {
            return patterns.reduce( ( result, current ) => {
                let regexp = new RegExp(current.text, 'g');
                let style = current.classes.join(' ');
                return result.replace( regexp, `${ current.new_text }` );
            }, text );
        }

        let text = document.body.innerHTML;
        document.body.innerHTML = marker( text, patterns );

        $.ajax({
            type: 'GET',
            async: true,
            url: '/highlight_text/' + id + '/',
            data: "",
            success: function(data) {
                if (data['text'][0] !== undefined){
                    patterns.unshift({text: data['text'][0], classes: ['orange'], new_text: ``})
                    console.log(patterns);
                    let text = document.body.innerHTML;
                    document.body.innerHTML = marker( text, patterns );
                }
            },
            dataType: 'json',
        });

    </script>
{% endblock %}