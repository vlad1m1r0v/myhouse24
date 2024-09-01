function restructure_datatable() {
    $('#datatable_length, #datatable_filter, #datatable_info, #datatable_paginate')
        .addClass('col-sm-6')
        .css({'margin-top': '6px'})
    ;

    $('table').css({'font-size': '14px'});
}