# Установка #
Установку можно произвести 2мя способами

## Из репазитория ##
Установка свежей версии из репазитория
системные требования svn
  * установим svn
> > `sudo apt-get install svn`
  * сделаем временную папку и перейдем в нее
> > `mkdir tmp && cd tmp`
  * получим рабочую копию из репазитория
> > `svn checkout http://vkontaktemusicthief.googlecode.com/svn/trunk/ vkontaktemusicthief`
  * создадим папку для плагина
> > `mkdir -p ~/.gnome2/rhythmbox/plugins/vkontakte`
  * скопируем файлы в папку
> > `cp vkontaktemusicthief/src/* ~/.gnome2/rhythmbox/plugins/vkontakte`
## Из файла ##
  * создадим папку для плагинов, если ее нет
> > `mkdir -p ~/.gnome2/rhythmbox/plugins`
  * перейдем в нее
> > `cd ~/.gnome2/rhythmbox/plugins`
  * скачаем файл
> > `wget http://vkontaktemusicthief.googlecode.com/files/vkontakte.music.thief.tar.gz`
  * распакуем
> > `tar -xzvf vkontakte.music.thief.tar.gz`
  * удалим не нужны архив
> > `rm vkontakte.music.thief.tar.gz`
# Имя юзера и пароль #

> После проделанной операции, в меню Edit-Plugins в самом низу появится новый пункт **VkontakteMusicThief** рядом с которым нужно будет поставить галочку, далее жимкнуть кнопку Configure и ввести имя пользователя и пароль (хранится это все будет в брелке гнома, так что переживать что кто то уведет пароль, не стоит :)) после этого нужно перезагрузить rhythmbox и если все прошло удачно то в меню слева в library появится новый пункт **Vkontakte Thief**, нажав на который вы должны будете увидеть свой плейлист
