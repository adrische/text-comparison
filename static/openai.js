document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById('submit-button');
    const apiKeyInput = document.getElementById('api-key');
        
    const responseDiv = document.getElementById('chatgpt-response');

    submitButton.addEventListener('click', function () {
        const text1 = document.getElementById("text1").value;
        const text2 = document.getElementById("text2").value;
        
        const apiKey = apiKeyInput.value.trim();
        const apiUrl = 'https://api.openai.com/v1/chat/completions';
        const predefinedPrompt = "Compare the following two texts and briefly explain your reasoning. Then express the similarity of the two texts on a scale 1 to 5, where 5 means most similar, and 1 means least similar.";

        if (!apiKey) {
            responseDiv.innerText = 'Please enter your API key.';
            return;
        }

        const prompt = predefinedPrompt + "\nnText 1: " + text1 + "\nnText 1: " + text2;

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: "gpt-3.5-turbo",
                messages: [{role: "user", content: prompt}],
                max_tokens: 200,
            })
        })
        .then(response => response.json())
        .then(data => {
            const completion = data.choices[0].message.content;
            responseDiv.innerText = completion;
        })
        .catch(error => {
            console.error('Error:', error);
            responseDiv.innerText = 'An error occurred';
        });
    });
});
