# Задача: написать formatter для openHAB `.items` файлов

Нужно создать CLI-утилиту `openhab-items-format`, которая форматирует openHAB `.items` файлы в читаемый многострочный стиль.

Утилита должна уметь:

```bash
openhab-items-format file.items
openhab-items-format --write file.items
openhab-items-format --check file.items
cat file.items | openhab-items-format
```

Ключевое требование: утилита позже будет подключена к Neovim через `conform.nvim`, поэтому обязательно поддержать режим:

```bash
openhab-items-format
```

где вход читается из `stdin`, а отформатированный результат пишется в `stdout`.

## Важные правила для совместимости с conform.nvim

1. Если вход читается из `stdin`, результат должен идти только в `stdout`.
2. Диагностика, предупреждения и ошибки должны идти только в `stderr`.
3. Утилита не должна печатать баннеры, логи, статистику или сообщения об успехе в `stdout`.
4. Exit code:

   * `0` — форматирование успешно;
   * `1` — ошибка парсинга, ошибка файла или `--check` обнаружил отличия;
   * `2` — неправильные аргументы CLI.
5. В режиме stdin/stdout утилита не должна модифицировать файлы.
6. Утилита должна быть идемпотентной: повторное форматирование уже отформатированного файла не должно менять результат.

Проверка идемпотентности:

```bash
openhab-items-format input.items > out1.items
openhab-items-format out1.items > out2.items
diff -u out1.items out2.items
```

`diff` должен быть пустым.

## Язык и структура проекта

Предпочтительно Python 3.11+.

Пример структуры:

```text
openhab_items_format/
  __init__.py
  cli.py
  formatter.py
  parser.py
  scanner.py
  model.py
tests/
  test_formatter.py
  fixtures/
pyproject.toml
README.md
```

Команда должна устанавливаться как console script:

```toml
[project.scripts]
openhab-items-format = "openhab_items_format.cli:main"
```

## Целевой стиль форматирования

Исходная строка:

```java
Number:Temperature localCurrentTemperature "Температура [%.1f %unit%]" <temperature2> (CurrentWeather) [Measurement, Temperature, "AI", "Weather", "Ai_Report"] { unit="°C", channel="mqtt:topic:mosquitto:OpenMeteo_Current:temperature", ai="state" [ aliases="температура сейчас,температура на улице", readable=true, writable=false, safety="read-only" ], report="diagnostics" [ priority=35, context=true ] }
```

Должна форматироваться так:

```java
Number:Temperature localCurrentTemperature
    "Температура [%.1f %unit%]"
    <temperature2>
    (CurrentWeather)
    [Measurement, Temperature, "AI", "Weather", "Ai_Report"]
{
    unit="°C",
    channel="mqtt:topic:mosquitto:OpenMeteo_Current:temperature",

    ai="state" [
        aliases="температура сейчас,температура на улице",
        readable=true,
        writable=false,
        safety="read-only"
    ],

    report="diagnostics" [
        priority=35,
        context=true
    ]
}
```

Основные правила:

1. Первая строка:

   ```java
   <Type> <Name>
   ```

2. Остальные части Item definition идут отдельными строками с отступом 4 пробела:

   ```java
       "Label"
       <icon>
       (Groups)
       [Tags]
   ```

3. Блок `{ ... }` открывается с новой строки без отступа:

   ```java
   {
       ...
   }
   ```

4. Внутри `{ ... }`:

   * каждый верхнеуровневый параметр — отдельной строкой;
   * простые параметры форматируются так:

     ```java
     key=value,
     key="value"
     ```
   * metadata/block параметры вида:

     ```java
     ai="state" [ ... ]
     ```

     форматируются многострочно:

     ```java
     ai="state" [
         readable=true,
         writable=false
     ]
     ```

5. Между многострочными metadata-блоками желательно оставлять пустую строку:

   ```java
   channel="...",

   ai="state" [
       ...
   ],

   report="diagnostics" [
       ...
   ]
   ```

6. Последний элемент внутри `{ ... }` не обязан иметь trailing comma. Лучше убрать trailing comma у последнего элемента.

7. Не переносить строки внутри кавычек:

   ```java
   aliases="a,b,c"
   channel="mqtt:topic:..."
   ```

## Что нужно поддержать в синтаксисе Item

Минимально поддержать такие формы:

```java
Switch ItemName
Switch ItemName "Label"
Switch ItemName "Label" <icon>
Switch ItemName "Label" <icon> (Group1, Group2)
Switch ItemName "Label" <icon> (Group1, Group2) [Tag1, Tag2, "Custom"]
Switch ItemName "Label" <icon> (Group1, Group2) [Tag1, Tag2] { channel="..." }
Number:Temperature ItemName "Label [%.1f %unit%]" <temperature> (Group) [Measurement, Temperature] { unit="°C", channel="..." }
Group:Switch:OR(ON, OFF) Some_Group "Label" <icon> (Parent) ["Lightbulb"]
```

То есть `Type` не всегда простой. Он может быть:

```java
Switch
Number
Number:Temperature
Group
Group:Switch
Group:Switch:OR(ON, OFF)
Dimmer
Color
String
DateTime
Contact
```

Не нужно валидировать openHAB-семантику. Formatter должен только форматировать текст.

## Не делать regex-only parser

Нельзя просто делить по запятым или скобкам регулярками.

Нужно написать небольшой scanner/tokenizer, который умеет проходить строку посимвольно и учитывать:

```text
"..."       строки
'...'       если встретятся, лучше тоже поддержать
(...)       groups или часть type
[...]       tags или metadata config
{...}       config block
<...>       icon
// ...      line comment
/* ... */   block comment, если встретится
```

Главная функция:

```python
split_top_level_commas(text: str) -> list[str]
```

Она должна делить строку по запятым только на верхнем уровне.

Пример:

```python
split_top_level_commas(
    'channel="x", ai="state" [ aliases="a,b,c", readable=true ], unit="°C"'
)
```

Результат:

```python
[
    'channel="x"',
    'ai="state" [ aliases="a,b,c", readable=true ]',
    'unit="°C"',
]
```

Запятая внутри `aliases="a,b,c"` не должна считаться разделителем.

## Обработка файла

Алгоритм верхнего уровня:

1. Читать весь текст.
2. Разбить его на логические блоки:

   * пустые строки;
   * комментарии;
   * item definitions;
   * неизвестные строки.
3. Для каждого item definition:

   * попытаться распарсить;
   * если успешно — отформатировать;
   * если неуспешно — оставить блок как есть и вывести warning в `stderr`.
4. Собрать файл обратно.

Важно: formatter не должен ломать файл из-за одной непонятной строки. Лучше оставить неизвестный блок без изменений.

## Как определить границы Item definition

Item definition начинается со строки, которая не является комментарием и начинается с похожего на openHAB type токена:

```text
Switch
Dimmer
Color
String
Number
Number:...
DateTime
Contact
Rollershutter
Player
Image
Location
Call
Group
Group:...
```

Но не надо делать слишком жёсткую проверку. Лучше иметь список известных префиксов и fallback.

Item definition может быть:

1. Однострочной.
2. Многострочной.
3. С `{ ... }`, где блок может занимать несколько строк.

Границы можно искать так:

* начать с первой строки Item;
* продолжать читать строки, пока все скобки верхнего уровня не закрыты;
* учитывать строки в кавычках;
* если `{` открыт, читать до соответствующего `}`;
* если `{` нет, item заканчивается перед следующей пустой строкой, комментарием или новой строкой, похожей на начало Item.

## Модель данных

Можно использовать dataclass:

```python
@dataclass
class ItemDefinition:
    item_type: str
    name: str
    label: str | None
    icon: str | None
    groups: str | None
    tags: str | None
    config: str | None
    original: str
```

`groups`, `tags`, `config` можно сначала хранить как raw string. Не нужно строить полноценное AST openHAB.

Для config:

```python
@dataclass
class ConfigEntry:
    raw: str
    key: str | None
    value: str | None
    metadata_config: str | None
```

## Форматирование config block

Вход:

```java
{ unit="°C", channel="mqtt:topic:mosquitto:OpenMeteo_Current:temperature", ai="state" [ aliases="температура сейчас,температура на улице", readable=true, writable=false, safety="read-only" ] }
```

Выход:

```java
{
    unit="°C",
    channel="mqtt:topic:mosquitto:OpenMeteo_Current:temperature",

    ai="state" [
        aliases="температура сейчас,температура на улице",
        readable=true,
        writable=false,
        safety="read-only"
    ]
}
```

Metadata block определяется как entry, содержащая верхнеуровневую `[` после `=`:

```java
ai="state" [ ... ]
report="diagnostics" [ ... ]
stateDescription="" [ ... ]
commandDescription="" [ ... ]
```

Внутренность `[ ... ]` тоже делится через `split_top_level_commas`.

## CLI

Поддержать:

```bash
openhab-items-format [--write] [--check] [--diff] [file]
```

Поведение:

### stdin/stdout

```bash
cat file.items | openhab-items-format
```

* читать stdin;
* писать отформатированный результат в stdout;
* ошибки в stderr.

### file argument

```bash
openhab-items-format file.items
```

* прочитать файл;
* отформатированный результат вывести в stdout;
* файл не менять.

### --write

```bash
openhab-items-format --write file.items
```

* прочитать файл;
* записать отформатированный результат обратно в файл;
* stdout оставить пустым;
* warnings/errors писать в stderr.

### --check

```bash
openhab-items-format --check file.items
```

* ничего не менять;
* если файл уже отформатирован, exit code `0`;
* если файл отличается от результата formatter, exit code `1`;
* сообщение в stderr:

  ```text
  file.items: needs formatting
  ```

### --diff

```bash
openhab-items-format --diff file.items
```

* вывести unified diff в stdout;
* exit code `1`, если есть отличия;
* exit code `0`, если отличий нет.

## Тесты

Нужны pytest-тесты.

Минимальные тесты:

1. Простая строка без config:

   ```java
   Switch Test "Test" <switch> (G1) [Tag]
   ```

2. Item с channel:

   ```java
   Switch Test "Test" <switch> (G1) [Tag] { channel="mqtt:topic:x:y" }
   ```

3. Item с metadata:

   ```java
   String Test "Test" { ai="state" [ aliases="a,b,c", readable=true, writable=false ] }
   ```

4. Item с несколькими config entries:

   ```java
   Number:Temperature T "Temp [%.1f %unit%]" <temperature> (Weather) [Measurement, Temperature] { unit="°C", channel="mqtt:topic:x:y", report="diagnostics" [ priority=35, context=true ] }
   ```

5. Не ломать запятые внутри строк:

   ```java
   aliases="a,b,c"
   expire="5m,command=OFF"
   ```

6. Идемпотентность:

   * форматировать fixture;
   * форматировать результат ещё раз;
   * сравнить.

7. Unknown lines:

   * непонятная строка должна сохраниться как есть;
   * warning должен идти в stderr.

8. Комментарии:

   ```java
   // comment
   Switch Test "Test"
   ```

   Комментарий должен сохраниться.

## Пример conform.nvim подключения

После реализации formatter должен работать с такой конфигурацией:

```lua
vim.filetype.add({
  extension = {
    items = "openhabitems",
  },
})

require("conform").setup({
  formatters_by_ft = {
    openhabitems = { "openhab_items_format" },
  },
  formatters = {
    openhab_items_format = {
      command = "openhab-items-format",
      stdin = true,
    },
  },
})
```

Поэтому stdout formatter'а должен содержать только отформатированный файл.

## Критерии готовности

1. Команда `openhab-items-format file.items` выводит форматированный текст в stdout.
2. Команда `cat file.items | openhab-items-format` работает так же.
3. Команда `openhab-items-format --write file.items` перезаписывает файл.
4. Команда `openhab-items-format --check file.items` корректно возвращает exit code.
5. Форматирование идемпотентно.
6. Запятые внутри строк не ломаются.
7. Metadata blocks форматируются многострочно.
8. Простые channel/unit параметры форматируются построчно.
9. Комментарии и пустые строки сохраняются.
10. Formatter можно безопасно подключить к `conform.nvim`.

