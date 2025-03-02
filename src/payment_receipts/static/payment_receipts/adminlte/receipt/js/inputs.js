// get all inputs
const $no = $("#id_no");
const $house = $("#id_house");
const $section = $("#id_section");
const $flat = $("#id_flat");
const $account = $("#id_personal_account");
const $tariff = $("#id_tariff");
const $date = $('#id_date');
const $date_from = $('#id_period_from');
const $date_to = $('#id_period_to');
const $user_name = $('#user-name');
const $user_phone = $('#user-phone');

// default settings for select2
$.fn.select2.defaults.set('language', 'uk');
$.fn.select2.defaults.set('width', '100%');
$.fn.select2.defaults.set('placeholder', 'Виберіть...');
$.fn.select2.defaults.set('allowClear', true);


$(document).ready(function () {
    // dates
    $date.datepicker({
        autoclose: true,
        language: 'uk',
    });

    $date_from.datepicker({
        autoclose: true,
        language: 'uk',
    });

    $date_to.datepicker({
        autoclose: true,
        language: 'uk',
    });

// open calendar when we click on icon
    $('.kv-date-calendar').click(function () {
        $(this).parent().find('input').focus();
    });

// select2
    $house.select2({
        ajax: {
            url: houses_url,
            processResults: data => ({results: data})
        },
    });

    $section.select2({
        ajax: {
            url: sections_url,
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
            url: flats_url,
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
            url: tariffs_url,
            processResults: data => ({results: data})
        },
    });

})
