import { Ollama } from 'https://esm.sh/ollama'
const OLLAMA_HOST = 'https://ollama-clem.lab.sspcloud.fr';

export async function pullModel(modelName) {
  const response = await fetch(`${OLLAMA_HOST}/api/pull`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: modelName })
  });

  if (!response.ok) {
    throw new Error(`Failed to pull model: ${response.statusText}`);
  }
}

export async function askOllama(modelName, prompt, stream = false) {
    await pullModel(modelName);
    const ollama = new Ollama({ host: OLLAMA_HOST });

    const response = await ollama.chat({
        model: modelName,
        messages: [{ role: 'user', content: prompt }],
        stream: stream
    });

    if (stream) {
        return response; // Return the stream object
    } else {
        return response.message.content;
    }
}

// Example for creating a custom model (if needed)
export async function createCustomModel(modelFrom, newModelName, rules) {

  await pullModel(modelFrom);
  const modelfile = `
  FROM ${modelFrom}
  SYSTEM "${rules}"
  `;
  const ollama = new Ollama({ host: OLLAMA_HOST });
  await ollama.create({ model: newModelName, modelfile: modelfile });
}

export async function recuperer_modeles_dispo() {
  const response = await fetch(`${OLLAMA_HOST}/api/tags`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch models: ${response.statusText}`);
  }

  const data = await response.json();
  return data.models
    .map(model => model.name.replace(':latest', ''))
    .filter(name => name); // Enlève les valeurs vides si jamais
}


// ... autres imports et fonctions ...

export async function deleteModel(modelName) {
    const response = await fetch(`${OLLAMA_HOST}/api/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: modelName
      })
    });
  
    if (!response.ok) {
      throw new Error(`Erreur lors de la suppression du modèle: ${response.statusText}`);
    }
  
    return await response.json();
  }