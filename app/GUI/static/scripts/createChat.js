
const createChatButton = document.getElementById("createChat");
const createChatForm = document.getElementById("createChatForm")
// Открытие формы создания чата

createChatButton.addEventListener("click", () => {
    darkenBg.classList.remove('hidden');
    darkenBg.style.opacity = '0.5';
    createChatForm.classList.remove('hidden');
    setTimeout(() => {
        createChatForm.style.opacity = '1';
        createChatForm.style.transform = 'scale(1)';
    }, 10);
});


