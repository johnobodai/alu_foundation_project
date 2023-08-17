function logout() {
  var form = document.createElement('form');
  form.method = 'post';
  form.action = '{{ url_for('logout') }}'; // Replace with the actual logout URL

  var csrfField = document.createElement('input');
  csrfField.type = 'hidden';
  csrfField.name = 'csrf_token';
  csrfField.value = '{{ csrf_token() }}'; // Replace with the actual CSRF token

  form.appendChild(csrfField);

  document.body.appendChild(form);
  form.submit();
}

