fetch('http://0.0.0.0:8000/api/method/frappe.auth.get_logged_user', {
    headers: {
        'Authorization': 'token 1e75f8ce2564dea:4c9ae925a139c0a'
    }
})
.then(r => r.json())
.then(r => {
    console.log(r);
})