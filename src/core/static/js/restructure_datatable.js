function restructure_datatable() {
    $('#datatable_length, #datatable_filter, #datatable_info, #datatable_paginate')
        .addClass('col-sm-6')
        .css({'margin-top': '6px'})
    ;

    $('table').css({'font-size': '14px'});

    $('th.sorting, th.sorting_asc, th.sorting_desc').css({'color': '#337ab7'});

    $("th>input[type='text']").addClass('form-control');
}