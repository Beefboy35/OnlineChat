  window.addEventListener("DOMContentLoaded", async () => {
       try {
           await axios.post("auth/refresh");
       } catch (e) {
           console.log("error receiving jwt tokens:", e);
           window.location.href = "/login";
       }
   });


const roomData = document.getElementById("room-data");
const roomIdInput = document.getElementById("roomId");
const username = roomData.getAttribute("data-username");
const userId = roomData.getAttribute("data-user-id");
const connectButton = document.getElementById("connectToTheRoom");
connectButton.addEventListener("click", async () => {
    const roomId = roomIdInput.value;
    const nickname = username; // Убедитесь, что nickname задан
    ws = new WebSocket(`/ws/chat/${roomId}/${userId}/${nickname}`);

    ws.onopen = () => {
        console.log("Соединение установлено");
    };

    ws.onclose = () => {
        console.log("Соединение закрыто");
    };

    ws.onmessage = (event) => {
        const messages = document.getElementById("messages");
        const messageData = JSON.parse(event.data);
        const message = document.createElement("div");

        // Определяем стили в зависимости от отправителя
        if (messageData.is_self) {
            message.className = "p-2 my-1 bg-blue-500 text-white rounded-md self-end max-w-xs ml-auto";
        } else {
            message.className = "p-2 my-1 bg-gray-200 text-black rounded-md self-start max-w-xs";
        }

        message.textContent = messageData.text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight; // Автопрокрутка вниз
    };
});
const profileForm = document.getElementById("profileForm");
const darkenBg = document.getElementById("darkenBg");
document.getElementById("getProfile").addEventListener("click", () => {
    darkenBg.classList.remove('hidden');
    darkenBg.style.opacity = '0.5';
    profileForm.classList.remove('hidden');
    setTimeout(() => {
        profileForm.style.opacity = '1';
        profileForm.style.transform = 'scale(1)';
    }, 10);
});

document.getElementById("closeForm").addEventListener("click", () => {
    profileForm.style.opacity = '0';
    profileForm.style.transform = 'scale(0.2)';
    darkenBg.style.opacity = '0';
    setTimeout(() => {
        profileForm.classList.add('hidden');
        darkenBg.classList.add('hidden');
    }, 300);
});