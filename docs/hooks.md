# Работа с хуками

## Виды хуков:
1. `before_init`
2. `after_init` 
3. `before_deploy`
4. `after_deploy`
5. `before_rollback`
6. `after_rollback`


## Порядок работы с хуками
В качестве примера будет рассмотрен хук `before_init`. Работа с остальными аналогична.

1. Импортировать в модуль `fablib` список `before_init` из модуля `fablib`. 
2. Определить функцию `func` или ряд функций, которые будут запущены перед выполнением `init`.
3. Добавить нужные функции в список вызовом `fablib.before_init.append(func)`.

**При добавлении нескольких функций в список следует помнить о порядке их выполнения.**

## Пример использования хуков

``` python
import autodeploy.fablib as fl

fl.before_init.append(lambda: run('echo "hello from before init" >> hello.txt'))
fl.before_deploy.append(lambda: run('echo "Hello from deploy" >> hello.txt'))
fl.before_rollback.append(lambda: run('echo "Hello from rollback" >> hello.txt'))

fl.after_init.append(lambda: run('echo "Bye from init" >> bye.txt'))
fl.after_deploy.append(lambda: run('echo "Bye from deploy" >> bye.txt'))
fl.after_rollback.append(lambda: run('echo "Bye from rollback" >> bye.txt'))
```


**[Обратно к README](../README.md)**