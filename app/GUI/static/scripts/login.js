document.getElementById("getSignedUp").addEventListener("click", () => {
    window.location.href = "/";
})
const errorBlock = document.getElementById("showError");
document.querySelector('form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Не отправлять форму стандартным образом

    const formData = new FormData(event.target); // Собрать данные формы
    const data = Object.fromEntries(formData); // Преобразовать FormData в обычный объект
    console.log(data);

    try {
        const response = await axios.post("/auth/login", {
            email: data.email,
            password: data.password,
        }, {
            headers: {
                'CSRF-Token': data.csrf_token
            } // Отправка токена в заголовке
        });

        if (response.status === 200) {
            console.log(`Пользователь ${data.nickname} успешно вошел`);
            window.location.href = "/main_page";
        }
    } catch (error) {
        // Обработка ошибок
        errorBlock.innerText = error.response?.data?.detail || "Ошибка при регистрации.";
        errorBlock.classList.remove('hidden');
        console.error("Ошибка при регистрации:", error);
        setTimeout(() => {
            errorBlock.classList.add('hidden');
        }, 2000);
      }
});