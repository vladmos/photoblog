$(document).ready(function() {
    $('.dropdown-toggle').dropdown();

    var $menu = $('#photoalbum-select .dropdown-menu');

    $menu.delegate('a', 'click', function(event) {
        var $menu_item = $(this);
        selectAlbum($menu_item);
    });

    /*
    var $first = $('a', $menu.children(':first-child'));

    if ($first) {
        $first.click();
    }
    */

    function selectAlbum($menu_item) {
        console.log($menu_item);
        $.ajax({
            url: $menu_item[0].id,
            success: function(data) {
                $('#photoalbum-select .dropdown-caption').html($menu_item.html());
                $menu_item.parent().parent().children().removeClass('active');
                $menu_item.parent().addClass('active');
                $('#photoalbum-preview').html(data);
            }
        })
    }
});