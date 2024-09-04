function restructure_datatable() {
    $('#datatable_length, #datatable_filter, #datatable_info, #datatable_paginate')
        .addClass('col-sm-6')
        .css({'margin-top': '6px'})
    ;

    $('table').css({'font-size': '14px'});

    $('th.sorting, th.sorting_asc, th.sorting_desc').css({'color': '#337ab7'});

    $('td').css({'vertical-align': 'middle'});

    const $table = $(`#datatable`);

    const $wrapper = $('<div></div>');

    $wrapper.css({
        'overflow-x': 'auto',
        'width': '100%',
        'scrollbar-width': 'none'
    })

    $table.wrap($wrapper);

    $("th>input[type='text']").addClass('form-control');

    $("th>select").select2({
        placeholder: '',
        width: '100%',
        dropdownAutoWidth: true,
        minimumResultsForSearch: -1
    });


}