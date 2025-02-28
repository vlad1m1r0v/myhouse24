function get_flat_search_params() {
    const params = {};

    if ($flat.val()) params.set('flat_id', $flat.val());

    return new URLSearchParams(params);
}

async function on_flat_select() {
    const response = await fetch('../api/flat-info/',
        {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrf_token,
            },
            body: get_flat_search_params()
        }
    );

    if (response.ok) {
        const info = await response.json();
        $account.val(info.account_no);
        $user_name.attr('href', `../../flat-owners/${info.owner_id}/`);
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

$flat.on('select2:select', on_flat_select);