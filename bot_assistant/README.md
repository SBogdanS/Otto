# team_project_1_group_10
Team project (Python core 21, group 10)
__________________________________________________________

#Інструкція з використання

##1. Опис програми.

Помічник Otto - wе консольний бот-асистент, взаємодія з яким відбувається через команди в консолі. 
Пакет знаходиться в репозиторії GitHub, завантажити його можна за посиланням: 
`<link>` :https://github.com/Yuliia-Vogel/team-project1-group10

###1.1 Встановлення.

Щоб встановити пакет помічника Otto, слід спочатку розархівувати його. 
Потім через консоль зайти в зовнішню папку "bot_assistant" та набрати в консолі команду "pip install e ." та натиснути "Enter" на клавіатурі.
Пакет встановиться разом з необхідним для його роботи пакетом "prompt_toolkit" (це може зайняти кілька хвилин).
Якщо установка була неуспішною, будь ласка, повідомте про це команду розробників пакету "bot_assistant".

###1.2. Запуск.

Щоб запустити встновлений помічник Otto, слід в консолі написати команду "otto" (без лапок та пробілів) та натиснути "Enter" на клавіатурі.
Після цього на екрані має з"явитися привітання "Hello my name is Otto. How can I help you?" та нижче - "Enter command:" і курсор, що блимає.
Якщо запуск виявився неуспішним, будь ласка, повідомте про це команду розробників пакету "bot_assistant".

##2. Використання програми.

Функціонал помічника Otto можна розділити на три великі частини:
> робота з контактною книгою,
> робота з нотатками,
> сортування файлів у вказаній папці.

Користувач вводить команду та натискає "Enter", а бот опрацьовує команду і виводить відповідь.
Після того, як користувач ввів першу літеру команди, бот у випадаючому списку пропонує набір команд, що підходять за першою введеною літерою, і стрілочками "вгору" та "вниз" на клавіатурі можна обрати необхідну команду. 
Після того - або "Enter", якщо команда не передбачає введення додаткової інформації, або натиснути пробіл і продовжити введенняданих.
Випадаючий список підказок випадає лише один раз після першої літери. Якщо список підказок зник, а користувач не обрав потрібну команду, то команду можна ввести самостійно.
Якщо команда буде введена некоректно, помічник Otto повідомить про це користувача та попросить ввести іншу команду.
Після того, як було введено команду для виходу з програми, помічник Otto закривається і зберігає всі дані (створені та відредаговані контакти та нотатки) у файлах формату json.

Щоб продовжити роботу з помічник Otto, який закрився, будь ласка, повторіть дії, описані в пункті 1.2.

###2.2. Команди для використання помічника "otto".

####2.2.1. Загальні команди.

    - `hello`: виводить "How can I help you?".
    - `good bye`, `close`, `exit`, `.`: ці команди завершують роботу і зберігають всі дані (контакти та нотатки) в файл на диску в поточну папку.
    - `help`: виводить список усіх доступних команд.

####2.2.2. Команди для використання Контактної книги.

    - `add_contact`: додає контакт до контактної книги. Після команди через пробіл потрібно вказати ім'я та через пробіл номер телефону контакту. 
    - `add_birthday`: додає день народження для контакту. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі) та через пробіл дату народження у форматі рік-місяць-день, наприклад 2005-05-29.
    - `add_email`: додає електронну пошту для контакту. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі) та через пробіл електронну пошту.
    - `add_phone`: додає телефон до списку телефонів контакту. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі) та через пробіл номер телефону.
    - `change_contact_phone`: змінити контактний телефон. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі) та через пробіл номер телефону.
    - `show_all_contacts`: демонструє всі контакти.
    - `delete_contact`: видаляє контакт. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі).
    - `search_contacts`: пошук і виведення даних про контакт. Після команди через пробіл потрібно вказати ім'я контакту (точно як записано в контактній книзі).
    - `search_by_bd`: виведення всіх днів народження протягом наступних 14 днів від сьогоднішньої (поточної) дати.

####2.2.3. Команди для використання Нотаток.

    - `add_note`: додає нотатку до нотатника. Бот запитує: 1. "Enter the title of the note:  " - після команди через пробіл потрібно ввести назву нотатки. Краще вводити одне слово або розділяти слова нижнім підкресленням ("_"), накше нотатку неможливо буде редагувати.
							   2. "Enter the content of the note: " - після команди через пробіл потрібно ввести текст нотатки. 
							   3. "Enter tags, separated by commas: " - після команди через пробіл потрібно ввести ключові слова.
    - `search_note': здійснює пошук нотаток за вказаними ключовими словами і сортує їх від новішої до старішої (за датою). Після команди через пробіл потрібно вказати ключове слово.
    - `edit_note`: редагує існуючу нотатку. Після команди через пробіл потрібно вказати "назву нотатки" та через пробіл "новий текст нотатки".
    - `remove_note`: видаляє нотатку. Після команди через пробіл потрібно вказати назву нотатки.
    - `show_note`: виводить список всіх нотаток.
    - `help_note`: виводить список доступних команд для нотатника (без функцій з контактами).
 
####2.2.4. Команди для використання функції сортування файлів у папці.

    - `sort_files': здійснює сортування файлів у папці за заданим шляхом. Після команди через пробіл потрібно вказати шлях до папки, яку слід опрацювати.


##3. Вимоги до системи.
Бот-асистент працює на системах Linux та Windows.
