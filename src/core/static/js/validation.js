$.validator.addMethod(
    "valid_email",
    function (value, element) {
        const regexp = new RegExp(/^\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i);
        return this.optional(element) || regexp.test(value);
    }, "Невірна адреса електронної пошти"
);

$.validator.addMethod(
    "strong_password",
    function (value, element) {
        const hasUpperCase = new RegExp(/[A-Z]/).test(value);
        const hasDigit = new RegExp(/[0-9]/).test(value);
        return this.optional(element) || (hasUpperCase && hasDigit);
    },
    "Пароль повинен містити щонайменше одну велику літеру та одну цифру"
);

$.validator.addMethod(
    "phone_ua",
    function (value, element) {
        const phoneRegex = /^\+38\(0\d{2}\)-\d{3}-\d{2}-\d{2}$/;
        return this.optional(element) || phoneRegex.test(value);
    },
    "Вкажіть коректний номер телефону"
);

$.validator.addMethod(
    "map_iframe",
    function (value, element) {
        const mapIframeRegex = /<iframe\s*src="https:\/\/www\.google\.com\/maps\/embed\?[^"]+"\s*[^>]*><\/iframe>/i;
        return this.optional(element) || mapIframeRegex.test(value);
    },
    "Вкажіть коректний код карти"
);

$.validator.addMethod("birth_date", function (value, element) {
    const regex = /^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$/;

    if (!regex.test(value)) {
        return false;
    }

    const parts = value.split('.');
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1;
    const year = parseInt(parts[2], 10);

    const date = new Date(year, month, day);

    return date.getDate() === day && date.getMonth() === month && date.getFullYear() === year;
}, "Введіть правильну дату народження в форматі DD.MM.YYYY");

$.validator.addMethod("viber", function (value, element) {
    const viberRegex = /^viber:\/\/chat\?number=\+380\d{9}$/;
     return this.optional(element) || viberRegex.test(value);
}, "Вкажіть валідну адресу в Viber");

$.validator.addMethod("telegram", function (value, element) {
    const telegramRegex = /^https:\/\/t\.me\/\w{3,}$/;
     return this.optional(element) || telegramRegex.test(value);
}, "Вкажіть валідну адресу в Telegram");

$.validator.addMethod("ddmmyyyy", function (value, element) {
    const pattern =/^([0-9]{2})\.([0-9]{2})\.([0-9]{4})$/;
    return this.optional(element) ||  pattern.test(value);
}, "Вкажіть валідну дату");

$.validator.addMethod("hhmm", function (value, element) {
    const pattern =/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/;
    return this.optional(element) ||  pattern.test(value);
}, "Вкажіть валідний час");