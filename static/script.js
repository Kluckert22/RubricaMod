document.getElementById("formulario").addEventListener("submit", async function (e) {
    e.preventDefault();
    const archivo = document.getElementById("archivo").files[0];
    const formData = new FormData();
    formData.append("archivo", archivo);

    const respuesta = await fetch("/procesar", {
        method: "POST",
        body: formData
    });

    const datos = await respuesta.json();
    const original = datos.original;
    const interpolado = datos.interpolado;

    const ctx = document.getElementById("grafica").getContext("2d");
    const tiempo = interpolado.map(x => x.Tiempo);
    const tempOriginal = original.map(x => x.Temperatura);
    const tempInterp = interpolado.map(x => x.Temperatura);

    new Chart(ctx, {
        type: "line",
        data: {
            labels: tiempo,
            datasets: [
                {
                    label: "Original",
                    data: tempOriginal,
                    borderColor: "red",
                    borderWidth: 1,
                    fill: false
                },
                {
                    label: "Interpolado",
                    data: tempInterp,
                    borderColor: "blue",
                    borderWidth: 2,
                    fill: false
                }
            ]
        }
    });

    const tablaDiv = document.getElementById("tabla");
    tablaDiv.innerHTML = "<h3>Datos Interpolados</h3><table><tr><th>Tiempo</th><th>Temperatura</th></tr>" +
        interpolado.map(row => `<tr><td>${row.Tiempo}</td><td>${row.Temperatura}</td></tr>`).join("") + "</table>";
});
