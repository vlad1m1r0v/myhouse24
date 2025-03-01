function get_indicators_search_params() {
    const params = {};

    if ($flat.val()) params.flat_id = $flat.val();
    if ($date_from.val()) params.date_from = $date_from.val();
    if ($date_to.val()) params.date_to = $date_to.val();

    return new URLSearchParams(params);
};

async function add_indicators() {
    const response = await fetch('../api/indicators/?' + get_indicators_search_params(),
        {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrf_token,
            }
        }
    );

    if (response.ok) {
        const indicators = await response.json();

        // firstly delete all created forms inside formset
        $('#receipt-services tbody tr:visible .delete-service').each(function () {
            $(this).trigger('click');
        })

        indicators.forEach((indicator) => {
            append_form();

            const new_form = $('#receipt-services tbody tr:last-child');
            // meter indicator id hidden field
            new_form.find('td.indicator select').val(indicator.id);
            // service id. Unit updated automatically
            new_form.find('td.service select').val(indicator.service_id).trigger('change');
            // value
            new_form.find('td.value input').val(indicator.value).trigger('change');
            // price per unit
            new_form.find('td.price input').val(indicator.price).trigger('change');
        });

        validate_form();
    };
};

$('.add-indicators').on('click', add_indicators);