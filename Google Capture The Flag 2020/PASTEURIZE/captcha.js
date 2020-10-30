function captcha_cb(token){
    document.querySelectorAll('form').forEach(form=>{
        console.log('token', token);
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('name', 'g-recaptcha-response');
        input.setAttribute('value', token);
        input.setAttribute('hidden', '1');
        form.appendChild(input);
    });
}