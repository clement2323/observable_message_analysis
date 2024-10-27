---
title: Ollama
---

```js
import {askOllama, pullModel, createCustomModel} from "./utils/ollama_call.js";
```

```js
const question = view(Inputs.textarea({
  label: "Question", 
  placeholder: "Posez votre question",
  submit: "Valider"
}));
```

```jsx

function OllamaResponse({ question }) {
  const [reponse, setReponse] = React.useState("");

  React.useEffect(() => {
    async function fetchResponse() {
      const streamResponse = await askOllama("llama2", question, true);
      for await (const part of streamResponse) {
        if (part.message && part.message.content) {
          setReponse(prev => prev + part.message.content);
        }
      }
    }
    
    if (question) {
      setReponse(""); // Reset response when question changes
      fetchResponse();
    }
  }, [question]);

  return (
    <div style={{
      border: '1px solid black',
      padding: '10px',
      fontStyle: 'italic',
      minHeight: '100px'
    }}>
      {reponse}
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



