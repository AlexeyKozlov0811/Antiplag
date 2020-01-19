{% block scripts %}
{% load staticfiles %}
    <script src="{% static 'app/scripts/ajax.js' %}">
    </script>

    <script>
        let patterns = [
            {text: "123", classes: ['orange']},
            //{text: "Python (найчастіше вживане прочитання — «Па?йтон», запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на всіх основних платформах. В мові програмування Python підтримується ", classes: ['orange']},
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