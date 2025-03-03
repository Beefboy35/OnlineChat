
document.getElementById("getLoggedIn").addEventListener("click", () => {
    window.location.href = "/login";
});

const errorBlock = document.getElementById("showError");
document.querySelector('form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Не отправлять форму стандартным образом

    const formData = new FormData(event.target); // Собрать данные формы
    const data = Object.fromEntries(formData); // Преобразовать FormData в обычный объект
    console.log(data)
    try {
        const response = await axios.post("/auth/register", {
            phone_number: data.phone,
            first_name: data.first_name,
            last_name: data.last_name,
            nickname: data.nickname,
            email: data.email,
            password: data.password,
            confirm_password: data.confirm_password,

        }, {
        headers: {
        'CSRF-Token': data.csrf_token
        } // Отправка токена в заголовке
    });
        if (response.status === 200) {
            console.log(`Пользователь ${data.nickname} зарегистрирован`);
            window.location.href = "/main_page";
        }
    } catch (error) {
           // Обработка ошибок
           errorBlock.innerText = error.response.data || "Ошибка при регистрации, попробуйте позже";
           errorBlock.classList.remove('hidden')
           setTimeout(() => {
            errorBlock.classList.add("hidden");
           }, 2000);
           console.error("Ошибка при регистрации:", error.response ? error.response.data : error);
       }
   });
