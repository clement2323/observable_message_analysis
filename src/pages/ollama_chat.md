---
title: Ollama
---

```js
import {askOllama,recuperer_modeles_dispo,pullModel} from "../utils/ollama_call.js";
import ReactMarkdown from 'https://esm.sh/react-markdown@9'
```

```js
const question = view(Inputs.textarea({
  label: "Question", 
  placeholder: "Posez votre question",
  submit: "Valider"
}));
```
```js
const liste_modeles =recuperer_modeles_dispo();
```
```js
const modeles_dispo = view(Inputs.select(liste_modeles, {value: "steelblue", label: "modèle"}));
```


```jsx
function OllamaResponse({ question }) {
  const [reponse, setReponse] = React.useState("");

  React.useEffect(() => {
    async function fetchResponse() {
      try {
        const streamResponse = await askOllama(modeles_dispo, question, true);
        for await (const part of streamResponse) {
          if (part.message?.content) {
            setReponse(prev => prev + part.message.content);
          }
        }
      } catch (error) {
        console.error("Erreur lors de la récupération de la réponse:", error);
        setReponse("Une erreur s'est produite lors de la récupération de la réponse.");
      }
    }
    
    if (question) {
      setReponse(""); // Réinitialiser la réponse lorsque la question change
      fetchResponse();
    }
  }, [question]);

  return (
    <div 
      style={{
        border: '1px solid black',
        padding: '10px',
        minHeight: '100px'
      }}
    >
   <ReactMarkdown>{reponse}</ReactMarkdown>
    </div>
  );
}
```

```jsx
display(
  <div>
    <h3>Réponse:</h3>
    <OllamaResponse question={question} />
  </div>
);
```


```jsx
// FAIRE uneexmple pour le GT qui use des customs modeles
// Faire un OLLAMA CALL POUR GENERER DES EMBEDDINGS DANS L'API ...
// GENERATE EMBEDDINGS DANS L'API ...
```



