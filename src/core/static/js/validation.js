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