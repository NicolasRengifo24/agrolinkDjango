def guardar_datos_google(backend, user, response, *args, **kwargs):
    """
    Pipeline personalizado que se ejecuta después de que Google
    autentica al usuario. Guarda los datos de Google en la sesión
    para usarlos en el formulario de completar registro.
    """

    # Solo ejecutar para Google
    if backend.name != 'google-oauth2':
        return

    # Guardar datos en la sesión para el formulario
    request = backend.strategy.request

    request.session['google_nombre']   = response.get('given_name', '')
    request.session['google_apellido'] = response.get('family_name', '')
    request.session['google_correo']   = response.get('email', '')
    request.session['google_foto']     = response.get('picture', '')
    request.session['google_user_id']  = user.id