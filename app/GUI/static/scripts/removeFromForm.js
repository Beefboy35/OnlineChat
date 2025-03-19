
const RemoveFromButton = document.getElementById("removeFromChat");
const RemoveFromForm = document.getElementById("removeForm")
// Открытие формы создания чата

RemoveFromButton.addEventListener("click", () => {
    darkenBg.classList.remove('hidden');
    darkenBg.style.opacity = '0.5';
    RemoveFromForm.classList.remove('hidden');
    setTimeout(() => {
        RemoveFromForm.style.opacity = '1';
        RemoveFromForm.style.transform = 'scale(1)';
    }, 10);
});
