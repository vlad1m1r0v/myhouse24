function generate_strong_password() {
    const uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const lowercase = "abcdefghijklmnopqrstuvwxyz";
    const digits = "0123456789";
    const special_chars = "!@#$%^&*()_+{}:<>?[];,.";

    const get_random_char = (str) => str[Math.floor(Math.random() * str.length)];

    let password = [
        get_random_char(uppercase),
        get_random_char(digits),
        get_random_char(lowercase),
        get_random_char(special_chars)
    ];

    const all_chars = uppercase + lowercase + digits + special_chars;

    while (password.length < 8) {
        password.push(get_random_char(all_chars));
    }

    password = password.sort(() => Math.random() - 0.5);

    return password.join('');
}

$(document).ready(function () {
    $('#generate-password-button').on('click', function () {
        const generated_password = generate_strong_password();
        $('#id_new_password').val(generated_password);
        $('#id_repeat_password').val(generated_password);
    })

    $('#show-password-button').on('click', function () {
        $('#id_new_password').attr('type', (_, attr) => attr === 'password' ? 'text' : 'password');
        $('#id_repeat_password').attr('type', (_, attr) => attr === 'password' ? 'text' : 'password');
    })
})