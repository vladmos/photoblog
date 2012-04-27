$(document).ready(function() {
    $('.dropdown-toggle').dropdown();
});

function initArticleEditor() {
    jQuery.fn.extend({
        insertAtCaret: function(myValue){
            return this.each(function(i) {
                if (document.selection) {
                    //For browsers like Internet Explorer
                    this.focus();
                    sel = document.selection.createRange();
                    sel.text = myValue;
                    this.focus();
                }
                else if (this.selectionStart || this.selectionStart == '0') {
                    //For browsers like Firefox and Webkit based
                    var startPos = this.selectionStart;
                    var endPos = this.selectionEnd;
                    var scrollTop = this.scrollTop;
                    this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
                    this.focus();
                    this.selectionStart = startPos + myValue.length;
                    this.selectionEnd = startPos + myValue.length;
                    this.scrollTop = scrollTop;
                } else {
                    this.value += myValue;
                    this.focus();
                }
            })
        }
    });

    var $menu = $('#photoalbum-select .dropdown-menu');

    $menu.delegate('a', 'click', function(event) {
        var $menu_item = $(this);
        selectAlbum($menu_item);
        $(this).closest('.dropdown').click();
        return false;
    });

    var $tab_preview = $('#tab-preview'),
        $tab_edit = $('#tab-edit'),
        $panel_preview = $('#panel-preview'),
        $panel_edit = $('#panel-edit'),
        $textarea = $('#id_raw_text');

    $tab_preview.delegate('', 'click', function() {
        $tab_preview.parent().addClass('active');
        $tab_edit.parent().removeClass('active');

        $panel_preview.show();
        $panel_edit.hide();

        $panel_preview.html('<h2>Loading...</h2>');

        $.ajax({
            url: '/admin/ajax/article/',
            type: 'post',
            data: 'text=' + encodeURIComponent($textarea.val()),
            success: function(text) {
                console.log(text);
                $panel_preview.html(text);
            }
        });

        return false;
    });

    $tab_edit.delegate('', 'click', function() {
        $tab_edit.parent().addClass('active');
        $tab_preview.parent().removeClass('active');

        $panel_edit.show();
        $panel_preview.hide();

        return false;
    });

    $($panel_edit).delegate('input, textarea', 'focus', function() {
        $('.alert-success .close').click();
    });

    $('#photoalbum-preview').delegate('.thumbnail img', 'click', function(event) {
        var $this = $(this),
            photo_tag = '[' + $this[0].id + ']';
        $textarea.insertAtCaret(photo_tag);
        $textarea.focus();
    })

    var dates = $('#id_event_beginning, #id_event_end').datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        dateFormat: 'dd.mm.yy',
        onSelect: function(selectedDate) {
            var option = this.id == "id_event_beginning" ? "minDate" : "maxDate",
                instance = $(this).data("datepicker"),
                date = $.datepicker.parseDate(
                    instance.settings.dateFormat ||
                        $.datepicker._defaults.dateFormat,
                    selectedDate, instance.settings );
            dates.not(this).datepicker("option", option, date);
        }
    });

    var selectAlbum = function($menu_item) {
        $.ajax({
            url: $menu_item[0].id,
            success: function(data) {
                var $preview = $('#photoalbum-preview');

                $('#photoalbum-select .dropdown-caption').html($menu_item.html());
                $menu_item.parent().parent().children().removeClass('active');
                $menu_item.parent().addClass('active');
                $preview.html(data);
            }
        });
    };
}
