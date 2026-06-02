from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"}),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"placeholder": "Escribe tu mensaje aquí..."}),
    )

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get("mensaje", "")
        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje debe tener al menos 10 caracteres."
            )
        return mensaje
