function get_flat_search_params() {
    const params = {};

    if ($flat.val()) params.flat_id = $flat.val();

    return new URLSearchParams(params);
}

async function on_flat_select() {
    const response = await fetch(`${flat_info_url}?${get_flat_search_params()}`,
        {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrf_token,
            },
        }
    );

    if (response.ok) {
        const info = await response.json();
        $account.val(info.account_no);
        $user_name.attr('href', info.owner_url);
        $user_name.text(info.owner_name);
        $user_phone.attr('href', `tel:${info.owner_phone}`);
        $user_phone.text(info.owner_phone);

        const tariff_data = {'id': info.tariff_id, 'text': info.tariff_name};

        if ($tariff.find("option[value='" + tariff_data.id + "']").length) {
            $tariff.val(tariff_data.id).trigger('change');
        } else {
            const option = new Option(tariff_data.text, tariff_data.id, true, true);
            $tariff.append(option).trigger('change');
        }
    }
};

$(document).ready(function () {
    if ($flat.val()) {
        // If we create receipt for flat or duplicate existing receipt we have flat preselected
        // So we can prefetch other data like tariff, personal_account, owner information, etc...
        on_flat_select();

        // Form validation is not initialized yet, so we call it manually
        validate_form();
    }
});

$flat.on('select2:select', on_flat_select);