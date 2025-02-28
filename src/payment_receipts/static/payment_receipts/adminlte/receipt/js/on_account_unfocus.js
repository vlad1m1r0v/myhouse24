function get_account_search_params() {
    const params = {};

    if ($account.val()) params.account_no = $account.val();

    return new URLSearchParams(params);
}


async function on_account_unfocus() {
    const response = await fetch('../api/flat-info-by-account/?' + get_account_search_params(),
        {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrf_token,
            }
        }
    );

    if (response.ok) {
        const info = await response.json();
        $user_name.attr('href', `../../flat-owners/${info.owner_id}/`);
        $user_name.text(info.owner_name);
        $user_phone.attr('href', `tel:${info.owner_phone}`);
        $user_phone.text(info.owner_phone);

        // preselect house
        const house_data = {'id': info.house_id, 'text': info.house_name};

        if ($house.find("option[value='" + house_data.id + "']").length) {
            $house.val(house_data.id).trigger('change');
        } else {
            const option = new Option(house_data.text, house_data.id, true, true);
            $house.append(option).trigger('change');
        }

        // preselect section
        const section_data = {'id': info.section_id, 'text': info.section_name};

        if ($section.find("option[value='" + section_data.id + "']").length) {
            $section.val(section_data.id).trigger('change');
        } else {
            const option = new Option(section_data.text, section_data.id, true, true);
            $section.append(option).trigger('change');
        }

        // preselect flat
        const flat_data = {'id': info.flat_id, 'text': info.flat_name};

        if ($flat.find("option[value='" + flat_data.id + "']").length) {
            $flat.val(flat_data.id).trigger('change');
        } else {
            const option = new Option(flat_data.text, flat_data.id, true, true);
            $flat.append(option).trigger('change');
        }

        // preselect tariff
        const tariff_data = {'id': info.tariff_id, 'text': info.tariff_name};

        if ($tariff.find("option[value='" + tariff_data.id + "']").length) {
            $tariff.val(tariff_data.id).trigger('change');
        } else {
            const option = new Option(tariff_data.text, tariff_data.id, true, true);
            $tariff.append(option).trigger('change');
        }
    }
};

$account.on('blur', on_account_unfocus);