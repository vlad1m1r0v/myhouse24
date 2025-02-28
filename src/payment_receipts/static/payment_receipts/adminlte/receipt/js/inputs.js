// get all inputs
const $no = $("#id_no");
const $house = $("#id_house");
const $section = $("#id_section");
const $flat = $("#id_flat");
const $account = $("#id_personal_account");
const $tariff = $("#id_tariff");
const $date_from = $('#id_period_from');
const $date_to = $('#id_period_to');
const $user_name = $('#user-name');
const $user_phone = $('#user-phone');

// no
$no.val(Date.now());

// dates
const $dates = $('.date');

$dates.datepicker({
    autoclose: true,
    language: 'uk',
});

// set current date by default
$dates.datepicker("setDate", new Date());

// open calendar when we click on icon
$('.kv-date-calendar').click(function () {
    $(this).closest('.date').focus();
});

$.fn.select2.defaults.set('language', 'uk');
$.fn.select2.defaults.set('width', '100%');
$.fn.select2.defaults.set('placeholder', 'Виберіть...');
$.fn.select2.defaults.set('allowClear', true);

// select2
$house.select2({
    ajax: {
        url: '../api/houses/',
        processResults: data => ({results: data})
    },
});

$section.select2({
    ajax: {
        url: '../api/sections/',
        data: function (params) {
            return {
                term: params.term,
                house_id: $house.val()
            }
        },
        processResults: data => ({results: data})
    },
});

$flat.select2({
    ajax: {
        url: '../api/flats/',
        data: function (params) {
            return {
                term: params.term,
                section_id: $section.val()
            }
        },
        processResults: data => ({results: data})
    },
});

$tariff.select2({
    ajax: {
        url: '../api/tariffs/',
        processResults: data => ({results: data})
    },
});