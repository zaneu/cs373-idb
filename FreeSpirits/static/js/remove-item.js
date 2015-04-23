// Note that this code is passed in the parameters from the Jinja
// templating engine

function remove_item(user_id, item_id, item_type) {
    user_id = parseInt(user_id, 10);
    item_id = parseInt(item_id, 10);
    $.post('/api/remove-item', {
        user_id: user_id,
        item_id: item_id,
        item_type: item_type
    });
    $('#' + item_type + item_id).hide();
}
