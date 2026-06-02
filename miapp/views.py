from django.shortcuts import render
from .forms import ContactoForm


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            correo = form.cleaned_data["correo"]
            mensaje = form.cleaned_data["mensaje"]
            print(f"📩 Nuevo mensaje de {nombre} ({correo}):")
            print(f"   {mensaje}")
            return render(request, "miapp/contacto.html", {
                "form": ContactoForm(),
                "exito": True,
            })
    else:
        form = ContactoForm()

    return render(request, "miapp/contacto.html", {"form": form})
