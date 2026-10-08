const promptInput = document.getElementById("prompt");
const sendButton = document.getElementById("send");
const responseDiv = document.getElementById("response");


sendButton.addEventListener("click",async ()=>{

    const response=await fetch("http://127.0.0.1:8000/chat/stream",{
        method:"POST",
        headers:{
            "content-type":"application/json"
        },
        body:JSON.stringify({
            prompt:promptInput.value,
            provider:"ollama",
            model: "qwen2.5:0.5b",
            level: "beginner",
            length: "short"

    })
    })

    const reader=response.body.getReader()
    const decoder= new TextDecoder()
    responseDiv.textContent=""
    while(true){
        
    }




})
