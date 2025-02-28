const datatable = new DataTable('#datatable', {
    order: [],
    lengthChange: false,
    searching: false,
    processing: true,
    serverSide: true,
    scrollX: true,
    columnDefs: [
        {
            className: "dt-head-center",
            orderable: false,
            targets: '_all'
        },
        {
            className: "dt-left",
            targets: [2]
        },
        {
            className: "dt-center",
            targets: [0, 1, 2, 3, 5, 6, 8, 9]
        },
        {
            className: "dt-center",
            targets: [1, 8, 9]
        }],
    rowCallback: function (row) {
        $('td', row).css({
            'vertical-align': 'middle',
            'padding': '10px'
        });

        $('td:eq(8), td:eq(9)', row).css('background-color', '#DFD5');
    },
    language: {
        url: 'https://cdn.datatables.net/plug-ins/2.2.2/i18n/uk.json'
    },
    ajax: {
        url: "../api/datatable/",
        data: function (params) {
            params.house_id = $house.val();
            params.section_id = $section.val();
            params.flat_id = $flat.val();

            params.date_from = $date_from.val();
            params.date_to = $date_to.val();
        },
    },
    columns: [
        {data: "no"},
        {data: "status"},
        {data: "date"},
        {data: "month"},
        {data: "house"},
        {data: "section"},
        {data: "flat"},
        {data: "service"},
        {data: "value"},
        {data: "unit"},
    ],
});

$date_from.on('changeDate', function () {
    datatable.columns(2).search($(this).val()).draw();
});

$date_to.on('changeDate', function () {
    datatable.columns(2).search($(this).val()).draw();
})

$house.on('change', function () {
    datatable.columns(4).search($(this).val()).draw();
});

$section.on('change', function () {
    datatable.columns(5).search($(this).val()).draw();
})

$flat.on('change', function () {
    datatable.columns(6).search($(this).val()).draw();
});