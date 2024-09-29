function restructure_datatable() {
    // positioning search input and pagination select, pagination block and results information in the same row
    $('#datatable_length, #datatable_filter, #datatable_info, #datatable_paginate')
        .addClass('col-sm-6')
        .css({'margin-top': '6px'})
    ;

    // enlarge font size
    $('table').css({'font-size': '14px'});

    // highlight column titles with blue
    $('th.sorting, th.sorting_asc, th.sorting_desc').css({'color': '#337ab7'});

    // align text inside cell in middle
    $('td').css({'vertical-align': 'middle'});

    // make table scrollable horizontally if we have overflow
    const $table = $(`#datatable`);

    const $wrapper = $('<div></div>');

    $wrapper.css({
        'overflow-x': 'auto',
        'width': '100%',
        'scrollbar-width': 'none'
    })

    $table.wrap($wrapper);

    // make column filters look prettier using bootstrap form-control class
    $("th>input[type='text']").addClass('form-control');

    // make select filters look prettier using select2 library
    $("th>select").select2({
        placeholder: '',
        width: '100%',
        dropdownAutoWidth: true,
        minimumResultsForSearch: -1
    });

    // disable border radius for search input
    $("input[type=search]").css({'border-radius': '0'});
}