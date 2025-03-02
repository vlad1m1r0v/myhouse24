const $form = $('#receipt-form');
const $button = $('button[type=submit]');

const validate_form = function () {
    const is_valid = $form.validate({
        ignore: ':hidden, button',
        rules: {
            no: {
                required: true,
                number: true,
            },
            date: {
                required: true,
                date: false,
                ddmmyyyy: true,
            },
            house: {
                required: true,
            },
            section: {
                required: true,
            },
            flat: {
                required: true,
            },
            is_complete: {
                required: false,
            },
            status: {
                required: false,
            },
            tariff: {
                required: true,
            },
            period_from: {
                required: true,
                date: false,
                ddmmyyyy: true,
            },
            period_to: {
                required: true,
                date: false,
                ddmmyyyy: true,
            },
            personal_account: {
                required: true,
                number: true,
            },
        },
        messages: {
            no: {
                required: 'Введіть номер квитанції',
                number: 'Номер квитанції має бути числом'
            },
            date: {
                required: 'Вкажіть дату',
                ddmmyyyy: 'Вкажіть валідну дату'
            },
            house: {
                required: 'Вкажіть будинок'
            },
            section: {
                required: 'Вкажіть секцію'
            },
            flat: {
                required: 'Вкажіть квартиру'
            },
            tariff: {
                required: 'Вкажіть тариф'
            },
            period_from: {
                required: 'Вкажіть початковий період',
                ddmmyyyy: 'Вкажіть валідну дату'
            },
            period_to: {
                required: 'Вкажіть кінцевий період',
                ddmmyyyy: 'Вкажіть валідну дату'
            },
            personal_account: {
                required: 'Введіть особовий рахунок',
                number: 'Особовий рахунок має складатись з цифр'
            },
        },
        errorElement: 'small',
        errorPlacement: function (error, element) {
            error.css({'color': 'red'});
            const parent = element.closest('.form-group');
            parent.hasClass('form-group') ? parent.append(error) : element.after(error);
        },
        highlight: function (element) {
            const $el = $(element);
            const parent = $el.closest('.form-group, td');
            parent.addClass('has-error');
            $el.addClass('is-invalid');
        },
        unhighlight: function (element) {
            const $el = $(element);
            const parent = $el.closest('td, .form-group');
            parent.removeClass('has-error').addClass('has-success');
            $el.removeClass('is-invalid').addClass('is-valid');
        }
    }).checkForm();

    $('#receipt-services > tbody > tr > td.service select, ' +
        '#receipt-services > tbody > tr > td.unit select').each(function () {
        $(this).rules('add', {
            required: true,
            messages: {
                required: 'Не вибрано',
            }
        });
    });

    $('#receipt-services > tbody > tr > td.value input, ' +
        '#receipt-services > tbody > tr > td.price input, ' +
        '#receipt-services > tbody > tr > td.total input').each(function () {
        $(this).rules('add', {
            required: true,
            messages: {
                required: 'Не вказано',
            }
        });
    });

    if (is_valid) {
        $button.prop('disabled', false);
    } else {
        $button.prop('disabled', 'disabled');
    }
}

$form.on('focus change keyup blur', 'input,select', function () {
    validate_form();
});


// proper validation for date widgets
// validate when we pick date
$date.on('changeDate', function () {
    $(this).trigger('change').valid();
});

$date_from.on('changeDate', function () {
    $(this).trigger('change').valid();
});


$date_to.on('changeDate', function () {
    $(this).trigger('change').valid();
});


// proper validation for select2
// validate if we open or close select2 widgets
$('.select').on('select2:opening select2:closing', function () {
    $(this).trigger('blur');
});

// for preload from entering account number or selecting flat
$('.select').on('change', function () {
    $(this).valid();
});


// clean section if we deselect house
$house.on('change', function () {
    $section.val('').trigger('change').valid();
});

// clean flat if we deselect section
$section.on('change', function () {
    $flat.val('').trigger('change').valid();
});

// proper validation of inputs and selects of forms inside formset
$(document).on('focus change keyup blur', '#receipt-services tbody tr:visible td:visible input, #receipt-services tbody tr:visible td:visible select', function () {
        $(this).valid();
    }
);