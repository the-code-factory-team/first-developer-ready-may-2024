$( document ).ready(function() {
    $('.but-red').click(function (event) {
        if($(this).text() !== 'Вы уверены? 🧐' && $(this).text().indexOf("На главную") <= 0 && $(this).text().indexOf("Назад") <= 0) {
            event.preventDefault();

            $(this).removeClass('but-red');
            $(this).addClass('but-danger-2');
            $(this).text('Вы уверены? 🧐');
        }
    });
});