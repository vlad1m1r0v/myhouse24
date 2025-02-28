function get_indicators_search_params() {
    const params = {
        flat_id: $flat.val(),
        date_from: $date_from.val(),
        date_to: $date_to.val()
    };

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

        $('#receipt-services tbody tr:visible').each(function () {
            const $tr = $(this);

            const service_id = parseFloat($tr.find('td:nth-child(2) select').val());

            const indicator = indicators.find((item) => item.service_id === service_id);

            if (indicator) {
                $tr.find('td:nth-child(1) input').val(indicator.id);
                $tr.find('td:nth-child(3) input').val(indicator.value).trigger('change');
            };
        });
    }
};

$('.add-indicators').on('click', add_indicators);