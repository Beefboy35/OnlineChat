
const AddToChatButton = document.getElementById("addToChat");
const AddToChatForm = document.getElementById("addToChatForm")
// Открытие формы создания чата

AddToChatButton.addEventListener("click", () => {
    darkenBg.classList.remove('hidden');
    darkenBg.style.opacity = '0.5';
    AddToChatForm.classList.remove('hidden');
    setTimeout(() => {
        AddToChatForm.style.opacity = '1';
        AddToChatForm.style.transform = 'scale(1)';
    }, 10);
});
