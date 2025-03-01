// formset
const $service_extra_form = $('#receipt-services tbody tr:last-child');
const $service_form_clone = $service_extra_form.clone(true);
$service_extra_form.hide();

function append_form() {
    const $total_forms = $('#id_receiptservice_set-TOTAL_FORMS');
    const count = parseInt($total_forms.val());

    const form_markup = $service_form_clone.prop('outerHTML');
    const regex = /receiptservice_set-(\d+)-/g;
    const form = form_markup.replace(regex, `receiptservice_set-${count}-`);

    $('#receipt-services tbody').append(form);

    $total_forms.attr('value', count + 1);
}

// add form
$('#add-service').on('click', function () {
    append_form();
    validate_form();
});

// delete form
$(document).on('click', '.delete-service', function () {
    $(this).closest('td').find('input[type=checkbox]').attr('checked', true);
    $(this).closest('tr').hide();
    update_costs();
    validate_form();
});

// syncing services and units selects
$(document).on('change', '#receipt-services > tbody > tr > td.service select', function () {
    const unit_id = $(this).find('option:selected').data('unit-id');
    $(this).closest('tr').find('td.unit > select').val(unit_id).valid();
});

$(document).ready(function () {
    $('#id_receiptservice_set-INITIAL_FORMS').attr('value', 0);
    $('#receipt-services > tbody > tr > td.indicator select').val(null);
    update_costs();
});
