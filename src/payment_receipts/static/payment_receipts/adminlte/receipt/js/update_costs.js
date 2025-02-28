// update cost for each service based on its price and value
// then calculate total price
function update_costs() {
    $('#receipt-services tbody tr:visible').each(function () {
        const $tr = $(this);

        const value = parseFloat($tr.find('td:nth-child(3) input').val()) || 0;
        const price = parseFloat($tr.find('td:nth-child(5) input').val()) || 0;

        const cost = value * price;
        $tr.find('td:nth-child(6) input').val(cost.toFixed(2)).valid();
    });

    let total = 0;

    $('#receipt-services tr:visible td:nth-child(6) input').each(function () {
        total += parseFloat($(this).val()) || 0;
    });

    $('#total-cost').text(total.toFixed(2));
}

// update costs each time we change price per unit or value
$(document).on('change', "#receipt-services tbody tr td:nth-child(3) input, #receipt-services tbody tr td:nth-child(5) input", function () {
    update_costs();
});