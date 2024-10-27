```js
import {recuperer_modeles_dispo,createCustomModel,deleteModel,pullModel} from "../utils/ollama_call.js";
```

```js
const liste_modeles = await recuperer_modeles_dispo();
const createModelForm = view(Inputs.form({
  baseModel: Inputs.select(liste_modeles, {
    label: "Modèle de base",
    value: "steelblue"
  }),
  newModelName: Inputs.text({
    label: "Nom du nouveau modèle",
    placeholder: "mon-modele-personnalise"
  }),
  rules: Inputs.textarea({
    label: "Règles du modèle",
    placeholder: "Décrivez le comportement souhaité du modèle...",
    rows: 10
  })
}, {
  template: (formParts) => html`
    <div style="margin-top: 20px; border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
      <h3>Créer un modèle personnalisé</h3>
      <div style="display: grid; gap: 15px;">
        <div style="display: flex; gap: 10px;">
          ${formParts.baseModel}
          ${formParts.newModelName}
        </div>
        <div>
          ${formParts.rules}
        </div>
        <button id="createButton" onclick=${async (e) => {
          const button = e.target;
          const statusDiv = document.getElementById('statusMessage');
          
          try {
            button.disabled = true;
            statusDiv.textContent = "Création du modèle en cours... Veuillez patienter.";
            statusDiv.style.color = "orange";
            
            await createCustomModel(
              formParts.baseModel.value,
              formParts.newModelName.value,
              formParts.rules.value
            );
            
            statusDiv.textContent = "Modèle créé avec succès !";
            statusDiv.style.color = "green";
          } catch (error) {
            console.error("Erreur lors de la création du modèle:", error);
            statusDiv.textContent = "Erreur lors de la création du modèle.";
            statusDiv.style.color = "red";
          } finally {
            button.disabled = false;
          }
        }}>Créer le modèle</button>
        <div id="statusMessage"></div>
      </div>
    </div>
  `
}));
```


```js
// Créer un état observable pour la liste des modèles
const liste_modeles_effacables = await recuperer_modeles_dispo();
```
```js
const select_modeles_effacables = view(Inputs.select(liste_modeles_effacables, {
    label: "Modèles effacables",
    value: null
}));
```
```js
const time = view(Inputs.button("Effacer modèle", {
  value: 0,
  reduce: async () => {
    await deleteModel(select_modeles_effacables); // Correction: ajout de .value
    // Mettre à jour la liste après suppression
  }
}));

```


```js
const text = view(Inputs.text({
    label: "Nom du modèle",
    placeholder: "Entrez le nom du modèle",
    value: ""
  }));
```

```js
const push = view(Inputs.button("Pusher le modèle", {
  value: 0,
  reduce: async () => {
    await pullModel(text); // Correction: ajout de .value
    // Mettre à jour la liste après suppression
  }
}));
```

