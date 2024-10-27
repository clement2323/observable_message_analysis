---
title: Ollama
---

```js
import {askOllama, pullModel, createCustomModel} from "./utils/ollama_call.js";
import Markdown from 'https://esm.sh/react-markdown@9'
```

```js
const question = view(Inputs.textarea({
  label: "Question", 
  placeholder: "Posez votre question",
  submit: "Valider"
}));
```

```jsx
//import ReactMarkdown from 'react-markdown'

function OllamaResponse({ question }) {
  const [reponse, setReponse] = React.useState("");

  React.useEffect(() => {
    async function fetchResponse() {
      try {
        const streamResponse = await askOllama("mistral-small", question, true);
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
      <Markdown>{reponse}</Markdown>
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



