function get_services_params() {
    const params = {};

    if ($tariff.val()) params.tariff_id = $tariff.val();

    return new URLSearchParams(params);
};

async function set_services() {
    const response = await fetch('../api/services/?' + get_services_params(),
        {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrf_token,
            }
        }
    );

    if (response.ok) {
        const services = await response.json();

        // firstly delete all created forms inside formset
        $('#receipt-services tbody tr:visible .delete-service').each(function () {
            $(this).trigger('click');
        })

        services.forEach((service) => {
            append_form();

            const new_form = $('#receipt-services tbody tr:last-child');
            new_form.find('td:nth-child(2) select').val(service.service_id);
            new_form.find('td:nth-child(4) select').val(service.unit_id);
            new_form.find('td:nth-child(5) input').val(service.price);
        });

        validate_form();
    }
}

$('.set-services').on('click', set_services);