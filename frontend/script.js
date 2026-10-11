
const promptInput = document.getElementById("prompt");
const sendButton = document.getElementById("send");
const responseDiv = document.getElementById("response");
const providerSelect = document.getElementById("provider");
const modelSelect = document.getElementById("model");

// Load available models for the selected provider
async function loadModels() {
    const response = await fetch("http://127.0.0.1:8000/models");

    if (!response.ok) {
        throw new Error("Could not load models");
    }

    const providers = await response.json();
    const selectedProvider = providerSelect.value;

    const providerData = providers.find(
        item => item.provider === selectedProvider
    );

    modelSelect.innerHTML = "";

    if (!providerData || providerData.models.length === 0) {
        const option = document.createElement("option");
        option.value = "";
        option.textContent = providerData?.error || "No models available";
        modelSelect.appendChild(option);
        return;
    }

    providerData.models.forEach(modelName => {
        const option = document.createElement("option");
        option.value = modelName;
        option.textContent = modelName;
        modelSelect.appendChild(option);
    });
}

// Send a prompt and display the streamed response
sendButton.addEventListener("click", async () => {
    if (promptInput.value.trim() === "") {
        responseDiv.textContent = "Please enter a question first.";
        return;
    }

    if (!modelSelect.value) {
        responseDiv.textContent = "Please select an available model.";
        return;
    }

    sendButton.disabled = true;
    sendButton.textContent = "Generating response...";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: promptInput.value,
                provider: providerSelect.value,
                model: modelSelect.value,
                level: "beginner",
                length: "short"
            })
        });

        // Display errors returned by the backend
        if (!response.ok) {
            let errorMessage = `HTTP error: ${response.status}`;

            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch {
                // Keep the default error message if the response isn't JSON
            }

            throw new Error(errorMessage);
        }

        if (!response.body) {
            throw new Error("The server returned no response stream.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        responseDiv.textContent = "";

        while (true) {
            const { value, done } = await reader.read();

            if (done) {
                break;
            }

            const chunk = decoder.decode(value, { stream: true });
            responseDiv.textContent += chunk;

            console.log("Received chunk:", chunk);
        }

        // Flush any remaining decoded text
        responseDiv.textContent += decoder.decode();

    } catch (error) {
        console.error(error);
        responseDiv.textContent =
            error.message || "Something went wrong. Please try again.";

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
    }
});

// Load models when the page opens
loadModels().catch(error => {
    console.error("Failed to load models:", error);
    modelSelect.innerHTML = "";

    const option = document.createElement("option");
    option.value = "";
    option.textContent = "Could not load models";
    modelSelect.appendChild(option);
});

// Reload models when the provider changes
providerSelect.addEventListener("change", async () => {
    modelSelect.innerHTML = "";

    const option = document.createElement("option");
    option.textContent = "Loading models...";
    option.value = "";
    modelSelect.appendChild(option);

    try {
        await loadModels();
    } catch (error) {
        console.error("Failed to load models:", error);

        modelSelect.innerHTML = "";

        const errorOption = document.createElement("option");
        errorOption.value = "";
        errorOption.textContent = "Could not load models";
        modelSelect.appendChild(errorOption);
    }
});
